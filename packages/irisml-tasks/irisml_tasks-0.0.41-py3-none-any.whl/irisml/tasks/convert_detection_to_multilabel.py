import dataclasses
import typing
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Convert targets or predictions of object detection to multilabel.

    Input detections is a list of N tensors, each tensor is objects of an image, with each row containing class_id, (score), bbox coordinates.
    If score is provided, the maximum score of each class in an image is used as the multi-label logit for that class.
    Output is a tensor of shape (N, num_classes) wich each row being multi-hot vectors or logits (if score is provided).
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        detections: typing.List[torch.Tensor]
        num_classes: int

    @dataclasses.dataclass
    class Outputs:
        results: torch.Tensor

    def execute(self, inputs):
        detections = inputs.detections
        has_score = (torch.as_tensor(detections[0]).shape[1] == 6)
        results = torch.zeros((len(detections), inputs.num_classes))

        if has_score:
            for i, img_dts in enumerate(detections):
                dts = torch.as_tensor(img_dts)
                if dts.nelement() > 0:
                    sorted_dts = dts[dts[:, 1].sort().indices]  # for each class, the maximum score is used if there are multiple boxes.
                    results[i, sorted_dts[:, 0].to(int)] = sorted_dts[:, 1]
        else:
            for i, img_dts in enumerate(detections):
                dts = torch.as_tensor(img_dts)
                if dts.nelement() > 0:
                    results[i, dts[:, 0].to(int)] = 1
                results = results.to(int)

        return self.Outputs(results)

    def dry_run(self, inputs):
        return self.execute(inputs)
