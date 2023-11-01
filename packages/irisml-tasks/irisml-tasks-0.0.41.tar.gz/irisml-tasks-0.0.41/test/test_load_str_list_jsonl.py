import pathlib
import tempfile
import unittest

from irisml.tasks.load_str_list_jsonl import Task


class TestLoadStrListJsonl(unittest.TestCase):
    def test_simple(self):
        with tempfile.NamedTemporaryFile() as f:
            path = pathlib.Path(f.name)
            path.write_text('{"key": "value1"}\n{"key": "value2"}\n')
            outputs = Task(Task.Config(path=path, key_name="key")).execute(Task.Inputs())
            self.assertEqual(outputs.data, ['value1', 'value2'])
