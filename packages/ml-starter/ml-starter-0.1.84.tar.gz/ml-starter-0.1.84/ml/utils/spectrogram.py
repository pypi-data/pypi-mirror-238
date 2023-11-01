# mypy: disable-error-code="import"
"""Defines spectrogram functions.

This file contains utilities for converting waveforms to MFCCs and back. This
can be a more useful representation to use for training models than raw
waveforms, since it's easier for models to learn patterns in the MFCCs than
in the waveforms.
"""

import argparse
import logging
from pathlib import Path
from typing import Literal, NamedTuple

import numpy as np
import torch
import torchaudio
import torchaudio.functional as A
from torch import Tensor, nn
from torchaudio.transforms import GriffinLim, InverseSpectrogram, Spectrogram

from ml.utils.amp import autocast_tensors
from ml.utils.logging import configure_logging
from ml.utils.numpy import as_numpy_array

logger = logging.getLogger(__name__)

Array = Tensor | np.ndarray

try:
    import pyworld
except ModuleNotFoundError:
    pyworld = None


class _Normalizer(nn.Module):
    __constants__ = ["_dims"]

    def __init__(self, dims: int) -> None:
        super().__init__()

        self._dims = dims

        self.register_buffer("_loc", torch.zeros(dims))
        self.register_buffer("_scale", torch.ones(dims))
        self.register_buffer("_ema", torch.zeros(1))

    _loc: Tensor
    _scale: Tensor
    _ema: Tensor

    def normalize(self, x: Tensor) -> Tensor:
        """Normalizes a signal along the final dimension.

        This updates the running mean and standard deviation of the signal
        if training.

        Args:
            x: The input tensor, with shape ``(*, N)``

        Returns:
            The normalized tensor, with shape ``(*, N)``
        """
        if self.training:
            mean, std = x.flatten(0, -2).mean(0), x.flatten(0, -2).std(0)
            self._loc.mul_(self._ema).add_(mean * (1 - self._ema))
            self._scale.mul_(self._ema).add_(std * (1 - self._ema))
            self._ema.add_(0.001 * (1 - self._ema))
        x = (x - self._loc) / self._scale
        return x

    def denormalize(self, x: Tensor) -> Tensor:
        """Denormalizes a signal along the final dimension.

        Args:
            x: The latent tensor, with shape ``(*, N)``

        Returns:
            The denormalized tensor, with shape ``(*, N)``
        """
        return x * self._scale + self._loc

    @property
    def dimensions(self) -> int:
        """Returns the dimensionality of the latent space.

        Returns:
            The dimensionality of the latent space.
        """
        return self._dims


