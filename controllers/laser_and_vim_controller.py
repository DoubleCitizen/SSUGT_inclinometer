import os
import subprocess

import cv2
import threading

import numpy as np
from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QMainWindow

from classes.GlobalController import GlobalController
from classes.GlobalVarialbles import GlobalVariables
from classes.NivelTool import NivelTool
from classes.ShootingSpeed import ShootingSpeed
from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.stream_controller import StreamController
from controllers import start_menu_controller
from dialogs.dialog_esp32 import Esp32Dialog
from dialogs.dialog_linear_reg import InputDialog
from ui import laser_and_vim


class UiVIMLaserController(QMainWindow, laser_and_vim.Ui_MainWindow, QObject):
    signal_send_frame_graphics_view_vim = Signal(np.ndarray)
    signal_send_frame_graphics_view_laser = Signal(np.ndarray)

    def __init__(self):
        super(UiVIMLaserController, self).__init__()
        self.segmentation: StreamController | None = None

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        super().setupUi(MainWindow)
        self.disable_mode_static()
        self.initialize_global_controller()
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)
        self.segmentation = None
        self.lineEdit_speed_frame.textChanged.connect(self.speed_frame_line_edit_changed)

        self.add_functions()
        self.lineEdit_source_video.setEnabled(True)
        self.lineEdit_source_video_laser.setEnabled(True)
        self.signal_send_frame_graphics_view_vim.connect(self.send_frame_in_graphics_view_vim)
        self.signal_send_frame_graphics_view_laser.connect(self.send_frame_in_graphics_view_laser)
        self.speed_frame_line_edit_changed()
        self.comboBox_speed_frame.currentIndexChanged.connect(self.combobox_speed_frame_changed)

    def combobox_speed_frame_changed(self):
        ShootingSpeed.set_mode_speed_frame(self.comboBox_speed_frame.currentIndex())

    def speed_frame_line_edit_changed(self):
        try:
            float(self.lineEdit_speed_frame.text())
        except ValueError:
            self.pushButton_start_stream.setEnabled(False)
        else:
            self.pushButton_start_stream.setEnabled(True)

    def initialize_global_controller(self):
        GlobalController.set_label_fps_counter(self.label_fps_counter)
        GlobalController.set_label_vim_temperature(self.label_vim_temp)
        GlobalController.set_label_status_esp_connect(self.label_status_esp_connect)
        GlobalController.set_status_esp_icon(self.label_status_esp_icon)
        GlobalController.set_checkBox_segmentaion_show(self.checkBox_segmentaion_show)
        GlobalController.set_checkBox_view_points(self.checkBox_view_points)
        GlobalController.set_checkBox_enable_record(self.checkBox_enable_record)
        GlobalController.set_checkBox_rectangle_show(self.checkBox_rectangle_show)
        GlobalController.set_spinBox_points(self.spinBox_points)
        GlobalController.set_lineEdit_source_video_vim(self.lineEdit_source_video)
        GlobalController.set_lineEdit_source_video_laser(self.lineEdit_source_video_laser)
        GlobalController.set_checkBox_start_position(self.checkBox_start_position)
        GlobalController.set_push_button_start_stream(self.pushButton_start_stream)
        ShootingSpeed.set_line_edit_speed_frame(self.lineEdit_speed_frame)
        ShootingSpeed.set_combobox_speed_frame(self.comboBox_speed_frame)

    def send_frame_in_graphics_view_vim(self, frame: np.ndarray):
        self.graphicsView_vim.image_cv(frame)

    def send_frame_in_graphics_view_laser(self, frame: np.ndarray):
        self.graphicsView_laser.image_cv(frame)

    def start_timer(self):
        self.timer.start(1000)  # Start the timer with 1 second interval

    def stop_timer(self):
        self.timer.stop()

    def onTimeout(self):
        GlobalVariables.add_time_static(1)
        text_time = GlobalVariables.get_str_time_static()
        self.label_timer.setText(text_time)

    def enable_mode_static(self):
        self.frame_static_1.setVisible(True)
        self.frame_static_2.setVisible(True)

    def disable_mode_static(self):
        self.frame_static_1.setVisible(False)
        self.frame_static_2.setVisible(False)

    def switch_mode_static(self):
        if self.action_static_mode.isChecked():
            self.enable_mode_static()
        else:
            self.disable_mode_static()

    def start_time_point(self):
        self.start_timer()
        self.pushButton_time_point_end.setEnabled(True)
        self.pushButton_time_point_start.setEnabled(False)
        GlobalVariables.set_indicator_value(self.lineEdit_indicator_value.text())
        # GlobalVariables.set_indicator_value(False)

    def stop_time_point(self):
        self.stop_timer()
        GlobalVariables.set_time_static(0)
        self.pushButton_time_point_end.setEnabled(False)
        self.pushButton_time_point_start.setEnabled(True)
        # GlobalVariables.set_indicator_value(self.lineEdit_indicator_value.text())
        GlobalVariables.set_indicator_value(False)

    def update_indicator_value(self):
        pass
        # if self.pushButton_time_point_start.isEnabled():
        #     GlobalVariables.set_indicator_value(self.lineEdit_indicator_value.text())

    def closeEvent(self, event):
        # Здесь можно выполнить необходимые действия перед закрытием
        NivelTool.close_modem()
        self.stop_stream()

    def start_stream(self, cap_vim, cap_laser):
        self.segmentation = StreamController(cap_vim, cap_laser, self.label_value,
                                             self.signal_send_frame_graphics_view_vim, self.signal_send_frame_graphics_view_laser)
        self.segmentation.start_stream()

    def stop_stream(self):
        if self.segmentation is not None:
            self.segmentation.stop_stream()
        self.graphicsView_vim.scene.clear()
        self.graphicsView_laser.scene.clear()

    def add_functions(self):
        self.pushButton_start_stream.clicked.connect(lambda: self.apply_source())
        self.pushButton_stop_stream.clicked.connect(lambda: self.stop_stream())
        self.pushButton_start_position.clicked.connect(lambda: CoordinateSystemOffset.apply_start_position())
        self.pushButton_time_point_start.clicked.connect(lambda: self.start_time_point())
        self.pushButton_time_point_end.clicked.connect(lambda: self.stop_time_point())
        self.lineEdit_indicator_value.textChanged.connect(self.update_indicator_value)

        self.add_actions()

    @staticmethod
    def open_directory():
        path = os.getcwd() + '\\data'
        subprocess.Popen(['explorer', path])

    def add_actions(self):
        NivelTool.set_action_nivel_220(self.menu_Nivel_220)
        NivelTool.set_label_nivel_220(self.label_nivel)
        self.menu_tools.aboutToShow.connect(self.update_list_com_ports)
        self.action_open_directory.triggered.connect(self.open_directory)
        self.action_dialog_regres.triggered.connect(self.open_dialog_parameters_reg)
        self.action_esp32.triggered.connect(self.open_dialog_esp32)
        self.action_static_mode.triggered.connect(self.switch_mode_static)
        self.action_main_window.triggered.connect(lambda: self.open_start_window())

    def open_start_window(self):
        start_menu_window = start_menu_controller.Ui_MainWindow()
        start_menu_window.setupUi(self.MainWindow)

    def open_dialog_esp32(self):
        dialog = Esp32Dialog()
        dialog.exec()

    def open_dialog_parameters_reg(self):
        dialog = InputDialog()
        if dialog.exec():
            print('Данные сохранены')
        else:
            print('Данные отменены')

    def update_list_com_ports(self):
        NivelTool.update_list_com_ports()

    def apply_source(self):
        if self.segmentation is None or not self.segmentation.video_is_started:
            source_video_vim = self.lineEdit_source_video.text()
            source_video_laser = self.lineEdit_source_video_laser.text()
            process = threading.Thread(target=lambda: self.start_stream(source_video_vim, source_video_laser))
            process.start()
