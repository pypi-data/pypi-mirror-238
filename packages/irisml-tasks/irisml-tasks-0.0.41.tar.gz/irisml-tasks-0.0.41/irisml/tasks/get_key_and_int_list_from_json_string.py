import dataclasses
import json
import logging
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Parse a JSON string and return a list of keys and a list of lists of ints.

    The JSON string must be a dictionary with string keys and list of ints values.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        json_string: str

    @dataclasses.dataclass
    class Outputs:
        key_names: typing.List[str]
        ints: typing.List[torch.Tensor]

    def execute(self, inputs):
        try:
            json_dict = self._decode_json(inputs.json_string)
        except Exception as e:
            logger.error(f"Could not decode JSON string: {e}")
            raise

        key_names = []
        ints = []
        for key, value in json_dict.items():
            logger.debug(f"Key: {key}, Value: {value}")
            if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
                logger.warning(f"Skipping key {key} because it is not a list of ints")
                continue
            key_names.append(key)
            ints.append(torch.tensor(value))

        assert len(key_names) == len(ints)
        return self.Outputs(key_names=key_names, ints=ints)

    @staticmethod
    def _decode_json(json_str):
        start = json_str.find('{')
        if start == -1:
            raise ValueError("Could not find start of JSON string")

        try:
            decoded, _ = json.JSONDecoder().raw_decode(json_str[start:])
            return decoded
        except json.JSONDecodeError:
            pass

        try:
            # Try replacing a single quote with a double quote and vice versa.
            trans = str.maketrans('\'"', '"\'')
            decoded, _ = json.JSONDecoder().raw_decode(json_str.translate(trans)[start:])
            return decoded
        except json.JSONDecodeError:
            pass

        try:
            # Try replacing a single quote with a double quote
            decoded, _ = json.JSONDecoder().raw_decode(json_str.replace('\'', '"')[start:])
            return decoded
        except json.JSONDecodeError:
            raise
