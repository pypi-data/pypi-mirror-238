import dataclasses
import json
import logging
import pathlib
import typing
from collections import defaultdict
import torch
import irisml.core


logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Load coco detections from a JSON to a list of tensors.

    The JSON file is a list of dictionaries, each dictionary should at least has key "image_id", "bbox" xywh normalized, "category_id". Optionally,
    the "score" field will also be loaded. All indices are supposed to start from 1.

    The output detections is a list of tensors, each tensor contains detections for an image, with shape (N, 5) or (N, 6), each row is [class (,score), x, y, x, y]. Absolute coordinates.
    If an image does not have prediction, N = 0.

    Config:
        filepath (Path): Path to the JSON file.
    """
    VERSION = '0.1.1'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        filepath: pathlib.Path

    @dataclasses.dataclass
    class Outputs:
        detections: typing.List[torch.Tensor]

    def execute(self, inputs):
        data = json.loads(self.config.filepath.read_text())
        if not isinstance(data, list):
            raise TypeError('JSON file should contain a list!')
        has_score = 'score' in data[0]
        n_col_tensor = 6 if has_score else 5

        pred_by_image = defaultdict(list)
        for pred in data:
            box_xyxy = self._convert_xywh_to_xyxy(pred['bbox'])
            pred_by_image[pred["image_id"] - 1].append([pred["category_id"] - 1, pred["score"], *box_xyxy] if has_score else [pred["category_id"] - 1, *box_xyxy])

        detections = [torch.tensor(pred_by_image[img_id]) if img_id in pred_by_image else torch.empty((0, n_col_tensor)) for img_id in range(max(pred_by_image.keys())+1)]
        logger.info(f"Loaded {len(data)} detections with score? {has_score}")
        return self.Outputs(detections=detections)

    def _convert_xywh_to_xyxy(self, box):
        return [box[0], box[1], box[0] + box[2], box[1] + box[3]]

    def dry_run(self, inputs):
        return self.execute(inputs)
