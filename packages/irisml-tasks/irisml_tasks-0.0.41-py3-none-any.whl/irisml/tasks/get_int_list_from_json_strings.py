import dataclasses
import json
import logging
import re
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Get a list of ints from a JSON string.

    This task takes a list of JSON strings and returns a list of lists of ints.
    Each JSON string must contain a key with the name specified in the
    configuration. The value of this key must be a list of ints.

    Config:
        key_name (str): The name of the key in the JSON string that contains the list of ints.
    """
    VERSION = '1.0.1'

    @dataclasses.dataclass
    class Inputs:
        json_strings: typing.List[str]

    @dataclasses.dataclass
    class Config:
        key_name: str

    @dataclasses.dataclass
    class Outputs:
        tensors: typing.List[torch.Tensor]

    def execute(self, inputs):
        tensors = []
        for i, json_string in enumerate(inputs.json_strings):
            values = []
            try:
                values = self._get_ints_from_json(json_string)
                logger.info(f"Index {i}: Found values {values} in json: {repr(json_string)}")
            except Exception as e:
                logger.warning(f"Index {i}: {repr(e)}. json: {repr(json_string)}")

            tensors.append(torch.tensor(values, dtype=torch.int64))

        assert len(tensors) == len(inputs.json_strings)
        return self.Outputs(tensors)

    def dry_run(self, inputs):
        return self.execute(inputs)

    def _get_ints_from_json(self, json_str):
        json_dict, _ = self._decode_json(json_str)
        if json_dict is None:
            raise ValueError("JSON string could not be decoded.")

        if self.config.key_name not in json_dict:
            raise ValueError(f"Key {self.config.key_name} not found in JSON string.")

        result = json_dict[self.config.key_name]
        if not isinstance(result, list) or not all(isinstance(x, int) for x in result):
            raise ValueError(f"Key {self.config.key_name} is not a list of ints.")

        return result

    @staticmethod
    def _decode_json(json_str):
        """Decode a JSON string.

        This method tries to decode a JSON string. If the string cannot be
        decoded, it tries to fix the string and decode it again. If the string
        still cannot be decoded, it returns None.

        Returns:
            A tuple of the decoded JSON object and the index of the end of the
            JSON string in the original string.
        """
        start = json_str.find('{')
        if start == -1:
            return None, len(json_str)

        try:
            return json.JSONDecoder().raw_decode(json_str[start:])
        except json.JSONDecodeError:
            pass

        try:
            # Try replacing a single quote with a double quote and vice versa.
            trans = str.maketrans('\'"', '"\'')
            return json.JSONDecoder().raw_decode(json_str.translate(trans)[start:])
        except json.JSONDecodeError:
            pass

        try:
            # Try replacing a single quote with a double quote
            return json.JSONDecoder().raw_decode(json_str.replace('\'', '"')[start:])
        except json.JSONDecodeError:
            pass

        try:
            # Try escaping a double quote in the JSON string
            pattern = r'([:\[,{]\s*)"(.*?)"(?=\s*[:,\]}])'

            def replace(match):
                return match.group(1) + '"' + match.group(2).replace('"', "'") + '"'
            fixed_json = re.sub(pattern, replace, json_str[start:])
            return json.JSONDecoder().raw_decode(fixed_json)
        except json.JSONDecodeError:
            pass

        return None, len(json_str)