class AudioMfccConverter(_Normalizer):
    """Defines a module for converting waveforms to MFCCs and back.

    This module returns the normalized MFCCs from the waveforms. It uses
    the pseudoinverse of the mel filterbanks and the DCT matrix to convert
    MFCCs back to spectrograms, and then uses the Griffin-Lim algorithm to
    convert spectrograms back to waveforms. The pseudoinverse is used because
    it's faster than doing gradient decent every time we want to generate a
    spectrogram.

    Parameters:
        sample_rate: Sample rate of the audio.
        n_mfcc: Number of MFCC bands.
        n_mels: Number of Mel bands.
        n_fft: Number of FFT bands.
        hop_length: Hop length for the STFT.
        win_length: Window length for the STFT.
    """

    def __init__(
        self,
        sample_rate: int = 16_000,
        n_mfcc: int = 40,
        n_mels: int = 128,
        n_fft: int = 1024,
        hop_length: int | None = None,
        win_length: int | None = None,
    ) -> None:
        super().__init__(n_mfcc)

        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length or n_fft // 4
        self.win_length = win_length or n_fft

        self.spec = Spectrogram(n_fft=n_fft, hop_length=hop_length, win_length=win_length, power=2, normalized=False)
        self.griffin_lim = GriffinLim(n_fft=n_fft, hop_length=hop_length, win_length=win_length, power=2)

        mel_fb = A.melscale_fbanks(n_fft // 2 + 1, 0.0, sample_rate // 2, n_mels, sample_rate)
        self.register_buffer("mel_fb", mel_fb)
        self.register_buffer("inv_mel_fb", torch.linalg.pinv(mel_fb))

        dct_mat = A.create_dct(n_mfcc, n_mels, "ortho")
        self.register_buffer("dct_mat", dct_mat)
        self.register_buffer("inv_dct_mat", torch.linalg.pinv(dct_mat))

    mel_fb: Tensor
    inv_mel_fb: Tensor
    dct_mat: Tensor
    inv_dct_mat: Tensor

    def audio_to_spec(self, waveform: Tensor) -> Tensor:
        """Converts a waveform to MFCCs.

        Args:
            waveform: Tensor of shape ``(..., num_samples)``.

        Returns:
            Tensor of shape ``(..., num_frames, n_mfcc)``.
        """
        with autocast_tensors(waveform, enabled=False) as waveform:
            spec = self.spec(waveform)
            mel_spec = torch.einsum("...ct,cf->...ft", spec, self.mel_fb)
            log_mel_spec = torch.log(mel_spec + 1e-6)
            mfcc = torch.einsum("...ct,cf->...tf", log_mel_spec, self.dct_mat)
            mfcc = self.normalize(mfcc)
            return mfcc

    def spec_to_audio(self, mfcc: Tensor) -> Tensor:
        """Converts MFCCs to a waveform.

        Args:
            mfcc: Tensor of shape ``(..., n_mfcc, num_frames)``.

        Returns:
            Tensor of shape ``(..., num_samples)``.
        """
        with autocast_tensors(mfcc.detach(), enabled=False) as mfcc:
            mfcc = self.denormalize(mfcc)
            log_mel_spec = torch.einsum("...tf,fc->...tc", mfcc, self.inv_dct_mat)
            mel_spec = torch.exp(log_mel_spec) - 1e-6
            spec = torch.einsum("...tf,fc->...ct", mel_spec, self.inv_mel_fb).clamp_min_(1e-8)
            waveform = self.griffin_lim(spec)
            return waveform


class AudioStftConverter(_Normalizer):
    """Defines a class for converting waveforms to spectrograms and back.

    This is an exact forward and backward transformation, meaning that the
    input can be reconstructed perfectly from the output. However, oftentimes
    the phase information is not easy to deal with for downstream networks.

    Parameters:
        n_fft: Number of FFT bands.
        hop_length: Hop length for the STFT.
        win_length: Window length for the STFT.
    """

    def __init__(
        self,
        n_fft: int = 1024,
        hop_length: int | None = None,
        win_length: int | None = None,
    ) -> None:
        super().__init__(n_fft // 2 + 1)

        self.n_fft = n_fft
        self.win_length = win_length or n_fft
        self.hop_length = hop_length or self.win_length // 4

        self.stft = Spectrogram(self.n_fft, self.win_length, self.hop_length, power=None, normalized=True)
        self.istft = InverseSpectrogram(self.n_fft, self.win_length, self.hop_length, normalized=True)

    def normalize(self, mag: Tensor) -> Tensor:
        log_mag = torch.log(mag + 1e-6)
        return super().normalize(log_mag)

    def denormalize(self, log_mag: Tensor) -> Tensor:
        log_mag = super().denormalize(log_mag)
        return torch.exp(log_mag) - 1e-6

    def audio_to_spec(self, waveform: Tensor) -> Tensor:
        """Converts a waveform to a spectrogram.

        This version keeps the phase information, in a parallel channel with
        the magnitude information.

        Args:
            waveform: Tensor of shape ``(..., num_samples)``.

        Returns:
            Tensor of shape ``(..., 2, num_frames, n_fft // 2 + 1)``.
            The first channel is the magnitude, the second is the phase.
        """
        with autocast_tensors(waveform, enabled=False) as waveform:
            spec = self.stft(waveform.detach())
            mag = self.normalize(spec.abs().transpose(-1, -2))
            phase = spec.angle().transpose(-1, -2)
            return torch.stack((mag, phase), -3)

    def spec_to_audio(self, spec: Tensor) -> Tensor:
        """Converts a spectrogram to a waveform.

        This version expects the spectrogram to have two channels, one for
        magnitude and one for phase.

        Args:
            spec: Tensor of shape ``(..., 2, num_frames, n_fft // 2 + 1)``.

        Returns:
            Tensor of shape ``(..., num_samples)``, the reconstructed waveform.
        """
        with autocast_tensors(spec, enabled=False) as spec:
            mag, phase = spec.detach().unbind(-3)
            mag = self.denormalize(mag).transpose(-1, -2)
            phase = phase.transpose(-1, -2)
            real, imag = mag * phase.cos(), mag * phase.sin()
            spec = torch.complex(real, imag)
            waveform = self.istft(spec)
            return waveform


class AudioMagStftConverter(_Normalizer):
    def __init__(
        self,
        n_fft: int = 1024,
        n_iter: int = 32,
        hop_length: int | None = None,
        win_length: int | None = None,
    ) -> None:
        super().__init__(n_fft // 2 + 1)

        self.n_fft = n_fft
        self.n_iter = n_iter
        self.win_length = win_length or n_fft
        self.hop_length = hop_length or self.win_length // 4

        self.stft = Spectrogram(self.n_fft, self.win_length, self.hop_length, power=2, normalized=False)
        self.griffin_lim = GriffinLim(self.n_fft, n_iter, self.win_length, self.hop_length, power=2)

    def audio_to_mag_spec(self, waveform: Tensor) -> Tensor:
        """Converts a waveform to a magnitude spectrogram.

        Args:
            waveform: Tensor of shape ``(..., num_samples)``.

        Returns:
            Tensor of shape ``(..., num_frames, n_fft // 2 + 1)``.
        """
        with autocast_tensors(waveform, enabled=False) as waveform:
            mag = self.stft(waveform.detach())
            log_mag = torch.log(mag + 1e-6)
            log_mag = self.normalize(log_mag.transpose(-1, -2))
            return log_mag

    def mag_spec_to_audio(self, mag: Tensor) -> Tensor:
        """Converts a magnitude spectrogram to a waveform.

        Args:
            mag: Tensor of shape ``(..., num_frames, n_fft // 2 + 1)``.

        Returns:
            Tensor of shape ``(..., num_samples)``, the reconstructed waveform.
        """
        with autocast_tensors(mag, enabled=False) as mag:
            log_mag = self.denormalize(mag.detach()).transpose(-1, -2)
            mag = (torch.exp(log_mag) - 1e-6).clamp_min_(1e-8)
            waveform = self.griffin_lim(mag)
            return waveform


class WorldFeatures(NamedTuple):
    sp: Tensor
    f0: Tensor
    ap: Tensor


class AudioPyworldConverter(_Normalizer):
    """Defines a class for converting waveforms to PyWorld features and back.

    This function also normalizes the features to have zero mean and unit
    variance using statistics over time.

    Parameters:
        sample_rate: Sample rate of the audio.
        dim: Dimension of the PyWorld features.
        frame_period: Frame period in milliseconds.
        f0_floor: Minimum F0 value.
        f0_ceil: Maximum F0 value.
    """

    def __init__(
        self,
        sample_rate: int = 16_000,
        dim: int = 24,
        frame_period: float = 5.0,
        f0_floor: float = 71.0,
        f0_ceil: float = 800.0,
    ) -> None:
        super().__init__(dim)

        if pyworld is None:
            raise ModuleNotFoundError("PyWorld is not installed; please install it with `pip install pyworld`.")

        self.sampling_rate = sample_rate
        self.dim = dim
        self.frame_period = frame_period
        self.f0_floor = f0_floor
        self.f0_ceil = f0_ceil

    def normalize(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return super().normalize(torch.from_numpy(x).to(self._scale)).detach().cpu().numpy().astype(np.float64)

    def denormalize(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return super().denormalize(torch.from_numpy(x).to(self._scale)).detach().cpu().numpy().astype(np.float64)

    def audio_to_features(self, waveform: np.ndarray) -> WorldFeatures:
        assert pyworld is not None

        waveform = waveform.astype(np.float64)
        f0, timeaxis = pyworld.harvest(  # F0 estimation
            waveform,
            self.sampling_rate,
            frame_period=self.frame_period,
            f0_floor=self.f0_floor,
            f0_ceil=self.f0_ceil,
        )
        sp = pyworld.cheaptrick(waveform, f0, timeaxis, self.sampling_rate)  # Smoothed spectrogram
        ap = pyworld.d4c(waveform, f0, timeaxis, self.sampling_rate)  # Harmonics spectral envelope
        coded_sp = pyworld.code_spectral_envelope(sp, self.sampling_rate, self.dim)  # Mel-cepstral coefficients
        coded_sp = self.normalize(coded_sp)
        return WorldFeatures(sp=torch.from_numpy(coded_sp), f0=torch.from_numpy(f0), ap=torch.from_numpy(ap))

    def features_to_audio(self, features: WorldFeatures | tuple[Array, Array, Array]) -> np.ndarray:
        assert pyworld is not None

        coded_sp, f0, ap = (as_numpy_array(f) for f in features)
        coded_sp = self.denormalize(coded_sp)
        fftlen = pyworld.get_cheaptrick_fft_size(self.sampling_rate)  # Obtaining FFT size from the sampling rate
        decoded_sp = pyworld.decode_spectral_envelope(coded_sp, self.sampling_rate, fftlen)  # Decoding the spectrum
        wav = pyworld.synthesize(f0, decoded_sp, ap, self.sampling_rate, self.frame_period)  # Synthesizing the waveform
        return wav


class SpectrogramToMFCCs(_Normalizer):
    __constants__ = _Normalizer.__constants__ + ["n_fft"]

    def __init__(
        self,
        sample_rate: int = 16_000,
        n_mels: int = 128,
        n_mfcc: int = 40,
        f_min: float = 0.0,
        f_max: float | None = None,
        n_stft: int = 201,
        norm: str | None = None,
        mel_scale: str = "htk",
        dct_norm: str = "ortho",
    ) -> None:
        super().__init__(n_mfcc)

        self.n_fft = (n_stft - 1) * 2

        # Convert raw spectrogram to MFCCs. This is differentiable since
        # the transformations are just matrix multiplications.
        self.mel_scale = torchaudio.transforms.MelScale(n_mels, sample_rate, f_min, f_max, n_stft, norm, mel_scale)
        dct_mat = A.create_dct(n_mfcc, n_mels, dct_norm)
        self.register_buffer("dct_mat", dct_mat)

    dct_mat: Tensor

    def audio_to_spec(self, waveform: Tensor) -> Tensor:
        return torch.stft(waveform, n_fft=self.n_fft, return_complex=True).abs()

    def forward(self, spec: Tensor) -> Tensor:
        x = self.mel_scale(spec)
        x = torch.log(x.clamp_min(1e-6))
        x = torch.einsum("...ij,ik->...kj", x, self.dct_mat)
        x = self.normalize(x.transpose(-1, -2))
        return x


class AudioToHifiGanMels(nn.Module):
    """Defines a module to convert from a waveform to the mels used by HiFi-GAN.

    This module can be used to get the target Mel spectrograms during training
    that will be compatible with pre-trained HiFi-GAN models. Since the full
    HiFi-GAN model can be expensive to load during inference, Griffin-Lim is
    used here to provide a light-weight reconstruction of the audio from the
    Mel spectrogram during training (although the quality will be poor). Then,
    during inference, the full HiFi-GAN model can be used instead.

    Parameters:
        sampling_rate: The sampling rate of the audio.
        num_mels: The number of mel bins.
        n_fft: The number of FFT bins.
        win_size: The window size.
        fmin: The minimum frequency.
        fmax: The maximum frequency.
    """

    __constants__ = ["sampling_rate", "num_mels", "n_fft", "win_size", "hop_size", "fmin", "fmax"]

    def __init__(
        self,
        sampling_rate: int,
        num_mels: int,
        n_fft: int,
        win_size: int,
        hop_size: int,
        fmin: int = 0,
        fmax: int = 8000,
    ) -> None:
        super().__init__()

        self.sampling_rate = sampling_rate
        self.num_mels = num_mels
        self.n_fft = n_fft
        self.win_size = win_size
        self.hop_size = hop_size
        self.fmin = fmin
        self.fmax = fmax

        mel_fb = A.melscale_fbanks(
            n_freqs=n_fft // 2 + 1,
            f_min=fmin,
            f_max=fmax,
            n_mels=num_mels,
            sample_rate=sampling_rate,
            norm="slaney",
            mel_scale="slaney",
        )

        self.register_buffer("mel_fb", mel_fb)
        self.register_buffer("inv_mel_fb", torch.linalg.pinv(mel_fb))
        self.register_buffer("hann_window", torch.hann_window(win_size))

    mel_fb: Tensor
    inv_mel_fb: Tensor
    hann_window: Tensor

    @classmethod
    def for_hifigan(cls, hifigan_type: Literal["16000hz", "22050hz"]) -> "AudioToHifiGanMels":
        match hifigan_type:
            case "16000hz":
                return cls(
                    sampling_rate=16_000,
                    num_mels=128,
                    n_fft=1024,
                    win_size=1024,
                    hop_size=160,
                    fmin=0,
                    fmax=8000,
                )
            case "22050hz":
                return cls(
                    sampling_rate=22_050,
                    num_mels=80,
                    n_fft=1024,
                    win_size=1024,
                    hop_size=256,
                    fmin=0,
                    fmax=8000,
                )
            case _:
                raise ValueError(f"Unknown HiFi-GAN type: {hifigan_type}")

    @property
    def dimensions(self) -> int:
        return self.num_mels

    def _dynamic_range_compression(self, x: np.ndarray, c: float = 1.0, clip_val: float = 1e-5) -> np.ndarray:
        return np.log(np.clip(x, a_min=clip_val, a_max=None) * c)

    def _dynamic_range_decompression(self, x: np.ndarray, c: float = 1.0) -> np.ndarray:
        return np.exp(x) / c

    def _dynamic_range_compression_torch(self, x: Tensor, c: float = 1.0, clip_val: float = 1e-5) -> Tensor:
        return torch.log(torch.clamp(x, min=clip_val) * c)

    def _dynamic_range_decompression_torch(self, x: Tensor, c: float = 1.0) -> Tensor:
        return torch.exp(x) / c

    def _spectral_normalize_torch(self, magnitudes: Tensor) -> Tensor:
        output = self._dynamic_range_compression_torch(magnitudes)
        return output

    def _spectral_de_normalize_torch(self, magnitudes: Tensor) -> Tensor:
        output = self._dynamic_range_decompression_torch(magnitudes)
        return output

    def audio_to_mels(self, waveform: Tensor) -> Tensor:
        # Adds padding to the input waveform.
        pad = int((self.n_fft - self.hop_size) / 2)
        left_pad, right_pad = waveform[..., :pad].flip(-1), waveform[..., -pad:].flip(-1)
        waveform = torch.cat([left_pad, waveform, right_pad], dim=-1)

        spec = torch.stft(
            waveform,
            self.n_fft,
            hop_length=self.hop_size,
            win_length=self.win_size,
            window=self.hann_window,
            center=False,
            pad_mode="reflect",
            normalized=False,
            onesided=True,
            return_complex=True,
        )

        spec = torch.sqrt(spec.real.pow(2) + spec.imag.pow(2) + 1e-9)
        spec = torch.einsum("...ct,cm->...mt", spec, self.mel_fb)
        spec = self._spectral_normalize_torch(spec)
        return spec

    def mels_to_audio(self, spec: Tensor) -> Tensor:
        spec = self._spectral_de_normalize_torch(spec)
        spec = torch.einsum("...mt,mc->...ct", spec, self.inv_mel_fb)

        waveform = A.griffinlim(
            spec,
            self.hann_window,
            self.n_fft,
            self.hop_size,
            self.win_size,
            1,
            32,  # n_iter
            0.99,  # momentum
            None,  # length
            True,  # rand_init
        )

        return waveform


def test_audio_adhoc() -> None:
    configure_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["mfcc", "stft", "mag-stft", "pyworld", "hifigan"], help="Mode to test.")
    parser.add_argument("audio_file", help="Path to a specific audio file.")
    parser.add_argument("--output-dir", default="out", help="Path to the output directory.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_file = Path(args.audio_file)

    waveform, sample_rate = torchaudio.load(audio_file)
    waveform = waveform[0]  # Only use the first channel.

    if args.mode == "mfcc":
        mfcc_converter = AudioMfccConverter(sample_rate)
        mfcc = mfcc_converter.audio_to_spec(waveform)
        mfcc_waveform = mfcc_converter.spec_to_audio(mfcc)
        torchaudio.save(output_dir / "original.wav", waveform[None], sample_rate)
        torchaudio.save(output_dir / "reconstructed.wav", mfcc_waveform[None], sample_rate)
        return

    if args.mode == "stft":
        stft_converter = AudioStftConverter()
        stft = stft_converter.audio_to_spec(waveform)
        stft_waveform = stft_converter.spec_to_audio(stft)
        torchaudio.save(output_dir / "original.wav", waveform[None], sample_rate)
        torchaudio.save(output_dir / "reconstructed.wav", stft_waveform[None], sample_rate)
        return

    if args.mode == "mag-stft":
        mag_stft_converter = AudioMagStftConverter()
        mag_stft = mag_stft_converter.audio_to_mag_spec(waveform)
        mag_stft_waveform = mag_stft_converter.mag_spec_to_audio(mag_stft)
        torchaudio.save(output_dir / "original.wav", waveform[None], sample_rate)
        torchaudio.save(output_dir / "reconstructed.wav", mag_stft_waveform[None], sample_rate)
        return

    if args.mode == "pyworld":
        pyworld_converter = AudioPyworldConverter(sample_rate)
        coded_sp = pyworld_converter.audio_to_features(waveform.numpy())
        pyworld_waveform = pyworld_converter.features_to_audio(coded_sp)
        pyworld_waveform_tensor = torch.from_numpy(pyworld_waveform).to(torch.float32)
        torchaudio.save(output_dir / "original.wav", waveform[None], sample_rate)
        torchaudio.save(output_dir / "reconstructed.wav", pyworld_waveform_tensor[None], sample_rate)
        return

    if args.mode == "hifigan":
        hifigan_converter = AudioToHifiGanMels.for_hifigan("16000hz")
        mels = hifigan_converter.audio_to_mels(waveform)
        mels_waveform = hifigan_converter.mels_to_audio(mels)
        torchaudio.save(output_dir / "original.wav", waveform[None], sample_rate)
        torchaudio.save(output_dir / "reconstructed.wav", mels_waveform[None], sample_rate)
        return

    raise ValueError(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    # python -m ml.utils.spectrogram
    test_audio_adhoc()
