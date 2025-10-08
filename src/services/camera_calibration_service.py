import cv2
import numpy as np
import starlette
from sqlalchemy.ext.asyncio import AsyncSession

from entities.calibration_data import CameraCalibrationData, CameraCalibrationWriteData
from infrastructure.db.pg_repo.camera_repo import CameraCalibrationInfoRepo
from schemas import CameraCalibrate
from services.camera_calibrator import CameraCalibrator


class CameraCalibrationService:
    def __init__(self, camera_calibration_info_repo: CameraCalibrationInfoRepo):
        self.camera_calibration_info_repo: CameraCalibrationInfoRepo = camera_calibration_info_repo

    async def calibrate_and_write(self, image_upload_file: starlette.datastructures.UploadFile,
                                  camera_calibrate: CameraCalibrate,
                                  session: AsyncSession):
        contents = await image_upload_file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        chessboard_size: tuple[int, int] = camera_calibrate.chessboard_w, camera_calibrate.chessboard_h
        camera_calibrator: CameraCalibrator = CameraCalibrator(chessboard_size=chessboard_size)
        camera_calibration_data: CameraCalibrationData = camera_calibrator.calibrate(image=image)

        camera_calibration_write_data: CameraCalibrationWriteData = CameraCalibrationWriteData(
            camera_id=camera_calibrate.camera_id,
            **camera_calibration_data.model_dump()
        )
        result = await self.camera_calibration_info_repo.add(session=session,
                                                       **camera_calibration_write_data.model_dump())

        return result