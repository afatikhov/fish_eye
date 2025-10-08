from fastapi import Form
from pydantic import BaseModel


class CameraAdd(BaseModel):
    camera_model: str
    camera_info: str

class CameraDelete(BaseModel):
    id: int

class CameraCalibrate(BaseModel):
    camera_id: int
    chessboard_w: int
    chessboard_h: int

    @classmethod
    def as_form(
        cls,
        camera_id: int = Form(...),
        chessboard_w: int = Form(...),
        chessboard_h: int = Form(...)
    ):
        return cls(camera_id=camera_id, chessboard_w=chessboard_w, chessboard_h=chessboard_h)