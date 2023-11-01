import dataclasses
import logging
import irisml.core


logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Join two strings to one string."""
    VERSION = '0.0.1'

    @dataclasses.dataclass
    class Inputs:
        string1: str = ''
        string2: str = ''

    @dataclasses.dataclass
    class Config:
        delimiter: str = ' '

    @dataclasses.dataclass
    class Outputs:
        string: str

    def execute(self, inputs):
        if not inputs.string1 and not inputs.string2:
            raise ValueError("string1 or string2 must be non-empty!")
        elif not inputs.string1 or not inputs.string2:
            return self.Outputs(inputs.string1 + inputs.string2)
        else:
            string = inputs.string1 + self.config.delimiter + inputs.string2
            logging.info(f'Joined string: {string}')
            return self.Outputs(string)

    def dry_run(self, inputs):
        return self.execute(inputs)
