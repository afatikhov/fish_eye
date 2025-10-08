from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.rest_api.depends.camera_undistortion_depends import get_camera_undistortion_service
from infrastructure.rest_api.depends.pg_depends import get_pg_db
from services.camera_undistortion_service import CameraUndistortionService

camera_undistortion_router = APIRouter()

@camera_undistortion_router.post("/undistort-image")
async def undistort_image(camera_id: int,
                          image_upload: UploadFile = File(..., media_type="image/png"),
                          camera_undistortion_service:
                          CameraUndistortionService=Depends(get_camera_undistortion_service),
                          session: AsyncSession=Depends(get_pg_db)):
    return await camera_undistortion_service.undistort_image_upload(camera_id=camera_id,
                                                              image_upload=image_upload,
                                                              session=session)