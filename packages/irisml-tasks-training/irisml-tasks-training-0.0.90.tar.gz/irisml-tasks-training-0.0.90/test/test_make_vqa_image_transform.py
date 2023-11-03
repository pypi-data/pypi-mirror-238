import unittest
import PIL.Image
import torch
import torchvision.transforms
from irisml.tasks.make_vqa_image_transform import Task


class TestMakeVqaImageTransform(unittest.TestCase):
    def test_simple(self):
        image_transform = torchvision.transforms.ToTensor()

        def text_transform(text):
            return f'question: {text} answer:'

        outputs = Task(Task.Config()).execute(Task.Inputs(image_transform, text_transform))
        transform = outputs.transform

        transform_outputs = transform(('What is this?', PIL.Image.new('RGB', (32, 32))), 'R2D2')
        self.assertEqual(transform_outputs[0][0], 'question: What is this? answer:')
        self.assertIsInstance(transform_outputs[0][1], torch.Tensor)
        self.assertEqual(transform_outputs[1], 'R2D2')
