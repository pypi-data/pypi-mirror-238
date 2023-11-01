import dataclasses
import logging
import random
import typing
import irisml.core
import torch
import PIL.Image

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Generate a fake image classification dataset.

    A generated dataset returns (image:PIL.Image, target:int)

    Config:
        num_images (int): Number of images to generate. Default: 100.
        num_classes (int): Number of classes to generate. Default: 10.
        random_seed (int): Random seed. Default: 0.
    """
    VERSION = '0.1.2'

    @dataclasses.dataclass
    class Config:
        num_images: int = 100
        num_classes: int = 10
        random_seed: int = 0

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset
        num_classes: int
        class_names: typing.List[str]

    class FakeDataset(torch.utils.data.Dataset):
        def __init__(self, image_labels: typing.List[int], colors: typing.List[typing.Tuple[int, int, int]]):
            self._image_labels = image_labels
            self._colors = colors

        def __len__(self):
            return len(self._image_labels)

        def __getitem__(self, index):
            image_class = self._image_labels[index]
            return self._generate_image(image_class), torch.tensor(image_class)

        def _generate_image(self, class_id):
            return PIL.Image.new('RGB', (224, 224), color=self._colors[class_id])

    def execute(self, inputs):
        if not self.config.num_images or not self.config.num_classes:
            raise ValueError(f"Invalid settings: num_images={self.config.num_images}, num_classes={self.config.num_classes}")

        if self.config.num_images < self.config.num_classes:
            logger.info(f"Some classes will be empty: num_images={self.config.num_images}, num_classes={self.config.num_classes}")

        num_images_per_class = [self.config.num_images // self.config.num_classes for _ in range(self.config.num_classes)]
        for i in range(self.config.num_images % self.config.num_classes):
            num_images_per_class[i] += 1

        assert sum(num_images_per_class) == self.config.num_images
        assert len(num_images_per_class) == self.config.num_classes

        labels = [c for c, x in enumerate(num_images_per_class) for _ in range(x)]
        rng = random.Random(self.config.random_seed)
        rng.shuffle(labels)

        colors = [(rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)) for _ in range(self.config.num_classes)]
        logger.debug(f"Generated labels: {colors}")
        dataset = Task.FakeDataset(labels, colors)
        class_names = [f'class_{i}' for i in range(self.config.num_classes)]
        return self.Outputs(dataset, num_classes=self.config.num_classes, class_names=class_names)

    def dry_run(self, inputs):
        return self.execute(inputs)
