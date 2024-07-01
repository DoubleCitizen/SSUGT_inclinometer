import cv2
import numpy as np

from classes.GlobalController import GlobalController


class CoordinateSystemOffset:
    _temp_start_position = 0
    _start_position = 0

    @classmethod
    def set_temp_start_position(cls, value: float):
        cls._temp_start_position = value

    @classmethod
    def apply_start_position(cls):
        cls._start_position = cls._temp_start_position

    @classmethod
    def get_new_image_coords(cls, points: np.ndarray, image: np.ndarray, center_bubble: float) -> np.ndarray | list | float:
        x = int(cls._start_position)
        y1 = 0
        y2 = int(image.shape[0])
        if GlobalController.is_draw_start_position():
            image = cv2.line(image, (x, y1), (x, y2), (255, 0, 0), thickness=10)
        center_bubble -= cls._start_position
        points[:, 0] -= np.int32(cls._start_position)

        return points, image, center_bubble
