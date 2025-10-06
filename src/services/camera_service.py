from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.pg_repo.camera_repo import CameraRepo
from schemas import CameraAdd


class CameraService:
    def __init__(self, camera_repo: CameraRepo):
        self.camera_repo: CameraRepo = camera_repo

    async def add_camera(self, camera_add: CameraAdd,
                         session: AsyncSession):
        result = await self.camera_repo.add(session=session,
                                   **camera_add.model_dump())

        return result