import unittest
import pickle
import pathlib
import tempfile

import torch
from irisml.tasks.load_tensor_list import Task


class TestLoadTensorList(unittest.TestCase):
    def test_tensor_list(self):
        tensor_list = [torch.Tensor([0, 1, 0, 0, 1, 1]), torch.Tensor([[1, 1, 0, 0, 1, 1]])]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir) / 'test.pth'
            temp_file.write_bytes(pickle.dumps(tensor_list))
            data = Task(Task.Config()).execute(Task.Inputs(path=temp_file)).tensor_list
            self.assertTrue(all([torch.equal(a, b) for a, b in zip(data, tensor_list)]))
