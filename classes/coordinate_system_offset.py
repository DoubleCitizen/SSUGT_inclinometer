import cv2
import numpy as np

from classes.GlobalController import GlobalController
from classes.config_controller import ConfigController


class CoordinateSystemOffset:
    _temp_start_position = 0
    _start_position = None

    @classmethod
    def set_temp_start_position(cls, value: float):
        cls._temp_start_position = value

    @classmethod
    def apply_start_position(cls):
        json_data = ConfigController("data/dialog_esp32.json").load()
        json_data.update({'start_position': cls._temp_start_position})
        ConfigController("data/dialog_esp32.json").save(json_data)
        cls._start_position = cls._temp_start_position

    @classmethod
    def get_start_position(cls):
        if cls._start_position is None:
            json_data = ConfigController("data/dialog_esp32.json").load()
            cls._start_position = json_data.get('start_position')
        return cls._start_position

    @classmethod
    def get_new_image_coords(cls, points: np.ndarray, image: np.ndarray,
                             center_bubble: float) -> np.ndarray | list | float:
        x = int(cls.get_start_position())
        y1 = 0
        y2 = int(image.shape[0])
        if GlobalController.is_draw_start_position():
            image = cv2.line(image, (x, y1), (x, y2), (255, 0, 0), thickness=10)
        center_bubble -= cls.get_start_position()
        points[:, 0] -= np.int32(cls.get_start_position())

        return points, image, center_bubble
