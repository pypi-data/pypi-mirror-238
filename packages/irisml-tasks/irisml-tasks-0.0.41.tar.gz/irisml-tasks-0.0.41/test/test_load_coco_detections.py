import json
import pathlib
import tempfile
import unittest
import torch
from irisml.tasks.load_coco_detections import Task


class TestLoadCOCODetections(unittest.TestCase):
    def test_simple(self):
        with tempfile.NamedTemporaryFile() as f:
            filepath = pathlib.Path(f.name)

            # With score.
            detections = [
                {"image_id": 1, "category_id": 3, "bbox": [0, 0, 5, 5], "score": 0.4},
                {"image_id": 1, "category_id": 4, "bbox": [10, 10, 20, 20], "score": 0.5},
                {"image_id": 3, "category_id": 1, "bbox": [0, 0, 2, 2], "score": 0.2}
            ]

            filepath.write_text(json.dumps(detections))
            outputs = Task(Task.Config(filepath)).execute(Task.Inputs())
            self.assertTrue(torch.equal(outputs.detections[0], torch.tensor([[2, 0.4, 0, 0, 5, 5], [3, 0.5, 10, 10, 30, 30]])))
            self.assertTrue(torch.equal(outputs.detections[1], torch.empty((0, 6))))
            self.assertTrue(torch.equal(outputs.detections[2], torch.tensor([[0, 0.2, 0, 0, 2, 2]])))

            # Without score.
            detections = [
                {"image_id": 1, "category_id": 3, "bbox": [1, 2, 4, 5]},
                {"image_id": 1, "category_id": 4, "bbox": [10, 10, 20, 20]},
                {"image_id": 3, "category_id": 1, "bbox": [0, 0, 2, 2]}
            ]
            filepath.write_text(json.dumps(detections))
            outputs = Task(Task.Config(filepath)).execute(Task.Inputs())
            self.assertTrue(torch.equal(outputs.detections[0], torch.tensor([[2, 1, 2, 5, 7], [3, 10, 10, 30, 30]])))
            self.assertTrue(torch.equal(outputs.detections[1], torch.empty((0, 5))))
            self.assertTrue(torch.equal(outputs.detections[2], torch.tensor([[0, 0, 0, 2, 2]])))
