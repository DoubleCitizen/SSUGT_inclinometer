import logging
import time

from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QLineEdit, QComboBox

from classes.consts import SpeedFrame


class ShootingSpeed:
    """Manages recording framerate limits and UI sanctions.
    
    Attributes:
        _lineEdit_speed_frame (QLineEdit): Input for framerate constraint.
        _comboBox_speed_frame (QComboBox): Input for limit mode (Hz vs seconds per frame).
        _mode_speed_frame (SpeedFrame): The active speed limit mode.
        _timer (float): Internal time reference for enforcing rate limits.
    """
    _lineEdit_speed_frame: QLineEdit | None = None
    _comboBox_speed_frame: QComboBox | None = None
    _mode_speed_frame: SpeedFrame = SpeedFrame.MODE_HZ
    _timer = time.time()

    @classmethod
    def enable_sanctions(cls):
        """Disables UI interaction for modifying speed settings."""
        logging.info("Framerate change sanctions enabled")
        cls._lineEdit_speed_frame.setEnabled(False)
        cls._comboBox_speed_frame.setEnabled(False)

    @classmethod
    def disable_sanctions(cls):
        """Enables UI interaction for modifying speed settings."""
        logging.info("Framerate change sanctions disabled")
        cls._lineEdit_speed_frame.setEnabled(True)
        cls._comboBox_speed_frame.setEnabled(True)

    @classmethod
    def set_line_edit_speed_frame(cls, lineedit_speed_frame: QLineEdit):
        """Maps speed framerate text inputs targeting validation restrictions."""
        cls._lineEdit_speed_frame = lineedit_speed_frame
        cls._lineEdit_speed_frame.setValidator(QDoubleValidator())

    @classmethod
    def get_line_edit_speed_frame(cls) -> QLineEdit:
        """Retrieves mapped framerate interval line edit configurations."""
        return cls._lineEdit_speed_frame

    @classmethod
    def set_combobox_speed_frame(cls, combobox_speed_frame: QComboBox):
        """Binds dropdown elements adjusting framerate limitation behaviors."""
        cls._comboBox_speed_frame = combobox_speed_frame

    @classmethod
    def get_combobox_speed_frame(cls) -> QComboBox:
        """Fetches bound limitation dropdown configuration element instances."""
        return cls._comboBox_speed_frame

    @classmethod
    def set_mode_speed_frame(cls, mode: SpeedFrame):
        """Updates internal speed calculation strategies tracking active delays."""
        cls._mode_speed_frame = mode

    @classmethod
    def get_mode_speed_frame(cls) -> SpeedFrame:
        """Extracts calculation limit algorithms adjusting temporal mapping bounds."""
        return cls._mode_speed_frame

    @classmethod
    def get_is_ready_shoot(cls) -> bool:
        """Determines if enough time has passed to capture another frame.
        
        Returns:
            bool: True if it's time to capture a frame based on speed limits, False otherwise.
        """
        match cls.get_mode_speed_frame():
            case SpeedFrame.MODE_HZ:
                if cls._timer + 1 / float(cls._lineEdit_speed_frame.text()) < time.time():
                    cls._timer = time.time()
                    return True
            case SpeedFrame.MODE_SECONDS_PER_FRAME:
                if cls._timer + float(cls._lineEdit_speed_frame.text()) < time.time():
                    cls._timer = time.time()
                    return True
        return False
