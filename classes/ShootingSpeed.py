import time

from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QLineEdit, QComboBox

from classes.consts import SpeedFrame


class ShootingSpeed:
    _lineEdit_speed_frame: QLineEdit | None = None
    _comboBox_speed_frame: QComboBox | None = None
    _mode_speed_frame: SpeedFrame = SpeedFrame.MODE_HZ
    _timer = time.time()

    @classmethod
    def enable_sanctions(cls):
        cls._lineEdit_speed_frame.setEnabled(False)
        cls._comboBox_speed_frame.setEnabled(False)

    @classmethod
    def disable_sanctions(cls):
        cls._lineEdit_speed_frame.setEnabled(True)
        cls._comboBox_speed_frame.setEnabled(True)

    @classmethod
    def set_line_edit_speed_frame(cls, lineedit_speed_frame: QLineEdit):
        cls._lineEdit_speed_frame = lineedit_speed_frame
        cls._lineEdit_speed_frame.setValidator(QDoubleValidator())

    @classmethod
    def get_line_edit_speed_frame(cls) -> QLineEdit:
        return cls._lineEdit_speed_frame

    @classmethod
    def set_combobox_speed_frame(cls, combobox_speed_frame: QComboBox):
        cls._comboBox_speed_frame = combobox_speed_frame

    @classmethod
    def get_combobox_speed_frame(cls) -> QComboBox:
        return cls._comboBox_speed_frame

    @classmethod
    def set_mode_speed_frame(cls, mode: SpeedFrame):
        cls._mode_speed_frame = mode

    @classmethod
    def get_mode_speed_frame(cls) -> SpeedFrame:
        return cls._mode_speed_frame

    @classmethod
    def get_is_ready_shoot(cls) -> bool:
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
