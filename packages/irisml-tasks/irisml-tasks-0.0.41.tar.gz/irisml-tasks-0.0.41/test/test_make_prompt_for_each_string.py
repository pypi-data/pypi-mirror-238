import unittest
from irisml.tasks.make_prompt_for_each_string import Task


class TestMakePromptForEachString(unittest.TestCase):
    def test_simple(self):
        output = Task(Task.Config(template='What is <|placeholder|>?')).execute(Task.Inputs(strings=['a', 'b', 'c']))
        self.assertEqual(output.prompts, ['What is a?', 'What is b?', 'What is c?'])

    def test_two_strings(self):
        output = Task(Task.Config(template='What is <|placeholder|> (<|placeholder2|>)?')).execute(Task.Inputs(strings=['a', 'b', 'c'], strings2=['1', '2', '3']))
        self.assertEqual(output.prompts, ['What is a (1)?', 'What is b (2)?', 'What is c (3)?'])

    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            # missing placeholder2
            Task(Task.Config(template='What is <|placeholder|>?')).execute(Task.Inputs(strings=['a', 'b', 'c'], strings2=['1', '2', '3']))

        with self.assertRaises(ValueError):
            # missing strings2
            Task(Task.Config(template='What is <|placeholder|> (<|placeholder2|>)?')).execute(Task.Inputs(strings=['a', 'b', 'c']))

        with self.assertRaises(ValueError):
            # different number of strings and strings2.
            Task(Task.Config(template='What is <|placeholder|> (<|placeholder2|>)?')).execute(Task.Inputs(strings=['a', 'b', 'c'], strings2=['1', '2']))
