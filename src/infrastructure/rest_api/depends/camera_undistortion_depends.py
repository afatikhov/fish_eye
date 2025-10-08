from fastapi import Depends

from infrastructure.db.pg_repo.camera_repo import CameraCalibrationInfoRepo
from infrastructure.rest_api.depends.camera_calibration_depends import get_camera_calibration_info_repo
from services.camera_undistortion_service import CameraUndistortionService


def get_camera_undistortion_service(camera_calibration_info_repo:
                                    CameraCalibrationInfoRepo=Depends(get_camera_calibration_info_repo)):
    return CameraUndistortionService(camera_calibration_info_repo=camera_calibration_info_repo)