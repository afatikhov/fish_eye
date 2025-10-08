from fastapi.params import Depends

from infrastructure.db.pg_models.camera_models import CameraCalibrationInfo
from infrastructure.db.pg_repo.camera_repo import CameraCalibrationInfoRepo
from services.camera_calibration_service import CameraCalibrationService


def get_camera_calibration_info_repo() -> CameraCalibrationInfoRepo:
    return CameraCalibrationInfoRepo(model=CameraCalibrationInfo)


def get_camera_calibration_service(camera_calibration_info_repo: CameraCalibrationInfoRepo=Depends(get_camera_calibration_info_repo)):
    return CameraCalibrationService(
        camera_calibration_info_repo=camera_calibration_info_repo
    )