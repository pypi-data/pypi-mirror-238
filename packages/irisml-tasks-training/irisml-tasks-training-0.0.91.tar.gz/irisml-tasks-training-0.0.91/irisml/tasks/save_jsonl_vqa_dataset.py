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
    """Save a VQA dataset to a JSONL file.

    The dataset is expected to be a torch.utils.data.Dataset with elements of the form ((question, image), answer).
    The image is expected to be a PIL.Image.Image.
    The dataset is saved as a JSONL file, where each line is a JSON object with the following fields:
    - id: the index of the element in the dataset
    - question: the question
    - image: the image, encoded as a base64 string
    - answer: the answer

    Config:
        filepath (Path): the path to save the dataset to
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Config:
        filepath: pathlib.Path

    def execute(self, inputs):
        logger.info(f"Saving dataset to {self.config.filepath}. Dataset size: {len(inputs.dataset)}")

        self.config.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config.filepath, 'w') as file:
            for i, ((question, image), answer) in enumerate(inputs.dataset):
                if not isinstance(question, str) or not isinstance(answer, str):
                    raise ValueError(f"Expected question and answer to be strings, got {type(question)} and {type(answer)}")
                if not isinstance(image, PIL.Image.Image):
                    raise ValueError(f"Expected image to be PIL.Image.Image, got {type(image)}")

                with io.BytesIO() as f:
                    image.save(f, format='jpeg')
                    image_bytes = f.getvalue()

                data = {'id': i + 1, 'question': question, 'image': base64.b64encode(image_bytes).decode('ascii'), 'answer': answer}
                file.write(json.dumps(data) + '\n')

        logger.info(f"Saved dataset to {self.config.filepath}.")

        return self.Outputs()
