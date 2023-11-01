import json
import pathlib
import tempfile
import unittest
from irisml.tasks.save_str_list_jsonl import Task


class TestSaveStrListJsonl(unittest.TestCase):
    def test_simple(self):
        with tempfile.NamedTemporaryFile() as f:
            temp_file = pathlib.Path(f.name)
            Task(Task.Config(path=temp_file, key_name='text')).execute(Task.Inputs(data=['a', 'b', 'c']))

            with open(temp_file) as f:
                lines = [json.loads(line) for line in f]
                self.assertEqual(lines, [{'text': 'a'}, {'text': 'b'}, {'text': 'c'}])
