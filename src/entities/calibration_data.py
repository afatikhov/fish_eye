from typing import Optional

from pydantic import BaseModel


class CameraCalibrationData(BaseModel):
    dim_width: int
    dim_height: int
    k_matrix: list[list[float]]
    d_coefficients: list[list[float]]
    rms_error: float
    calibration_flags: int
    num_images: int

class CameraCalibrationWriteData(CameraCalibrationData):
    camera_id: int