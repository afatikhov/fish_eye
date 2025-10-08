from typing import Optional
import cv2
import numpy as np

from entities.calibration_data import CameraCalibrationData
from infrastructure.db.pg_repo.camera_repo import CameraCalibrationInfoRepo
from schemas import CameraCalibrate


class CameraCalibrator:
    def __init__(self, chessboard_size: tuple[int, int]):
        self.chessboard_size: tuple[int, int] = chessboard_size
        self.objpoints: list[np.ndarray] = []
        self.imgpoints: list[np.ndarray] = []
        self.image_shape: tuple[int, int] | None = None

        self.K: np.ndarray | None = None
        self.D: np.ndarray | None = None
        self.rvecs: list[np.ndarray] | None = None
        self.tvecs: list[np.ndarray] | None = None

        self.subpix_criteria = (
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            30,
            0.1
        )

        self.calibration_flags = (
            cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC +
            cv2.fisheye.CALIB_CHECK_COND +
            cv2.fisheye.CALIB_FIX_SKEW
        )

    def calibrate(self, image: np.ndarray) -> CameraCalibrationData:
        self._process_image(image=image)
        N_OK = len(self.objpoints)
        K = np.zeros((3, 3))
        D = np.zeros((4, 1))
        rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]
        tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]

        rms, self.K, self.D, self.rvecs, self.tvecs = cv2.fisheye.calibrate(
            self.objpoints,
            self.imgpoints,
            self.image_shape[::-1],
            K,
            D,
            rvecs,
            tvecs,
            self.calibration_flags,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
        )

        camera_calibration_data: CameraCalibrationData = CameraCalibrationData(
            dim_width=self.image_shape[1],
            dim_height=self.image_shape[0],
            k_matrix=K.tolist(),
            d_coefficients=D.tolist(),
            rms_error=float(rms),
            calibration_flags=self.calibration_flags,
            num_images=len(self.objpoints)
        )

        return camera_calibration_data

    def _create_chessboard_points(self):
        obj_points = np.zeros((1, self.chessboard_size[0] * self.chessboard_size[1], 3), np.float32)
        obj_points[0, :, :2] = np.mgrid[0:self.chessboard_size[0], 0:self.chessboard_size[1]].T.reshape(-1, 2)
        return obj_points

    def _process_image(self, image: np.ndarray):
        self.image_shape: tuple[int, int] = image.shape[:-1]
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        ret, corners = cv2.findChessboardCorners(gray_image, self.chessboard_size,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

        if ret == True:
            obj_points = self._create_chessboard_points()
            self.objpoints.append(obj_points)
            cv2.cornerSubPix(gray_image, corners, (3, 3), (-1, -1), self.subpix_criteria)
            self.imgpoints.append(corners)

if __name__ == "__main__":
    image = cv2.imread("../../img.png")
    camera_calibrator: CameraCalibrator = CameraCalibrator(chessboard_size=(9, 6))
    print(camera_calibrator.calibrate(image=image))