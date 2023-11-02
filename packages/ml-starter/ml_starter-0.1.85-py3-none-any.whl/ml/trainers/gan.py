"""Defines a trainer to use for training GANs.

This trainer is similar to the supervised learning trainer, but with separate
optimizers for the generator and discriminator, and supporting round robin
training.
"""

import contextlib
import logging
import signal
from dataclasses import dataclass
from types import FrameType
from typing import Collection, Generic, Iterator, TypeVar

from torch import Tensor, nn
from torch.optim.optimizer import Optimizer

from ml.core.common_types import Batch
from ml.core.config import conf_field
from ml.core.registry import register_trainer
from ml.core.state import Phase, State, set_phase
from ml.loggers.multi import namespace_context
from ml.lr_schedulers.base import BaseLRScheduler, SchedulerAdapter
from ml.lr_schedulers.gan import GenerativeAdversarialNetworkLRScheduler
from ml.models.gan import GenerativeAdversarialNetworkModel
from ml.optimizers.base import BaseOptimizer
from ml.optimizers.gan import GenerativeAdversarialNetworkOptimizer
from ml.tasks.gan.base import GenerativeAdversarialNetworkTask
from ml.tasks.gan.round_robin import GenerativeAdversarialNetworkRoundRobinTask
from ml.trainers.sl import EpochDoneError, SupervisedLearningTrainer, SupervisedLearningTrainerConfig
from ml.utils.containers import recursive_chunk
from ml.utils.device.base import InfinitePrefetcher
from ml.utils.exceptions import TrainingFinishedError
from ml.utils.timer import Timer

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class GenerativeAdversarialNetworkTrainerConfig(SupervisedLearningTrainerConfig):
    discriminator_key: str = conf_field("dis", help="The logging key for the discriminator")
    generator_key: str = conf_field("gen", help="The logging key for the generator")
    round_robin: bool = conf_field(True, help="If set, use round-robin training, otherwise run together")


GenerativeAdversarialNetworkTrainerConfigT = TypeVar(
    "GenerativeAdversarialNetworkTrainerConfigT",
    bound=GenerativeAdversarialNetworkTrainerConfig,
)
GenerativeAdversarialNetworkModelT = TypeVar(
    "GenerativeAdversarialNetworkModelT",
    bound=GenerativeAdversarialNetworkModel,
)
GenerativeAdversarialNetworkTaskT = TypeVar(
    "GenerativeAdversarialNetworkTaskT",
    GenerativeAdversarialNetworkTask,
    GenerativeAdversarialNetworkRoundRobinTask,
)


