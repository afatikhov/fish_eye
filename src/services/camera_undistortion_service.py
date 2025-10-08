import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from entities.calibration_data import CameraCalibrationData
from infrastructure.db.pg_models.camera_models import CameraCalibrationInfo
from infrastructure.db.pg_repo.camera_repo import CameraCalibrationInfoRepo
import cv2
import starlette
import io


class CameraUndistortionService:
    def __init__(self, camera_calibration_info_repo: CameraCalibrationInfoRepo):
        self.camera_calibration_info_repo: CameraCalibrationInfoRepo = camera_calibration_info_repo

    async def undistort_image_upload(self, image_upload: starlette.datastructures.UploadFile,
                                     camera_id: int, session: AsyncSession):
        contents = await image_upload.read()
        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        undistorted_image = await self.undistort_photo(camera_id=camera_id,
                                          image=image,
                                          session=session)

        success, encoded_image = cv2.imencode(".png", undistorted_image)
        if not success:
            raise ValueError("Не удалось закодировать изображение")

        return StreamingResponse(
            io.BytesIO(encoded_image.tobytes()),
            media_type="image/png"
        )

    async def undistort_photo(self, camera_id: int,
                              image: np.ndarray,
                              session: AsyncSession):
        camera_calibration_data: CameraCalibrationData = await self.get_camera_calibration_data(camera_id=camera_id,
                                                                                                session=session)
        K = np.array(camera_calibration_data.k_matrix)
        D = np.array(camera_calibration_data.d_coefficients)
        DIM = camera_calibration_data.dim_width, camera_calibration_data.dim_height
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        undistorted_img = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted_img

    async def get_camera_calibration_data(self, camera_id: int,
                                          session: AsyncSession):
        camera_calibration_info: CameraCalibrationInfo = await self.camera_calibration_info_repo.get(session=session,
                                                                                                     camera_id=camera_id)

        camera_calibration_data: CameraCalibrationData = CameraCalibrationData.from_orm(camera_calibration_info)

        return camera_calibration_data
    async def undistort_video(self):
        pass