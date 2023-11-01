import unittest
import torch
from irisml.tasks.make_prompt_list_with_strings import Task


class TestMakePromptListWithStrings(unittest.TestCase):
    def test_simple(self):
        strings = [f'str{i}' for i in range(10)]
        indices = [torch.tensor([0, 1, 2]), torch.tensor([3]), torch.tensor([6, 7, 8])]
        outputs = Task(Task.Config(template='Here is a list. <|placeholder|>')).execute(Task.Inputs(strings=strings, indices=indices))
        self.assertEqual(outputs.prompts, ['Here is a list. str0, str1, str2', 'Here is a list. str3', 'Here is a list. str6, str7, str8'])
