from fastapi import APIRouter

from infrastructure.rest_api.routers.camera_calibration_routers import camera_calibration_router
from infrastructure.rest_api.routers.camera_routers import camera_router
from infrastructure.rest_api.routers.camera_undistortion_routers import camera_undistortion_router

routers = APIRouter()

routers.include_router(camera_router, prefix="/camera")
routers.include_router(camera_calibration_router)
routers.include_router(camera_undistortion_router)