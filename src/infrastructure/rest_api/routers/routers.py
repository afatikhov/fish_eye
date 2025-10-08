from fastapi import APIRouter

from infrastructure.rest_api.routers.camera_calibration_routers import camera_calibration_router
from infrastructure.rest_api.routers.camera_routers import camera_router

routers = APIRouter()

routers.include_router(camera_router, prefix="/camera")
routers.include_router(camera_calibration_router)