import dataclasses
import pickle
import pathlib
import typing
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Load a list of tensors from file."""
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        path: pathlib.Path

    @dataclasses.dataclass
    class Outputs:
        tensor_list: typing.List[torch.Tensor]

    def execute(self, inputs):
        data = pickle.loads(inputs.path.read_bytes())
        if not isinstance(data, list):
            raise TypeError(f"Loaded data is type {type(data)}, expected list")
        for i, t in enumerate(data):
            if not torch.is_tensor(t):
                raise TypeError(f"item {i} in the list is type {type(t)}, expected tensor")
        return self.Outputs(data)

    def dry_run(self, inputs):
        return self.execute(inputs)
