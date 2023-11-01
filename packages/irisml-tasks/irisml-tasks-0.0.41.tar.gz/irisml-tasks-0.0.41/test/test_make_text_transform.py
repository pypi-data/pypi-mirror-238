import unittest
from irisml.tasks.make_text_transform import Task


class TestMakeTextTransform(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config('Hello, {}!')).execute(Task.Inputs())
        self.assertEqual(outputs.transform('world'), 'Hello, world!')

    def test_invalid_template(self):
        with self.assertRaises(ValueError):
            Task(Task.Config('Hello, world!')).execute(Task.Inputs())
