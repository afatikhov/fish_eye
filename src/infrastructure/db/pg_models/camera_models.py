from sqlalchemy import Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.pg_models.base_model import BaseModel


class CameraCalibrationInfo(BaseModel):
    __tablename__ = "camera_calibration_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True)

    camera_id: Mapped[int] = mapped_column(Integer, ForeignKey("cameras.id"),
                                           unique=True)

    dim_width: Mapped[int] = mapped_column(Integer, nullable=False,
                                           unique=False)
    dim_height: Mapped[int] = mapped_column(Integer, nullable=False,
                                           unique=False)

    k_matrix: Mapped[dict] = mapped_column(JSON, nullable=False,
                                           unique=False)
    d_coefficients: Mapped[dict] = mapped_column(JSON, nullable=False,
                                           unique=False)

    rms_error: Mapped[float] = mapped_column(Float, nullable=False,
                                           unique=False)
    calibration_flags: Mapped[int] = mapped_column(Integer, nullable=False,
                                           unique=False)
    num_images: Mapped[int] = mapped_column(Integer, nullable=False,
                                           unique=False)



    camera: Mapped["Cameras"] = relationship(
        "Cameras",
        back_populates="camera_calibration_info"
    )

class Cameras(BaseModel):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True)

    camera_model: Mapped[str] = mapped_column(String, unique=False)

    camera_info: Mapped[str] = mapped_column(String, unique=False)

    camera_calibration_info: Mapped[CameraCalibrationInfo] = relationship(
        "CameraCalibrationInfo",
        lazy="selectin",
        uselist=False,
        back_populates="camera"
    )