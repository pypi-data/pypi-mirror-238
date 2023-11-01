import dataclasses
import logging
import random
import irisml.core
import torch.utils.data
import PIL.Image
import PIL.ImageColor

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Generate a fake visual question answering dataset.

    A generated dataset returns ((question: str, image: PIL.Image), answer: str) pairs.

    Images are 224x224 pixels, and are filled with a single color. The color is chosen randomly from the list of
    colors in PIL.ImageColor.colormap, and the list is shuffled with the given random seed.

    Config:
        num_images (int): Number of images to generate. Default: 100.
        question (str): Question to ask about each image. Default: 'What is the color of this image? <|image|>'.
        random_seed (int): Random seed. Default: 0.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        num_images: int = 100
        question: str = 'What is the color of this image? <|image|>'
        random_seed: int = 0

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset

    class FakeDataset(torch.utils.data.Dataset):
        def __init__(self, num_images, random_seed, question):
            color_names = list(PIL.ImageColor.colormap.keys())
            rng = random.Random(random_seed)
            rng.shuffle(color_names)
            logger.debug(f"Generated color names: {color_names} (random_seed={random_seed})")

            self._color_names = color_names
            self._num_images = num_images
            self._question = question

        def __len__(self):
            return self._num_images

        def __getitem__(self, index):
            if index >= self._num_images:
                raise IndexError(f"Index out of range: {index} >= {self._num_images}")

            color_name = self._color_names[index % len(self._color_names)]
            image = PIL.Image.new('RGB', (224, 224), color=color_name)
            return (self._question, image), color_name

    def execute(self, inputs):
        dataset = Task.FakeDataset(self.config.num_images, self.config.random_seed, self.config.question)
        return self.Outputs(dataset)

    def dry_run(self, inputs):
        return self.execute(inputs)
