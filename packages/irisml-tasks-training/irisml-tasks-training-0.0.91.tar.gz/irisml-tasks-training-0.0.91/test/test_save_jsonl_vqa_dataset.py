import base64
import json
import pathlib
import tempfile
import unittest
import PIL.Image
import torch.utils.data
from irisml.tasks.save_jsonl_vqa_dataset import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


class TestSaveJsonlVqaDataset(unittest.TestCase):
    def test_simple(self):
        dataset = FakeDataset([
            (('question1', PIL.Image.new('RGB', (32, 32))), 'answer1'),
            (('question2', PIL.Image.new('RGB', (32, 32))), 'answer2')
            ])

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir) / 'new_dir' / 'test.jsonl'
            outputs = Task(Task.Config(temp_file)).execute(Task.Inputs(dataset=dataset))
            self.assertIsNotNone(outputs)

            saved = [json.loads(line) for line in temp_file.read_text().splitlines()]
            self.assertEqual(len(saved), 2)
            self.assertEqual(saved[0]['id'], 1)
            self.assertEqual(saved[0]['question'], 'question1')
            self.assertEqual(saved[0]['answer'], 'answer1')
            self.assertTrue(base64.b64decode(saved[0]['image']))

            self.assertEqual(saved[1]['id'], 2)
            self.assertEqual(saved[1]['question'], 'question2')
            self.assertEqual(saved[1]['answer'], 'answer2')
            self.assertTrue(base64.b64decode(saved[0]['image']))
