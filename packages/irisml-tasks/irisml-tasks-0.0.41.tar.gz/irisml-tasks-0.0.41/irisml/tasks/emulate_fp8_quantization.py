import ctypes
import dataclasses
import logging
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Emulate FP8 quantization.

    Config:
        fp8_format ('e4m3' or 'e5m2'): FP8 format to use.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        tensor: torch.Tensor

    @dataclasses.dataclass
    class Config:
        fp8_format: typing.Literal['e4m3', 'e5m2'] = 'e4m3'

    @dataclasses.dataclass
    class Outputs:
        tensor: torch.Tensor

    def execute(self, inputs):
        if self.config.fp8_format == 'e4m3':
            fp8_num_fraction_bits = 3
            fp8_num_exponent_bits = 4
        elif self.config.fp8_format == 'e5m2':
            fp8_num_fraction_bits = 2
            fp8_num_exponent_bits = 5
        else:
            raise ValueError(f'Unknown fp8 format: {self.config.fp8_format}')

        if not torch.is_floating_point(inputs.tensor):
            raise ValueError(f'Expected floating point tensor, got {inputs.tensor.dtype}')

        fp32_num_fraction_bits = 23
        fp32_num_exponent_bits = 8

        fp8_min_exponent = -(1 << (fp8_num_exponent_bits - 1)) + 1
        fp8_max_exponent = (1 << (fp8_num_exponent_bits - 1)) - 1
        fp32_max_exponent = 127

        fp32_fraction_mask = (1 << fp32_num_fraction_bits) - 1
        fp32_exponent_mask = (1 << fp32_num_exponent_bits) - 1
        fp8_fraction_mask = (1 << fp8_num_fraction_bits) - 1

        # Convert to FP32 representation
        values = [ctypes.c_uint32.from_buffer(ctypes.c_float(t)).value for t in inputs.tensor.flatten().to(torch.float16)]

        # Parse FP32 representations
        fp8_fraction = [((v & fp32_fraction_mask) >> (fp32_num_fraction_bits - fp8_num_fraction_bits)) & fp8_fraction_mask for v in values]
        fp32_exponent = [(v >> fp32_num_fraction_bits) & fp32_exponent_mask for v in values]
        fp8_exponent = (torch.clamp(torch.tensor(fp32_exponent) - fp32_max_exponent, min=fp8_min_exponent, max=fp8_max_exponent) + fp8_max_exponent)
        sign_bits = [(v >> 31) & 1 for v in values]

        # Make FP8 values
        # fp8_values = [sign_bits[i] << 7 | fp8_exponent[i] << fp8_num_fraction_bits | fp8_fraction[i] for i in range(len(values))]

        new_fp32_exponent = [v - fp8_max_exponent + fp32_max_exponent for v in fp8_exponent]
        fp32_values = [sign_bits[i] << 31 | new_fp32_exponent[i] << fp32_num_fraction_bits | fp8_fraction[i] << (fp32_num_fraction_bits - fp8_num_fraction_bits) for i in range(len(values))]
        new_tensor = torch.tensor([ctypes.c_float.from_buffer(ctypes.c_uint32(int(v))).value for v in fp32_values], dtype=inputs.tensor.dtype).reshape(inputs.tensor.shape)

        # Overwrite the special values
        new_tensor[torch.isnan(inputs.tensor)] = float('nan')
        new_tensor[torch.isinf(inputs.tensor)] = float('inf')
        new_tensor[torch.isneginf(inputs.tensor)] = float('-inf')
        new_tensor[fp8_exponent.reshape(inputs.tensor.shape) == 0] = 0.0  # Subnormal numbers are considered zero.

        return self.Outputs(tensor=new_tensor)

    def dry_run(self, inputs):
        return self.execute(inputs)
