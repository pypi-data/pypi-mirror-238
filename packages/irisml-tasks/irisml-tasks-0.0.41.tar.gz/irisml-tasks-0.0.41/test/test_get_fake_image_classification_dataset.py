import unittest
from irisml.tasks.get_fake_image_classification_dataset import Task


class TestGetFakeImageClassificationDataset(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(num_images=100, num_classes=10)).execute(Task.Inputs())
        self.assertEqual(len(outputs.dataset), 100)
        self.assertEqual(len(outputs.class_names), 10)
        class_set = set(int(x[1]) for x in outputs.dataset)
        self.assertEqual(len(class_set), 10)

    def test_empty_classes(self):
        outputs = Task(Task.Config(num_images=100, num_classes=200)).execute(Task.Inputs())
        self.assertEqual(len(outputs.dataset), 100)
        self.assertEqual(len(outputs.class_names), 200)
        class_set = set(int(x[1]) for x in outputs.dataset)
        self.assertEqual(len(class_set), 100)

    def test_random_seed(self):
        outputs1 = Task(Task.Config(num_images=100, num_classes=10, random_seed=1)).execute(Task.Inputs())
        outputs2 = Task(Task.Config(num_images=100, num_classes=10, random_seed=1)).execute(Task.Inputs())
        classes1 = [int(x[1]) for x in outputs1.dataset]
        classes2 = [int(x[1]) for x in outputs2.dataset]
        self.assertEqual(classes1, classes2)

        outputs3 = Task(Task.Config(num_images=100, num_classes=10, random_seed=2)).execute(Task.Inputs())
        classes3 = [int(x[1]) for x in outputs3.dataset]
        self.assertNotEqual(classes1, classes3)
