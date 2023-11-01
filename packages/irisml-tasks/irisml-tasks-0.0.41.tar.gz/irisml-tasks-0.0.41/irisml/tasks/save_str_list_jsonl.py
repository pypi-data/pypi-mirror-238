import dataclasses
import json
import logging
import pathlib
import typing
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Save a list of strings to a JSONL file.

    Config:
        path (Path): Path to the output file.
        key_name (str): Name of the key to use for each item in the list.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        data: typing.List[str]

    @dataclasses.dataclass
    class Config:
        path: pathlib.Path
        key_name: str

    def execute(self, inputs):
        self.config.path.parent.mkdir(parents=True, exist_ok=True)
        with self.config.path.open('w') as f:
            for item in inputs.data:
                json.dump({self.config.key_name: item}, f)
                f.write('\n')

        logger.info(f"Saved {len(inputs.data)} items to {self.config.path}")
