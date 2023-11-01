import dataclasses
import logging
import typing
import torch
import irisml.core


PLACEHOLDER = '<|placeholder|>'
INDEX_PLACEHOLDER = '<|index|>'
logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Make a list of prompts from a template and a list of strings.

    The template should contain exactly one instance of "<|placeholder|>".
    The sub_template should contain exactly one instance of "<|placeholder|>". It may also contain "<|index|>".

    `indices` is a list of lists of indices into `strings`. Each index list will be used to fill in the sub_template.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        strings: typing.List[str]
        indices: typing.List[torch.Tensor] = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class Config:
        template: str
        sub_template: str = PLACEHOLDER
        delimiter: str = ', '

    @dataclasses.dataclass
    class Outputs:
        prompts: typing.List[str]

    def execute(self, inputs):
        if PLACEHOLDER not in self.config.template:
            raise ValueError(f'"{PLACEHOLDER}" not found in template')
        if PLACEHOLDER not in self.config.sub_template:
            raise ValueError(f'"{PLACEHOLDER}" not found in sub_template')
        if not all(isinstance(i, torch.Tensor) for i in inputs.indices):
            raise ValueError("indices must be a list of torch.Tensor")

        strings = [self.config.sub_template.replace(PLACEHOLDER, s).replace(INDEX_PLACEHOLDER, str(i)) for i, s in enumerate(inputs.strings)]

        prompts = []
        for index, indices in enumerate(inputs.indices):
            prompt = self.config.template.replace(PLACEHOLDER, self.config.delimiter.join([strings[i] for i in indices]))
            prompts.append(prompt)
            logger.info(f"Prompt {index}: {repr(prompt)}")

        return self.Outputs(prompts)

    def dry_run(self, inputs):
        return self.execute(inputs)
