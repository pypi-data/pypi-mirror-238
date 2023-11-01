import json
import unittest
import torch
from irisml.tasks.get_int_list_from_json_strings import Task


class TestGetIntListFromJsonStrings(unittest.TestCase):
    def test_simple(self):
        json_strings = [json.dumps({'a': [1, 2, 3], 'b': [3, 4, 5]}), json.dumps({'a': [6, 7, 8], 'b': [9, 10, 11]})]
        outputs = Task(Task.Config(key_name='a')).execute(Task.Inputs(json_strings))
        self.assertTrue(torch.equal(outputs.tensors[0], torch.tensor([1, 2, 3])))
        self.assertTrue(torch.equal(outputs.tensors[1], torch.tensor([6, 7, 8])))

    def test_empty(self):
        json_strings = [json.dumps({'a': [], 'b': [3, 4, 5]}), json.dumps({'b': [9, 10, 11]})]
        outputs = Task(Task.Config(key_name='a')).execute(Task.Inputs(json_strings))
        self.assertTrue(torch.equal(outputs.tensors[0], torch.tensor([])))
        self.assertEqual(outputs.tensors[0].dtype, torch.int64)
        self.assertTrue(torch.equal(outputs.tensors[1], torch.tensor([])))
        self.assertEqual(outputs.tensors[1].dtype, torch.int64)
