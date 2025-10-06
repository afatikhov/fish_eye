from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.rest_api.depends.camera_service_depends import get_camera_service
from infrastructure.rest_api.depends.pg_depends import get_pg_db
from schemas import CameraAdd, CameraDelete
from services.camera_service import CameraService

camera_router = APIRouter()

@camera_router.post("/add-camera")
async def add_camera(camera_add: CameraAdd=Body(...),
                     camera_service: CameraService=Depends(get_camera_service),
                     session: AsyncSession=Depends(get_pg_db)):
    result = await camera_service.add_camera(camera_add=camera_add,
                                             session=session)
    return result

@camera_router.get("/get-all-cameras")
async def get_all_cameras(camera_service: CameraService=Depends(get_camera_service),
        session: AsyncSession=Depends(get_pg_db)):
    result = await camera_service.get_all_cameras(session=session)
    return result

@camera_router.delete("/delete-camera-by-id")
async def delete_camera(camera_delete: CameraDelete=Body(...),
                        camera_service: CameraService=Depends(get_camera_service),
                        session: AsyncSession=Depends(get_pg_db)):
    result = await camera_service.delete_camera(camera_delete=camera_delete,
                                                session=session)

    return result