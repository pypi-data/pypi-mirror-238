import base64
import dataclasses
import io
import json
import logging
import pathlib
import PIL.Image
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Load a VQA dataset from a jsonl file.

    JSONL dataset format: {image: <base64 encoded image>, question: str, answer: str}

    Loaded dataset format is a tuple of ((question: str, image: PIL.Image.Image), answer: str)

    Config:
        filepath (Path): Path to the jsonl file.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        filepath: pathlib.Path

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        dataset = VQADataset(self.config.filepath)
        return self.Outputs(dataset=dataset)

    def dry_run(self, inputs):
        return self.execute(inputs)


class VQADataset(torch.utils.data.Dataset):
    def __init__(self, filepath):
        super().__init__()
        self._images = []
        self._questions = []
        self._answers = []
        with open(filepath) as f:
            for line in f:
                if not line:
                    continue
                data = json.loads(line)
                self._images.append(base64.b64decode(data['image']))
                self._questions.append(data['question'])
                self._answers.append(data['answer'])

        assert len(self._images) == len(self._questions) == len(self._answers), f"Length mismatch: {len(self._images)} {len(self._questions)} {len(self._answers)}"
        logger.info(f"Loaded Dataset {filepath} with {len(self)} images")

    def __len__(self):
        return len(self._images)

    def __getitem__(self, index):
        image = PIL.Image.open(io.BytesIO(self._images[index]))
        return (self._questions[index], image), self._answers[index]

    def get_targets(self, index):
        return self._answers[index]
