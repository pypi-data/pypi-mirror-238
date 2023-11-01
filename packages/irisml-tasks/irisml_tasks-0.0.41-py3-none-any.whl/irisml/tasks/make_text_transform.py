import dataclasses
import typing
import irisml.core


class Task(irisml.core.TaskBase):
    """Make a text transform function.

    This task creates a text transform function that replaces "{}" in a template with a given string.

    Config:
        template (str): The template to use for the text transform function. Must contain "{}".
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        template: str

    @dataclasses.dataclass
    class Outputs:
        transform: typing.Callable[[str], str]

    def execute(self, inputs):
        return self.Outputs(TextTransform(self.config.template))

    def dry_run(self, inputs):
        return self.execute(inputs)


class TextTransform:
    def __init__(self, template):
        self._template = template
        if '{}' not in self._template:
            raise ValueError('Template must contain "{}"')

    def __call__(self, text):
        return self._template.replace('{}', text)
