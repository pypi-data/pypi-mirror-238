import unittest
import PIL.Image
import torch.utils.data
from irisml.tasks.get_fake_visual_question_answering_dataset import Task


class TestGetFakeImageClassificationDataset(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(num_images=100)).execute(Task.Inputs())
        dataset = outputs.dataset
        self.assertIsInstance(dataset, torch.utils.data.Dataset)
        self.assertEqual(len(dataset), 100)
        self.assertEqual(len(dataset[0]), 2)
        self.assertIsInstance(dataset[0][0][0], str)
        self.assertIsInstance(dataset[0][0][1], PIL.Image.Image)
        self.assertIsInstance(dataset[0][1], str)