@register_trainer("gan", GenerativeAdversarialNetworkTrainerConfig)
class GenerativeAdversarialNetworkTrainer(
    SupervisedLearningTrainer[
        GenerativeAdversarialNetworkTrainerConfigT,
        GenerativeAdversarialNetworkModelT,
        GenerativeAdversarialNetworkTaskT,
    ],
    Generic[
        GenerativeAdversarialNetworkTrainerConfigT,
        GenerativeAdversarialNetworkModelT,
        GenerativeAdversarialNetworkTaskT,
    ],
):
    def _logging_key(self, task: GenerativeAdversarialNetworkTaskT, state: State, phase: Phase) -> str | None:
        if not isinstance(task, GenerativeAdversarialNetworkRoundRobinTask):
            return None
        is_gen = task.is_generator_step(state, phase)
        return self.config.generator_key if is_gen else self.config.discriminator_key

    def gan_train_step(
        self,
        *,
        task_model: nn.Module,
        params: tuple[list[nn.Parameter], list[nn.Parameter]],
        batches: Iterator[Batch],
        state: State,
        task: GenerativeAdversarialNetworkTaskT,
        model: GenerativeAdversarialNetworkModelT,
        optim: Optimizer | Collection[Optimizer],
        lr_sched: SchedulerAdapter | Collection[SchedulerAdapter],
    ) -> dict[str, Tensor]:
        if isinstance(task, GenerativeAdversarialNetworkRoundRobinTask):
            # For round robin training, we just follow the vanilla function.
            return self.train_step(
                task_model=task_model,
                batches=batches,
                state=state,
                task=task,
                model=model,
                optim=optim,
                lr_sched=lr_sched,
            )

        with self.step_context("change_mode"):
            task_model, state.phase = set_phase(task_model, "train")
        total_bsz: int | None = None
        losses: dict[str, tuple[Tensor, int]] = {}
        with self.step_context("zero_grads"):
            if isinstance(optim, Collection):
                for optim_i in optim:
                    optim_i.zero_grad(set_to_none=self.config.set_to_none)
            else:
                optim.zero_grad(set_to_none=self.config.set_to_none)
        num_steps = 0
        with self.autocast_context:
            for batch in batches:
                bsz = task.get_batch_size(batch)
                if bsz is not None:
                    total_bsz = bsz if total_bsz is None else total_bsz + bsz
                with self.step_context("forward"):
                    loss = task_model(batch, state)
                    gen_loss, dis_loss = task.separate_losses(loss)
                with self.step_context("get_single_loss"):
                    gen_single_loss, gen_loss_names = task.get_single_loss(gen_loss)
                    dis_single_loss, dis_loss_names = task.get_single_loss(dis_loss)
                with self.step_context("backward"):
                    gen_params, dis_params = params
                    self.backward_grads(task_model, dis_single_loss, dis_loss_names, True, dis_params)
                    self.backward_grads(task_model, gen_single_loss, gen_loss_names, False, gen_params)
                with self.step_context("log_losses"):
                    self.log_mp_scale()
                    for single_loss, loss_names in (
                        (dis_single_loss, dis_loss_names),
                        (gen_single_loss, gen_loss_names),
                    ):
                        single_loss_detached = single_loss.detach()
                        for i, name in enumerate(loss_names):
                            new_loss = single_loss_detached[i]
                            if name in losses:
                                old_loss, count = losses[name]
                                losses[name] = (old_loss + new_loss, count + 1)
                            else:
                                losses[name] = (new_loss, 1)
                num_steps += 1
        with self.step_context("log_losses"):
            loss_dict = {k: value / count for k, (value, count) in losses.items()}
            task.log_loss_dict(loss_dict, state)
        with self.step_context("step"):
            if isinstance(optim, Collection):
                for optim_i in optim:
                    self.step_optimizer(model, optim_i, num_steps)
            else:
                self.step_optimizer(model, optim, num_steps)
            if isinstance(lr_sched, Collection):
                for i, lr_sched_i in enumerate(lr_sched):
                    lr_sched_i.step(state)
                    self.logger.log_scalar(f"lr_scale_{i}", lr_sched_i.lr_scale, namespace="📉 optim")
            else:
                lr_sched.step(state)
                self.logger.log_scalar("lr_scale", lr_sched.lr_scale, namespace="📉 optim")
        with self.step_context("write_logs"), self.autocast_context:
            self.write_logs(task, model, state)
        with self.step_context("update_state"):
            state.num_steps += 1
            state.num_epoch_steps += 1
            if total_bsz is not None:
                state.num_samples += total_bsz
                state.num_epoch_samples += total_bsz
        return loss_dict

    def get_params(self, task_model: nn.Module) -> tuple[list[nn.Parameter], list[nn.Parameter]]:
        gen_params: list[nn.Parameter] = []
        dis_params: list[nn.Parameter] = []
        other_params: list[str] = []

        # Separates the parameters by searching for "generator" and
        # "discriminator" in the name. This is a bit hacky, but because these
        # names are set internally in the framework we can be pretty sure that
        # this won't break for downstream users.
        for name, param in task_model.named_parameters():
            g, d = name.find("generator"), name.find("discriminator")
            if g == -1 and d == -1:
                other_params.append(name)
            elif g == -1:
                dis_params.append(param)
            elif d == -1:
                gen_params.append(param)
            elif g < d:
                gen_params.append(param)
            else:
                dis_params.append(param)

        if other_params:
            other_str = ", ".join(other_params[:5])
            if len(other_params) > 5:
                other_str += f" (plus {len(other_params) - 5} more)"
            logger.warning("Found %d parameters not in generator or discriminator: %s", len(other_params), other_str)

        return gen_params, dis_params

    def train(
        self,
        model: GenerativeAdversarialNetworkModelT,
        task: GenerativeAdversarialNetworkTaskT,
        optimizer: BaseOptimizer,
        lr_scheduler: BaseLRScheduler,
    ) -> None:
        """Runs the training loop.

        Args:
            model: The model to train.
            task: The task to train on.
            optimizer: The optimizer to use.
            lr_scheduler: The learning rate scheduler to use.
        """
        if not isinstance(model, GenerativeAdversarialNetworkModel):
            raise ValueError(f"Expected model to be a GenerativeAdversarialNetworkModel, got {type(model)}")
        if not isinstance(task, (GenerativeAdversarialNetworkTask, GenerativeAdversarialNetworkRoundRobinTask)):
            raise ValueError(f"Expected task to be a GenerativeAdversarialNetworkTask, got {type(task)}")

        self._init_environment()

        with Timer("compiling model"):
            model = self._compile_model(model)

        with Timer("compiling training step"):
            train_step = self._compile_func(self.gan_train_step)

        with Timer("compiling validation step"):
            val_step = self._compile_func(self.val_step)

        with Timer("building task model"):
            task_model = self._get_task_model(task, model)

        with Timer("separating parameters"):
            gen_params, dis_params = self.get_params(task_model)

        gen_optim, gen_lr_sched = self._get_optim_and_lr_sched(model.generator, optimizer, lr_scheduler, True)
        dis_optim, dis_lr_sched = self._get_optim_and_lr_sched(model.discriminator, optimizer, lr_scheduler, False)
        optims = {"gen": gen_optim, "dis": dis_optim}
        lr_scheds = {"gen": gen_lr_sched, "dis": dis_lr_sched}
        state = self._get_state(task, model, optims, lr_scheds)

        def on_exit(signum: int, _: FrameType | None) -> None:
            sig = signal.Signals(signum)
            self.on_exit(sig, state, task, model, optims, lr_scheds)

        # Handle user-defined interrupts.
        signal.signal(signal.SIGUSR1, on_exit)

        # Gets the datasets.
        with Timer("getting datasets", 0.1):
            train_ds = task.get_dataset("train")
            valid_ds = task.get_dataset("valid")

        # Gets the dataloaders.
        with Timer("getting dataloaders", 0.1):
            train_dl = task.get_dataloader(train_ds, "train")
            valid_dl = task.get_dataloader(valid_ds, "valid")

        # Gets the prefetchers.
        with Timer("getting prefetchers", 0.1):
            train_pf = self._device.get_prefetcher(train_dl)
            valid_pf = self._device.get_prefetcher(valid_dl)
            valid_pf_iter = iter(InfinitePrefetcher(valid_pf))

        self.on_training_start(state, task, model, optims, lr_scheds)

        try:
            with contextlib.ExitStack() as ctx:
                profile = self.get_profile()
                if profile is not None:
                    ctx.enter_context(profile)

                while True:
                    with self.step_context("on_epoch_start"):
                        self.on_epoch_start(state, task, model, optims, lr_scheds)

                    def batch_splitter() -> Iterator[Batch]:
                        num_chunks = self.get_batch_chunks(state)
                        for batch in train_pf:
                            yield from recursive_chunk(batch, num_chunks, dim=self.config.batch_dim)

                    train_pf_iter: Iterator = batch_splitter()

                    def batch_iterator() -> Iterator[Batch]:
                        try:
                            yield next(train_pf_iter)
                        except StopIteration:
                            raise EpochDoneError

                        for _ in range(self.get_batches_per_step(state) - 1):
                            try:
                                yield next(train_pf_iter)
                            except StopIteration:
                                pass

                    while True:
                        if self.should_validate(state):
                            self._log_prefetcher_stats(valid_pf)

                            with namespace_context(self._logging_key(task, state, "valid")):
                                val_step(
                                    task_model=task_model,
                                    batch=next(valid_pf_iter),
                                    state=state,
                                    task=task,
                                    model=model,
                                )

                        self._log_prefetcher_stats(train_pf)

                        if task.is_training_over(state):
                            raise TrainingFinishedError

                        with self.step_context("on_step_start"):
                            self.on_step_start(state, task, model, optims, lr_scheds)

                        try:
                            if isinstance(task, GenerativeAdversarialNetworkRoundRobinTask):
                                is_gen = task.is_generator_step(state, "train")
                                optim = gen_optim if is_gen else dis_optim
                                lr_sched = gen_lr_sched if is_gen else dis_lr_sched

                                with namespace_context(self._logging_key(task, state, "train")):
                                    loss_dict = train_step(
                                        task_model=task_model,
                                        params=(gen_params, dis_params),
                                        batches=batch_iterator(),
                                        state=state,
                                        task=task,
                                        model=model,
                                        optim=optim,
                                        lr_sched=lr_sched,
                                    )

                            else:
                                loss_dict = train_step(
                                    task_model=task_model,
                                    params=(gen_params, dis_params),
                                    batches=batch_iterator(),
                                    state=state,
                                    task=task,
                                    model=model,
                                    optim=(gen_optim, dis_optim),
                                    lr_sched=(gen_lr_sched, dis_lr_sched),
                                )

                        except EpochDoneError:
                            break

                        if self.should_checkpoint(state):
                            self.save_checkpoint(state, task, model, optims, lr_scheds)

                        if profile is not None:
                            profile.step()

                        with self.step_context("on_step_end"):
                            self.on_step_end(state, loss_dict, task, model, optims, lr_scheds)

                    with self.step_context("on_epoch_end"):
                        self.on_epoch_end(state, task, model, optims, lr_scheds)

        except TrainingFinishedError:
            self.save_checkpoint(state, task, model, optims, lr_scheds)
            logger.info(
                "Finished training after %d epochs, %d steps, %d samples",
                state.num_epochs,
                state.num_steps,
                state.num_samples,
            )

        except Exception:
            logger.exception("Caught exception during training loop for %s", self.config_path)

        finally:
            self.on_training_end(state, task, model, optims, lr_scheds)

    def _get_optim_and_lr_sched(  # type: ignore[override]
        self,
        task_model: nn.Module,
        optimizer: BaseOptimizer,
        lr_scheduler: BaseLRScheduler,
        is_gen: bool,
    ) -> tuple[Optimizer, SchedulerAdapter]:
        if isinstance(optimizer, GenerativeAdversarialNetworkOptimizer):
            optimizer = optimizer.generator if is_gen else optimizer.discriminator
        if isinstance(lr_scheduler, GenerativeAdversarialNetworkLRScheduler):
            lr_scheduler = lr_scheduler.generator if is_gen else lr_scheduler.discriminator
        return super()._get_optim_and_lr_sched(task_model, optimizer, lr_scheduler)
