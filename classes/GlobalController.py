from PySide6.QtWidgets import QCheckBox, QSpinBox, QLabel, QPushButton


class GlobalController:
    _checkBox_rectangle_show: None | QCheckBox = None
    _checkBox_segmentaion_show: None | QCheckBox = None
    _checkBox_enable_record: None | QCheckBox = None
    _checkBox_view_points: None | QCheckBox = None
    _checkBox_start_position: None | QCheckBox = None
    _label_vim_temperature: None | QLabel = None
    _spinBox_points: None | QSpinBox = None
    _video_capture_source = None
    _lineEdit_source_video = None
    _label_status_esp_connect: QLabel | None = None
    _status_esp_icon: QLabel | None = None
    _label_fps_counter: QLabel | None = None
    _pushButton_apply_source: QPushButton | None = None

    @classmethod
    def get_push_button_apply_source(cls) -> QPushButton:
        return cls._pushButton_apply_source

    @classmethod
    def set_push_button_apply_source(cls, pushButton_apply_source: QPushButton):
        cls._pushButton_apply_source = pushButton_apply_source

    @classmethod
    def set_label_fps_counter(cls, label_fps_counter: QLabel):
        cls._label_fps_counter = label_fps_counter

    @classmethod
    def get_label_fps_counter(cls) -> QLabel:
        return cls._label_fps_counter

    @classmethod
    def set_status_esp_icon(cls, status_esp_icon: QLabel):
        cls._status_esp_icon = status_esp_icon

    @classmethod
    def get_status_esp_icon(cls) -> QLabel:
        return cls._status_esp_icon

    @classmethod
    def set_label_status_esp_connect(cls, label_status_esp_connect: QLabel):
        cls._label_status_esp_connect = label_status_esp_connect

    @classmethod
    def get_label_status_esp_connect(cls) -> QLabel:
        return cls._label_status_esp_connect

    @classmethod
    def set_label_vim_temperature(cls, label_vim_temperature: QLabel):
        cls._label_vim_temperature = label_vim_temperature

    @classmethod
    def get_label_vim_temperature(cls) -> QLabel:
        return cls._label_vim_temperature

    @classmethod
    def set_lineEdit_source_video(cls, value):
        cls._lineEdit_source_video = value

    @classmethod
    def set_video_capture_source(cls, value):
        cls._video_capture_source = value
        cls._lineEdit_source_video.setText(value)

    @classmethod
    def get_video_capture_source(cls):
        return cls._video_capture_source

    @classmethod
    def set_spinBox_points(cls, value):
        cls._spinBox_points = value

    @classmethod
    def get_spinBox_points(cls):
        return cls._spinBox_points

    @classmethod
    def get_count_draw_points(cls) -> int:
        return cls.get_spinBox_points().value()

    @classmethod
    def set_checkBox_rectangle_show(cls, value):
        cls._checkBox_rectangle_show = value

    @classmethod
    def set_checkBox_start_position(cls, value):
        cls._checkBox_start_position = value

    @classmethod
    def set_checkBox_segmentaion_show(cls, value):
        cls._checkBox_segmentaion_show = value

    @classmethod
    def set_checkBox_enable_record(cls, value):
        cls._checkBox_enable_record = value

    @classmethod
    def set_checkBox_view_points(cls, value):
        cls._checkBox_view_points = value

    @classmethod
    def is_draw_rectangle(cls):
        if cls._checkBox_rectangle_show is None:
            return False
        return cls._checkBox_rectangle_show.isChecked()

    @classmethod
    def is_segmentaion_show(cls):
        if cls._checkBox_segmentaion_show is None:
            return False
        return cls._checkBox_segmentaion_show.isChecked()

    @classmethod
    def is_recording(cls):
        if cls._checkBox_enable_record is None:
            return True
        return cls._checkBox_enable_record.isChecked()

    @classmethod
    def is_draw_points(cls):
        if cls._checkBox_view_points is None:
            return False
        return cls._checkBox_view_points.isChecked()

    @classmethod
    def is_draw_start_position(cls) -> bool:
        if cls._checkBox_start_position is None:
            return False
        return cls._checkBox_start_position.isChecked()
