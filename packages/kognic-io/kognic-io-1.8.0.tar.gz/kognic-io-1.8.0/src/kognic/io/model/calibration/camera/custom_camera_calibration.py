from __future__ import annotations

import base64
from typing import List, Optional, Tuple

from pydantic import conlist

from kognic.io.model.base_serializer import BaseSerializer
from kognic.io.model.calibration.camera.common import BaseCameraCalibration, CameraMatrix
from kognic.io.model.calibration.common import CalibrationType


class Point3d(BaseSerializer):
    x: float
    y: float
    z: float


class Point2d(BaseSerializer):
    x: float
    y: float


# Expected mapping between 3d and 2d.
# This will be used to validate the calibration so this is highly recommended.
class TestCase(BaseSerializer):
    point3d: Point3d
    point2d: Point2d


class CustomCameraCalibration(BaseCameraCalibration):
    calibration_type = CalibrationType.CUSTOM
    image_height: int
    image_width: int
    wasm_base64: str
    test_cases: conlist(TestCase, max_items=100) = list()

    def get_wasm_bytes(self) -> bytes:
        return base64.b64decode(self.wasm_base64)

    @staticmethod
    def from_bytes(wasm_bytes: bytes, **kwargs) -> CustomCameraCalibration:
        wasm_base64 = base64.b64encode(wasm_bytes)
        return CustomCameraCalibration(wasm_base64=wasm_base64, **kwargs)

    @staticmethod
    def from_file(wasm_path: str, **kwargs) -> CustomCameraCalibration:
        with open(wasm_path, "rb") as file:
            return CustomCameraCalibration.from_bytes(file.read(), **kwargs)
