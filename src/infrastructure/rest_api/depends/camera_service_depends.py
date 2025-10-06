from infrastructure.db.pg_models.camera_models import Cameras
from infrastructure.db.pg_repo.camera_repo import CameraRepo
from services.camera_service import CameraService


def get_camera_repo() -> CameraRepo:
    return CameraRepo(model=Cameras)

def get_camera_service(camera_repo: CameraRepo) -> CameraService:
    return CameraService(camera_repo=camera_repo)