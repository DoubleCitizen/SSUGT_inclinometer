import cv2
import numpy as np

from classes.GlobalController import GlobalController
from classes.config_controller import ConfigController


class CoordinateSystemOffset:
    """Manages offset logic and saving for coordinate systems relative to bubbles.
    
    Attributes:
        _temp_start_position (float): In-memory offset coordinate before applying.
        _start_position (float): Applied start position for shifting the axis.
    """
    _temp_start_position = 0
    _start_position = None

    @classmethod
    def set_temp_start_position(cls, value: float):
        """Prepares arbitrary tracking position resolving memory offset target."""
        cls._temp_start_position = value

    @classmethod
    def apply_start_position(cls):
        """Applies configuration and saves temporary offset into persistent state."""
        json_data = ConfigController("data/dialog_esp32.json").load()
        json_data.update({'start_position': cls._temp_start_position})
        ConfigController("data/dialog_esp32.json").save(json_data)
        cls._start_position = cls._temp_start_position

    @classmethod
    def set_start_position(cls, value: float):
        """Immediately alters offset position safely.
        
        Args:
            value (float): Coordinate offset position to apply immediately.
        """
        json_data = ConfigController("data/dialog_esp32.json").load()
        json_data.update({'start_position': value})
        ConfigController("data/dialog_esp32.json").save(json_data)
        cls._start_position = value

    @classmethod
    def get_start_position(cls):
        """Extracts validated cached target layout defaults."""
        if cls._start_position is None:
            json_data = ConfigController("data/dialog_esp32.json").load()
            cls._start_position = json_data.get('start_position', 0)
        return cls._start_position

    @classmethod
    def get_new_image_coords(cls, points: np.ndarray, image: np.ndarray,
                             center_bubble: float, is_draw_start_position: bool = False) -> np.ndarray | list | float:
        """Shifts coordinates based on established starting offsets, draws origin.
        
        Args:
            points (np.ndarray): Original image coordinates.
            image (np.ndarray): Full raw image instance.
            center_bubble (float): Reference coordinate of bubble center.
            is_draw_start_position (bool): Toggles drawing line on target.
            
        Returns:
            points: Shifted coordinates matrix.
            image (np.ndarray): Formatted resulting image array.
            center_bubble (float): Updated relative coordinate.
        """
        x = int(cls.get_start_position())
        y1 = 0
        y2 = int(image.shape[0])
        if is_draw_start_position:
            image = cv2.line(image, (x, y1), (x, y2), (255, 0, 0), thickness=10)
        center_bubble -= cls.get_start_position()
        points[:, 0] -= np.int32(cls.get_start_position())

        return points, image, center_bubble
