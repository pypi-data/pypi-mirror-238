import pathlib
import tempfile
import unittest
import torch
from irisml.tasks.save_jit_model import Task


class TestSaveJitModel(unittest.TestCase):
    def test_simple(self):
        model = torch.nn.Linear(1, 1)
        jit_model = torch.jit.script(model)

        with tempfile.NamedTemporaryFile() as f:
            path = pathlib.Path(f.name)
            Task(Task.Config(path=path)).execute(Task.Inputs(jit_model))

            loaded_model = torch.jit.load(path)
        self.assertEqual(jit_model(torch.tensor([1.0])), loaded_model(torch.tensor([1.0])))
