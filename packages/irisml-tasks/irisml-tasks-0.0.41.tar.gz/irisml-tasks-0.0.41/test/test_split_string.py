import unittest
from irisml.tasks.split_string import Task


class TestSplitString(unittest.TestCase):
    def test_simple(self):
        output = Task(Task.Config()).execute(Task.Inputs('a,b,c'))
        self.assertEqual(output.strings, ['a', 'b', 'c'])

        output = Task(Task.Config()).execute(Task.Inputs('a, b,   c'))
        self.assertEqual(output.strings, ['a', 'b', 'c'])

    def test_other_delimiter(self):
        output = Task(Task.Config(delimiter='-')).execute(Task.Inputs('a-b-c'))
        self.assertEqual(output.strings, ['a', 'b', 'c'])
