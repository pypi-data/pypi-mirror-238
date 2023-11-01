import unittest
import torch
from irisml.tasks.convert_detection_to_multilabel import Task


class TestConvertDetectionToMultilabel(unittest.TestCase):
    def test_simple(self):
        box = [0, 0, 0.5, 0.5]
        # class_ids: [0,1], [0,1,2]
        detections = [torch.tensor([[0, *box], [1, *box], [0, *box]]),
                      torch.tensor([[1, *box], [0, *box], [2, *box]])]
        result = Task(Task.Config()).execute(Task.Inputs(detections, num_classes=3))
        self.assertTrue(torch.equal(result.results, torch.tensor([[1, 1, 0], [1, 1, 1]])))

    def test_logits(self):
        box = [0, 0, 0.5, 0.5]
        detections_with_score = [torch.tensor([[0, 0.1, *box], [1, 0.9, *box], [0, 0.3, *box]]),
                                 torch.tensor([[1, 0.8, *box], [0, 0.3, *box], [2, 0.6, *box]])]
        result = Task(Task.Config()).execute(Task.Inputs(detections_with_score, num_classes=3))
        self.assertTrue(torch.equal(result.results, torch.tensor([[0.3, 0.9, 0.0], [0.3, 0.8, 0.6]])))
