"""Defines a Weights & Biases logging inferface.

This interface is used to log metrics and artifacts to Weights & Biases.
"""

import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, TypeVar

import wandb
from omegaconf import OmegaConf
from torch import Tensor

from ml.core.config import conf_field
from ml.core.env import get_exp_name, get_wandb_entity
from ml.core.registry import register_logger
from ml.core.state import Phase, State
from ml.loggers.base import BaseLogger, BaseLoggerConfig
from ml.loggers.multi import TARGET_FPS
from ml.utils.distributed import is_master
from ml.utils.logging import IntervalTicker
from ml.utils.numpy import as_numpy_array

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class WandbLoggerConfig(BaseLoggerConfig):
    flush_seconds: float = conf_field(10.0, help="How often to flush logs")


@register_logger("wandb", WandbLoggerConfig)
class WandbLogger(BaseLogger[WandbLoggerConfig]):
    def __init__(self, config: WandbLoggerConfig) -> None:
        super().__init__(config)

        self.scalars: dict[Phase, dict[str, Callable[[], int | float | Tensor]]] = defaultdict(dict)
        self.strings: dict[Phase, dict[str, Callable[[], str]]] = defaultdict(dict)
        self.images: dict[Phase, dict[str, Callable[[], Tensor]]] = defaultdict(dict)
        self.audio: dict[Phase, dict[str, Callable[[], tuple[Tensor, int]]]] = defaultdict(dict)
        self.videos: dict[Phase, dict[str, Callable[[], Tensor]]] = defaultdict(dict)

        self.warning_ticker = IntervalTicker(60.0)

    def initialize(self, log_directory: Path) -> None:
        super().initialize(log_directory)

        if not is_master():
            return

        log_directory.mkdir(exist_ok=True, parents=True)

        # Initializes Weights & Biases.
        wandb.init(
            project=get_exp_name(),
            entity=get_wandb_entity(),
            dir=log_directory,
            config=OmegaConf.to_container(self.raw_config),  # type: ignore[arg-type]
        )

    def log_scalar(self, key: str, value: Callable[[], int | float | Tensor], state: State, namespace: str) -> None:
        if is_master():
            self.scalars[state.phase][f"{namespace}/{key}"] = value

    def log_string(self, key: str, value: Callable[[], str], state: State, namespace: str) -> None:
        if is_master():
            self.strings[state.phase][f"{namespace}/{key}"] = value

    def log_image(self, key: str, value: Callable[[], Tensor], state: State, namespace: str) -> None:
        if is_master():
            self.images[state.phase][f"{namespace}/{key}"] = value

    def log_audio(self, key: str, value: Callable[[], tuple[Tensor, int]], state: State, namespace: str) -> None:
        if is_master():
            self.audio[state.phase][f"{namespace}/{key}"] = value

    def log_video(self, key: str, value: Callable[[], Tensor], state: State, namespace: str) -> None:
        if is_master():
            self.videos[state.phase][f"{namespace}/{key}"] = value

    def write(self, state: State) -> None:
        if not is_master():
            return

        all_keys: set[str] = set()

        def filter_items(items: Iterable[tuple[str, T]]) -> Iterable[tuple[str, T]]:
            duplicate_keys: set[str] = set()
            for k, v in items:
                if k in all_keys:
                    duplicate_keys
                else:
                    all_keys.add(k)
                    yield k, v
            if duplicate_keys and self.warning_ticker.tick():
                logger.warning("Found duplicate logging key(s): %s", duplicate_keys)

        for scalar_key, scalar_value in filter_items(self.scalars[state.phase].items()):
            wandb.log({scalar_key: scalar_value()}, step=state.num_steps)

        for string_key, string_value in filter_items(self.strings[state.phase].items()):
            wandb.log({string_key: string_value()}, step=state.num_steps)

        for image_key, image_value in filter_items(self.images[state.phase].items()):
            wandb.log({image_key: wandb.Image(image_value())}, step=state.num_steps)

        for audio_key, audio_value in filter_items(self.audio[state.phase].items()):
            audio_wav, audio_sample_rate = audio_value()
            wandb.log({audio_key: wandb.Audio(audio_wav, sample_rate=audio_sample_rate)}, step=state.num_steps)

        for video_key, video_value in filter_items(self.videos[state.phase].items()):
            wandb.log(
                {video_key: wandb.Video(as_numpy_array(video_value().unsqueeze(0)), fps=TARGET_FPS)},
                step=state.num_steps,
            )

        self.clear(state)

    def clear(self, state: State) -> None:
        self.scalars[state.phase].clear()
        self.strings[state.phase].clear()
        self.images[state.phase].clear()
        self.audio[state.phase].clear()
        self.videos[state.phase].clear()

    def default_write_every_n_seconds(self, state: State) -> float:
        return 10.0 if state.num_steps > 5000 else 1.0
