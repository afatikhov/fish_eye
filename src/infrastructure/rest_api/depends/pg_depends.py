from infrastructure.db.connection import AsyncSessionMaker
from infrastructure.db.pg_models.camera_models import Cameras
from infrastructure.db.pg_repo.camera_repo import CameraRepo


async def get_pg_db():
    async with AsyncSessionMaker() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise

def get_camera_repo() -> CameraRepo:
    return CameraRepo(model=Cameras)