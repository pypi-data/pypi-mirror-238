import dataclasses
from typing import Callable, Optional, Tuple
import PIL.Image
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Creates a transform function for VQA task.

    The input to the transform function is ((question, image), targets), where question is a string,
    image is a PIL image, and targets is a string. The output is ((question, image_tensor), targets),
    where question is a string, image_tensor is a tensor, and targets is a string.
    """
    VERSION = '1.0.0'

    @dataclasses.dataclass
    class Inputs:
        image_transform: Callable[[PIL.Image.Image], torch.Tensor]
        text_transform: Optional[Callable[[str], str]] = None

    @dataclasses.dataclass
    class Outputs:
        transform: Callable[[Tuple[str, PIL.Image.Image], str], Tuple[Tuple[str, torch.Tensor], str]]

    def execute(self, inputs):
        transform = VqaImageTransform(inputs.image_transform, inputs.text_transform)
        return self.Outputs(transform=transform)

    def dry_run(self, inputs):
        return self.execute(inputs)


class VqaImageTransform:
    def __init__(self, image_transform, text_transform):
        self._image_transform = image_transform
        self._text_transform = text_transform

    def __call__(self, inputs, targets):
        question, image = inputs
        assert isinstance(question, str)
        assert isinstance(image, PIL.Image.Image)
        image_tensor = self._image_transform(image)
        if self._text_transform:
            question = self._text_transform(question)
        return (question, image_tensor), targets
