import dataclasses
import logging
import pathlib
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Save an offline version of a pytorch model. torch.jit.save()

    The input model must not make any calls to native python functions.

    Config:
        path (Path): Path to save the model to.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module

    @dataclasses.dataclass
    class Config:
        path: pathlib.Path

    def execute(self, inputs):
        logger.info(f"Saving model to {self.config.path}")
        torch.jit.save(inputs.model, self.config.path)
        return self.Outputs()
