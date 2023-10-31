# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for extracting images from a video and converting annotations from a Label Studio video
object detection/tracking task to annotations for a object detection task.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from typing import Any, Dict, List

import cv2


class LabelStudioTrackingTaskConverter:  # pylint: disable=R0903
    """Class to handle conversion of a Label Studio tracking task to a object detection task."""

    @dataclass
    class __Annotation:
        """
        Class for storing an annotation.
        """

        x_min: float
        y_min: float
        width: float
        height: float
        rotation: float
        labels: List[str]

    @dataclass
    class __VideoSpecs:
        """
        Class for storing video attributes.
        """

        width: int
        height: int
        frame_count: int
        frame_rate: float

    def __init__(
        self,
        video_path: str,
        tracking_annotations_path: str,
        image_archive_path: str,
        annotations_path: str,
    ) -> None:
        """
        Create a LabelStudioTrackingTaskConverter

        Args:
            video_path: Path to the video.
            tracking_annotations_path: Path to the Label Studios tracking annotations.
            image_archive_path: Path to write the archive with separate images to.
            annotations_path: Path to write the annotations for the detection task to.

        Returns:
            The created LabelStudioTrackingTaskConverter instance
        """

        if not os.path.exists(video_path):
            raise ValueError(f"Path to video '{video_path}' does not exist.")
        if not os.path.exists(tracking_annotations_path):
            raise ValueError(
                f"Path to tracking annotations '{tracking_annotations_path}' does not exist."
            )

        self.video_path: str = video_path
        self.tracking_annotations_path: str = tracking_annotations_path
        self.image_archive_path: str = image_archive_path
        self.annotations_path: str = annotations_path

        self.video_specs = self._parse_video_specs()
        self.annotations: Dict[
            int, List[LabelStudioTrackingTaskConverter.__Annotation]
        ] = defaultdict(list)

    def run(self) -> None:
        """
        Extract images from video and convert annotations.
        """

        self._parse_tracking_annotations_file()
        self._extract_images()
        self._save_annotations()

    def _parse_video_specs(self) -> LabelStudioTrackingTaskConverter.__VideoSpecs:
        """
        Parse attributes for a video file.

        Returns:
            The parsed video attributes.
        """

        video = cv2.VideoCapture(self.video_path)

        if video.isOpened():
            video_specs = LabelStudioTrackingTaskConverter.__VideoSpecs(
                width=int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                height=int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                frame_count=int(video.get(cv2.CAP_PROP_FRAME_COUNT)),
                frame_rate=video.get(cv2.CAP_PROP_FPS),
            )
            video.release()

            return video_specs
        else:
            raise RuntimeError(f"Could not open video '{self.video_path}'")

    def _find_task(self) -> Dict[str, Any]:
        """
        Finds the task inside the tracking annotation file using the videos filename.
        """
        video_name = os.path.basename(self.video_path)

        with open(file=self.tracking_annotations_path, encoding="utf-8") as file:
            data = json.load(fp=file)

        if len(data) == 0:
            raise ValueError(
                f"Invalid annotation file. Task for video '{video_name}' is missing."
            )

        task: Dict[str, Any]
        for task in data:
            try:
                file = task["file_upload"]
            except KeyError as exc:
                raise ValueError(
                    "Invalid task. Key file_upload is missing for a task."
                ) from exc

            if file == video_name:
                return task

        raise ValueError(
            f"Invalid annotation file. Task for video '{video_name}' is missing."
        )

    def _parse_tracking_annotations_file(self) -> None:
        """
        Parse the tracking annotation JSON file.
        """

        task = self._find_task()

        annotations = task.get("annotations", [])

        if len(annotations) == 0:
            raise ValueError("Invalid task. Key annotations is missing or is empty.")

        for annotation in annotations:
            result = annotation.get("result", [])

            self._parse_tracking_annotations_result(result)

    def _parse_tracking_annotations_result(self, result: List[Dict[str, Any]]) -> None:
        """
        Parse a list of tracking annotation results.
        """

        if len(result) == 0:
            raise ValueError(
                "Invalid task. Key annotations.result is missing or is empty."
            )

        for res in result:
            value = res.get("value", {})

            frame_count = value.get("framesCount", -1)

            if frame_count != self.video_specs.frame_count:
                raise ValueError("Invalid task. Frame count differs.")

            labels = value.get("labels", [])

            if len(labels) == 0:
                raise ValueError(
                    "Invalid task. Key annotations.result.value.labels is missing or is empty."
                )

            boxes = value.get("sequence", [])

            if len(boxes) == 0:
                raise ValueError(
                    "Invalid task. Key annotations.result.value.sequence is missing or is empty."
                )

            for box in boxes:
                try:
                    frame_number = box["frame"]
                    x_min = box["x"]
                    y_min = box["y"]
                    width = box["width"]
                    height = box["height"]
                    rotation = box["rotation"]
                except KeyError as exc:
                    raise ValueError(
                        "Annotation must contain keys 'frame', 'time', 'x', 'y', 'width', "
                        "'height' and 'rotation'."
                    ) from exc

                self.annotations[frame_number].append(
                    LabelStudioTrackingTaskConverter.__Annotation(
                        x_min=x_min,
                        y_min=y_min,
                        width=width,
                        height=height,
                        rotation=rotation,
                        labels=labels,
                    )
                )

    def _extract_images(self) -> None:
        """
        Extract the images from the video that have at least one annotation.
        """

        video = cv2.VideoCapture(self.video_path)
        frame_counter = 0

        if video.isOpened():
            with TemporaryDirectory() as tmp_dir:
                with zipfile.ZipFile(self.image_archive_path, "w") as archive:
                    while True:
                        flag, frame = video.read()
                        if flag:
                            if frame_counter in self.annotations:
                                image_file = self._build_image_filename(
                                    frame_number=frame_counter
                                )
                                image_path = os.path.join(tmp_dir, image_file)
                                cv2.imwrite(image_path, frame)
                                archive.write(image_path, image_file)
                            frame_counter += 1
                        else:
                            break
        else:
            raise RuntimeError(f"Could not open video '{self.video_path}'")

    def _save_annotations(self) -> None:
        """
        Save the parsed annotations.
        """

        annotations = []
        for frame_number, annotation in self.annotations.items():
            results = [
                {
                    "original_width": self.video_specs.width,
                    "original_height": self.video_specs.height,
                    "image_rotation": 0,
                    "value": {
                        "x": a.x_min,
                        "y": a.y_min,
                        "width": a.width,
                        "height": a.height,
                        "rotation": a.rotation,
                        "rectanglelabels": a.labels,
                    },
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels",
                    "origin": "manual",
                }
                for a in annotation
            ]

            annotation_dict = {
                "annotations": [
                    {
                        "result": results,
                    }
                ],
                "data": {"image": self._build_image_filename(frame_number)},
            }
            annotations.append(annotation_dict)

        with open(file=self.annotations_path, mode="w", encoding="utf-8") as file:
            json.dump(obj=annotations, fp=file, indent=2)

    def _build_image_filename(self, frame_number: int) -> str:
        """
        Build filename for an image based on video filename and frame number.
        """

        leading_zeros = len(str(self.video_specs.frame_count))
        stem = os.path.splitext(os.path.basename(self.video_path))[0]

        return f"{stem}_{frame_number:0{leading_zeros}d}.png"


def parse_args() -> argparse.Namespace:
    """
    Parse arguments for the CLI script.
    """

    parser = argparse.ArgumentParser(
        description="Tool to convert tracking task annotations."
    )

    parser.add_argument("video_path", help="The video file to extract keyframes from.")
    parser.add_argument(
        "tracking_annotations_path",
        help="The file containing the trackking annotation data.",
    )
    parser.add_argument(
        "image_archive_path", help="Zip file, the keyframes are written to."
    )
    parser.add_argument(
        "annotations_path",
        help="File the detection annotations are written to.",
    )

    return parser.parse_args(sys.argv[1:])


def main() -> None:
    """
    Main entrypoint for the CLI script.
    """

    args = parse_args()

    converter = LabelStudioTrackingTaskConverter(
        video_path=args.video_path,
        tracking_annotations_path=args.tracking_annotations_path,
        image_archive_path=args.image_archive_path,
        annotations_path=args.annotations_path,
    )

    converter.run()


if __name__ == "__main__":
    main()
