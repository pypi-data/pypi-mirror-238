import unittest
import torch
from irisml.tasks.map_int_list import Task


class TestMapIntList(unittest.TestCase):
    def test_simple(self):
        mapping = [torch.tensor([0, 1, 2]), torch.tensor([3, 4, 5])]
        outputs = Task(Task.Config()).execute(Task.Inputs(data=torch.tensor([0, 1, 2, 3, 4, 5]), mapping=mapping))
        self.assertEqual(outputs.data.tolist(), [0, 0, 0, 1, 1, 1])
