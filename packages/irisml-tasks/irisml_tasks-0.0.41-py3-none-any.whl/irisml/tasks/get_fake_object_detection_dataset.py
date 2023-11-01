import dataclasses
import logging
import random
import typing
import irisml.core
import torch
import PIL.Image
import PIL.ImageDraw

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Generate a fake object detection dataset.

    A generated dataset returns (image:PIL.Image, targets:List[Tensor[N, 5]])

    Configs:
        num_images (int): The number of images to make. Default: 100
        num_classes (int): The number of classes. Default: 10
        num_max_boxes (int): The max number of objects per image. Default: 10
        image_sizes ([(int, int), ...]): A list of candidate image sizes. Default: [(320, 320)]
        random_seed (int): The random seed. Default: 0
        targets ([[[float, float, float, float, float], ...], ...]): A list of targets. If not specified, random targets are generated. Default: None
    """
    VERSION = '0.1.5'

    @dataclasses.dataclass
    class Config:
        num_images: int = 100
        num_classes: int = 10
        num_max_boxes: int = 10  # The max number of objects per image.
        image_sizes: typing.List[typing.Tuple[int, int]] = dataclasses.field(default_factory=lambda: [(320, 320)])
        random_seed: int = 0
        targets: typing.Optional[typing.List[typing.List[typing.List[float]]]] = None

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset
        num_classes: int
        class_names: typing.List[str]

    class FakeDataset(torch.utils.data.Dataset):
        def __init__(self, targets: typing.List[torch.Tensor], colors: typing.List[typing.Tuple[int, int, int]], sizes: typing.List[typing.Tuple[int, int]]):
            assert len(targets) == len(sizes)
            self._targets = targets
            self._colors = colors
            self._sizes = sizes

        def __len__(self):
            return len(self._targets)

        def __getitem__(self, index):
            targets = self._targets[index]
            return self._generate_image(index, targets), targets

        def _generate_image(self, index, targets):
            size = self._sizes[index]
            image = PIL.Image.new('RGB', size)
            draw = PIL.ImageDraw.Draw(image)
            for t in targets:
                rect = (t[1] * size[0], t[2] * size[1], t[3] * size[0], t[4] * size[1])
                draw.rectangle(rect, fill=self._colors[int(t[0])])
            return image

    def execute(self, inputs):
        rng = random.Random(self.config.random_seed)

        def _random_box(image_width, image_height):
            # Make sure the bounding box size is at least 1 pixel.
            cx = rng.uniform(1 / image_width / 2, 1 - 1 / image_width / 2)
            cy = rng.uniform(1 / image_height / 2, 1 - 1 / image_height / 2)
            w = rng.uniform(1 / image_width, min(1 - cx, cx) * 2)
            h = rng.uniform(1 / image_height, min(1 - cy, cy) * 2)
            return [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]

        if not self.config.image_sizes:
            raise ValueError("Image sizes setting is empty.")

        for c in self.config.image_sizes:
            if len(c) != 2 or c[0] <= 0 or c[1] <= 0:
                raise ValueError(f"Invalid image size configs: {self.config.image_sizes}")

        sizes = rng.choices(self.config.image_sizes, k=self.config.num_images)

        if self.config.targets:
            targets = [torch.tensor(t) for t in self.config.targets]
            if len(targets) != self.config.num_images:
                raise ValueError(f"Invalid targets: {self.config.targets}")
        else:
            targets = [torch.tensor([[rng.randrange(self.config.num_classes), *_random_box(*sizes[i])] for _ in range(rng.randrange(self.config.num_max_boxes + 1))]).reshape(-1, 5)
                       for i in range(self.config.num_images)]

        colors = [(rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)) for _ in range(self.config.num_classes)]
        logger.debug(f"Generated labels: {colors}")

        dataset = Task.FakeDataset(targets, colors, sizes)
        class_names = [f'class_{i}' for i in range(self.config.num_classes)]
        return self.Outputs(dataset, num_classes=self.config.num_classes, class_names=class_names)

    def dry_run(self, inputs):
        return self.execute(inputs)
