import base64
import io
import pathlib
import tempfile
import unittest
import PIL.Image
from irisml.tasks.load_jsonl_vqa_dataset import Task


class TestLoadJsonlVqaDataset(unittest.TestCase):
    def test_load_jsonl_vqa_dataset(self):
        with tempfile.NamedTemporaryFile() as f:
            temp_file = pathlib.Path(f.name)
            base64_image = self._get_fake_base64_image()
            temp_file.write_text(f'{{"image": "{base64_image}", "question": "What is this?", "answer": "a cat"}}\n{{"image": "{base64_image}", "question": "What is that?", "answer": "a dog"}}')

            outputs = Task(Task.Config(temp_file)).execute(Task.Inputs())
            self.assertEqual(len(outputs.dataset), 2)
            self.assertIsInstance(outputs.dataset[0], tuple)
            self.assertIsInstance(outputs.dataset[0][0][0], str)
            self.assertIsInstance(outputs.dataset[0][0][1], PIL.Image.Image)
            self.assertIsInstance(outputs.dataset[0][1], str)
            self.assertEqual(outputs.dataset[0][1], 'a cat')

            self.assertEqual(outputs.dataset.get_targets(1), 'a dog')

    @staticmethod
    def _get_fake_base64_image():
        image = PIL.Image.new('RGB', (32, 32))
        with io.BytesIO() as f:
            image.save(f, format='PNG')
            return base64.b64encode(f.getvalue()).decode('utf-8')
