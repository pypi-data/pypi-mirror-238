import dataclasses
import logging
import typing
import irisml.core


PLACEHOLDER = '<|placeholder|>'
PLACEHOLDER2 = '<|placeholder2|>'
logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Make a prompt for each string.

    For example, if the template is "What is <|placeholder|>?" and the strings are ["a", "b", "c"], the prompts will be ["What is a?", "What is b?", "What is c?"].

    Optionally, you can provide a second list of strings. If you do, the template must contain "<|placeholder2|>" and the two lists must be the same length.
    The second list of strings will be used to replace "<|placeholder2|>" in the prompts.

    Config:
        template (str): The template to use for the prompt. Must contain "<|placeholder|>".
    """
    VERSION = '0.2.0'

    @dataclasses.dataclass
    class Inputs:
        strings: typing.List[str]
        strings2: typing.Optional[typing.List[str]] = None

    @dataclasses.dataclass
    class Config:
        template: str

    @dataclasses.dataclass
    class Outputs:
        prompts: typing.List[str]

    def execute(self, inputs):
        if PLACEHOLDER not in self.config.template:
            raise ValueError(f'"{PLACEHOLDER}" must be in template')

        if inputs.strings2 is not None:
            if len(inputs.strings) != len(inputs.strings2):
                raise ValueError('len(strings) != len(strings2)')
            if PLACEHOLDER2 not in self.config.template:
                raise ValueError(f'"{PLACEHOLDER2}" must be in template')
        else:
            if PLACEHOLDER2 in self.config.template:
                raise ValueError(f'strings2 must be provided if "{PLACEHOLDER2}" is in template')

        prompts = [self.config.template.replace(PLACEHOLDER, s) for s in inputs.strings]
        if inputs.strings2 is not None:
            prompts = [p.replace(PLACEHOLDER2, s) for p, s in zip(prompts, inputs.strings2)]

        for p in prompts:
            logger.info(f"Created a prompt: {p}")

        return self.Outputs(prompts=prompts)

    def dry_run(self, inputs):
        return self.execute(inputs)
