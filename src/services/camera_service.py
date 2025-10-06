from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.pg_repo.camera_repo import CameraRepo
from schemas import CameraAdd, CameraDelete


class CameraService:
    def __init__(self, camera_repo: CameraRepo):
        self.camera_repo: CameraRepo = camera_repo

    async def add_camera(self, camera_add: CameraAdd,
                         session: AsyncSession):
        result = await self.camera_repo.add(session=session,
                                   **camera_add.model_dump())
        await session.commit()

        return result

    async def get_all_cameras(self, session: AsyncSession):
        result = await self.camera_repo.get_all(session=session)
        return result

    async def delete_camera(self, camera_delete: CameraDelete,
                            session: AsyncSession):
        result = await self.camera_repo.delete(session=session,
                                               **camera_delete.model_dump())
        await session.commit()

        return result