import dataclasses
import typing
import irisml.core


class Task(irisml.core.TaskBase):
    """Split string to a list of strings."""
    VERSION = '0.0.1'

    @dataclasses.dataclass
    class Inputs:
        string: str

    @dataclasses.dataclass
    class Config:
        delimiter: str = ','

    @dataclasses.dataclass
    class Outputs:
        strings: typing.List[str]

    def execute(self, inputs):
        return self.Outputs([s.strip() for s in inputs.string.split(self.config.delimiter)])
