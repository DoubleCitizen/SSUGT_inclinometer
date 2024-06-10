from PyQt5.QtWidgets import QCheckBox, QSpinBox


class GlobalController:
    _checkBox_rectangle_show: None | QCheckBox = None
    _checkBox_segmentaion_show: None | QCheckBox = None
    _checkBox_enable_record: None | QCheckBox = None
    _checkBox_view_points: None | QCheckBox = None
    _spinBox_points: None | QSpinBox = None
    _video_capture_source = None
    _lineEdit_source_video = None

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
    def set_checkBox_rectangle_show(cls, value):
        cls._checkBox_rectangle_show = value

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
        return cls._checkBox_rectangle_show.isChecked()

    @classmethod
    def is_segmentaion_show(cls):
        return cls._checkBox_segmentaion_show.isChecked()

    @classmethod
    def is_recording(cls):
        return cls._checkBox_enable_record.isChecked()

    @classmethod
    def is_draw_points(cls):
        return cls._checkBox_view_points.isChecked()
