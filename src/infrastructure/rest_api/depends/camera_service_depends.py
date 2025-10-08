from fastapi.params import Depends

from infrastructure.db.pg_models.camera_models import Cameras
from infrastructure.db.pg_repo.camera_repo import CameraRepo
from infrastructure.rest_api.depends.pg_depends import get_camera_repo
from services.camera_service import CameraService


def get_camera_service(camera_repo: CameraRepo=Depends(get_camera_repo)) -> CameraService:
    return CameraService(camera_repo=camera_repo)