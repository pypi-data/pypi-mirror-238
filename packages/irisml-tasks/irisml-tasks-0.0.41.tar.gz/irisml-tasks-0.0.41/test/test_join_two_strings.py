import unittest
from irisml.tasks.join_two_strings import Task


class TestJoinTwoStrings(unittest.TestCase):
    def test_simple(self):
        config = Task.Config(delimiter=' and ')
        outputs = Task(config).execute(Task.Inputs('1st str', '2nd str'))
        self.assertEqual(outputs.string, '1st str and 2nd str')

    def test_no_string2(self):
        first_string = '1st str'
        outputs = Task(Task.Config()).execute(Task.Inputs(first_string))
        self.assertEqual(outputs.string, first_string)

    def test_two_empty_strings(self):
        with self.assertRaises(ValueError):
            Task(Task.Config()).execute(Task.Inputs('', ''))
