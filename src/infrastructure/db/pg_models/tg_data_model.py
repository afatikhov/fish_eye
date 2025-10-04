from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.pg_models.base_model import BaseModel


class TgModel(BaseModel):
    __tablename__ = "tg_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True)

    tg_username: Mapped[str] = mapped_column(String, unique=True)

    chat_id: Mapped[int] = mapped_column(Integer, unique=True)