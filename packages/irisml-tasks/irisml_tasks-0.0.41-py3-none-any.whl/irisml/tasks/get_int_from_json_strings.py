import collections
import dataclasses
import json
import logging
import re
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Get an integer from a JSON string.

    This task takes a list of JSON strings and returns a list of integers. The
    JSON strings are expected to be dictionaries with a key that matches the
    `key_name` config value. If the JSON string cannot be decoded or the key
    cannot be found, the value -1 is returned.

    This task ignores any non-JSON text before or after the JSON string.

    If single quotes are used in the JSON string, they are replaced with double
    quotes before decoding.

    Config:
        key_name (str): The key to look for in the JSON string.
        voting (bool): If True, the most common value is returned. If False, the first value is returned.
    """
    VERSION = '1.1.2'

    @dataclasses.dataclass
    class Inputs:
        json_strings: typing.List[str]

    @dataclasses.dataclass
    class Config:
        key_name: str
        voting: bool = False

    @dataclasses.dataclass
    class Outputs:
        tensor: torch.Tensor

    def execute(self, inputs):
        ints = []
        for i, json_string in enumerate(inputs.json_strings):
            value = -1
            try:
                values = self._get_ints_from_json(json_string)
                if self.config.voting:
                    c = collections.Counter(values)
                    value = collections.Counter(values).most_common(1)[0][0]
                    if len(c) > 1:
                        logger.debug(f"Index {i}: Picked {value} from {values}")
                else:
                    value = values[0]

            except Exception as e:
                logger.warning(f"Index {i}: {repr(e)}. json: {repr(json_string)}")

            logger.info(f"Index {i}: Found value {value} in json: {repr(json_string)}")
            ints.append(value)

        int_tensor = torch.tensor(ints)
        logger.info(f"Returning {int_tensor.shape} tensor of ints")
        return self.Outputs(int_tensor)

    def dry_run(self, inputs):
        return self.execute(inputs)

    def _get_ints_from_json(self, json_str):
        index = 0
        values = []

        while index < len(json_str):
            json_dict, end_index = self._decode_json(json_str[index:])
            if json_dict is None:
                break
            assert end_index > 0
            index += end_index

            if self.config.key_name not in json_dict:
                logger.warning(f"Key {self.config.key_name} not found in JSON string: {repr(json_str[index:])}")
                continue

            if not isinstance(json_dict[self.config.key_name], int):
                logger.warning(f"Value {json_dict[self.config.key_name]} is not an integer")
                continue

            values.append(json_dict[self.config.key_name])

        if not values:
            logger.warning("All attempts to decode JSON string failed. Trying to extract values without decoding.")
            values = self._try_extract_values_directly(json_str, self.config.key_name)
            if not values:
                raise ValueError("No values found in JSON string.")

        return values

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
            return None, len(json_str)

        return None, len(json_str)

    @staticmethod
    def _try_extract_values_directly(json_str, key_name):
        matches = re.findall(rf'"{key_name}"\s*:\s*(\-?\d+)', json_str)
        return [int(m) for m in matches]
