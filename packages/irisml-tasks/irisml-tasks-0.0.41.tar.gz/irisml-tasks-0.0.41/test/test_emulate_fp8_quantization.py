import unittest
import torch
from irisml.tasks.emulate_fp8_quantization import Task


class TestEmulateFp8Quantization(unittest.TestCase):
    def test_allclose(self):
        inputs = (torch.rand(100) + 2 ** -6) * 10
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=inputs)).tensor
        self.assertTrue(torch.allclose(inputs, outputs, rtol=2 ** -2))

        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=-inputs)).tensor
        self.assertTrue(torch.allclose(-inputs, outputs, rtol=2 ** -2))

    def test_subnormal_numbers(self):
        inputs = (torch.rand(100) - 0.5) * (2 ** -6)
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=inputs)).tensor
        self.assertTrue(torch.equal(outputs, torch.zeros_like(outputs)))

    def test_exact_numbers(self):
        inputs = torch.tensor([0.25, 0.5, 1.0, 2.0, -0.25, -0.5, -1.0, -2.0])
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=inputs)).tensor
        self.assertTrue(torch.equal(outputs, inputs))

    def test_special_values(self):
        inputs = torch.tensor([0.0, 1.0, -1.0, float('inf'), float('-inf')])
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=inputs)).tensor
        self.assertTrue(torch.equal(outputs, inputs))

        inputs = torch.tensor([float('nan')])
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=inputs)).tensor
        self.assertTrue(torch.isnan(outputs).all())

    def test_out_of_range(self):
        inputs = torch.tensor([2 ** 16, -2 ** 16, 2 ** 32, -2 ** 32], dtype=torch.float32)
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=inputs)).tensor
        self.assertTrue(outputs.tolist(), [128, -128, 128, -128])

    def test_non_float(self):
        inputs = torch.tensor([1, 2, 3])
        with self.assertRaises(ValueError):
            Task(Task.Config()).execute(Task.Inputs(tensor=inputs))

    def test_shape(self):
        inputs = torch.rand(1, 3, 8, 8)
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=inputs)).tensor
        self.assertEqual(outputs.shape, inputs.shape)
