import unittest
from irisml.tasks.get_key_and_int_list_from_json_string import Task


class TestGetKeyAndIntListFromJsonString(unittest.TestCase):
    def test_simple(self):
        json_string = '{"key1": [1, 2, 3], "key2": [4, 5, 6]}'
        outputs = Task(Task.Config()).execute(Task.Inputs(json_string))
        self.assertEqual(outputs.key_names, ['key1', 'key2'])
        self.assertEqual(outputs.ints[0].tolist(), [1, 2, 3])
        self.assertEqual(outputs.ints[1].tolist(), [4, 5, 6])
