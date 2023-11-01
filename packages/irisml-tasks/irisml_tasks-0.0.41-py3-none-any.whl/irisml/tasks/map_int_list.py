import dataclasses
import typing
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Map a list of integers to a list of integers.

    The mapping is specified as a list of lists of integers. The mapping is
    applied to each element of the input list.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        data: torch.Tensor
        mapping: typing.List[torch.Tensor]

    @dataclasses.dataclass
    class Outputs:
        data: torch.Tensor

    def execute(self, inputs):
        if not isinstance(inputs.data, torch.Tensor):
            raise TypeError(f'Expected data to be of type torch.Tensor, got {type(inputs.data)}')
        if not all(isinstance(t, torch.Tensor) for t in inputs.mapping):
            raise TypeError(f'Expected mapping to be a list of torch.Tensor, got {[type(t) for t in inputs.mapping]}')

        if inputs.data.dim() != 1:
            raise ValueError(f'Expected data to be a 1D tensor, got {inputs.data.dim()}D')
        if not all(t.dim() == 1 for t in inputs.mapping):
            raise ValueError(f'Expected mapping to be a list of 1D tensors, got {[t.dim() for t in inputs.mapping]}')

        mapping = {int(v): i for i, t in enumerate(inputs.mapping) for v in t}
        return self.Outputs(data=torch.tensor([mapping[int(v)] for v in inputs.data]))

    def dry_run(self, inputs):
        return self.execute(inputs)
