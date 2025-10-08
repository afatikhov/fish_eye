from fastapi import APIRouter, Body, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.rest_api.depends.camera_calibration_depends import get_camera_calibration_service
from infrastructure.rest_api.depends.pg_depends import get_pg_db
from schemas import CameraCalibrate
from services.camera_calibration_service import CameraCalibrationService

camera_calibration_router = APIRouter()


@camera_calibration_router.post("/calibrate-camera")
async def calibrate_camera(camera_calibrate: CameraCalibrate=Depends(CameraCalibrate.as_form),
                           image_upload: UploadFile = File(..., media_type="image/png"),
                           session: AsyncSession=Depends(get_pg_db),
                           camera_calibration_service: CameraCalibrationService=Depends(get_camera_calibration_service)):
   result = await camera_calibration_service.calibrate_and_write(image_upload_file=image_upload,
                                                           camera_calibrate=camera_calibrate,
                                                           session=session)
   return result