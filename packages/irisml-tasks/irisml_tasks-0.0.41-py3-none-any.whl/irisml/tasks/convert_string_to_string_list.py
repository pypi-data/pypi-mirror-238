import dataclasses
import typing
import irisml.core


class Task(irisml.core.TaskBase):
    """Convert a string to a list of strings."""
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        string: str

    @dataclasses.dataclass
    class Outputs:
        strings: typing.List[str]

    def execute(self, inputs):
        return self.Outputs([inputs.string])

    def dry_run(self, inputs):
        return self.execute(inputs)
