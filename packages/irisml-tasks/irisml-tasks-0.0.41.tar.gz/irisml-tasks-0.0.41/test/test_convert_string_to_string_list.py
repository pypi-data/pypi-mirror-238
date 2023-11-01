import unittest
from irisml.tasks.convert_string_to_string_list import Task


class TestConvertStringToStringList(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config()).execute(Task.Inputs(string='foo'))
        self.assertEqual(outputs.strings, ['foo'])
