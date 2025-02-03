import json
import logging
import time
from datetime import datetime

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QLabel, QCheckBox
from PySide6 import QtCore
from sympy.physics.units import temperature

from classes.APIController import APIController
from classes.DevicesController import DevicesController
from classes.GlobalController import GlobalController
from classes.GlobalVarialbles import GlobalVariables
from classes.NivelTool import NivelTool
from classes.ShootingSpeed import ShootingSpeed
from classes.config_controller import ConfigController
from classes.consts import TypeDevices
from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.math_module import MathModule
from classes.modules.module_vim import ModuleESP32
from classes.segmentation_base import SegmentationBase
from classes.value_saver import FileSaver
from classes.video_saver import VideoSaver
from scripts import get_new_points
from widgets.graphicsviewvideo import QGraphicsViewVideo
from widgets.qgraphicsviewplot import QGraphicsViewPlot


class StreamController(QObject):

    def __init__(self, cap, cap_laser, label_value, signal_send_frame_graphics_view_vim, signal_send_frame_graphics_view_laser=None):
        super().__init__()
        self.cap = cap
        self._cap_laser = cap_laser
        self.label_value: QLabel = label_value
        # Получить общие кадры и FPS
        # self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.video_is_started = False
        self.segmentation = SegmentationBase()
        self.video_saver_vim = VideoSaver('vim')
        self.video_saver_laser = VideoSaver('laser')
        self.file_saver = FileSaver()
        self.file_saver.initialize(
            headers=['time', 'center_bubbles_px', 'nivel_x', 'nivel_y', 'nivel_t', 'temperature',
                     'watch_indicator', 'laser_x', 'laser_y', 'points_x', 'points_y'],
            sep=';')
        self.signal_send_frame_graphics_view_vim = signal_send_frame_graphics_view_vim
        self.signal_send_frame_graphics_view_laser = signal_send_frame_graphics_view_laser
        self.module_esp32_vim = ModuleESP32(type_device=TypeDevices.ESP32_VIM)
        self.module_esp32_laser = ModuleESP32(type_device=TypeDevices.ESP32_LASER)

    def stop_stream(self):
        self.video_is_started = False
        ShootingSpeed.disable_sanctions()

    def connection_is_missing(self, esp32_name):
        logging.info(f"Разорвано соединение с ВИМ: {esp32_name}")
        text_status = f"Разорвано соединение с ВИМ: {esp32_name}"
        icon = QIcon(u":/resource/resource/close.png")
        pixmap = icon.pixmap(16, 16)  # Установите размер иконки
        GlobalController.get_label_status_esp_connect().setText(f"{text_status}")
        GlobalController.get_status_esp_icon().setText("")
        GlobalController.get_status_esp_icon().setPixmap(pixmap)

    def connection_is_good(self, esp32_name):
        logging.info(f"Успешное соединение с ВИМ: {esp32_name}")
        text_status = f"Успешное соединение с ВИМ: {esp32_name}"
        icon = QIcon(u":/resource/resource/check.png")
        pixmap = icon.pixmap(16, 16)  # Установите размер иконки
        GlobalController.get_label_status_esp_connect().setText(f"{text_status}")
        GlobalController.get_status_esp_icon().setText("")
        GlobalController.get_status_esp_icon().setPixmap(pixmap)

    def start_stream(self):
        logging.info("Запущен стрим видеопотока")
        self.video_is_started = True
        esp32_vim_name = ''
        # APIController.check_is_video_capture(self.cap)
        self.module_esp32_vim.set_source(self.cap)
        self.module_esp32_vim.start_stream()
        if self._cap_laser is not None:
            self.module_esp32_laser.set_source(self._cap_laser)
            self.module_esp32_laser.start_stream()


        temperature = 0

        while self.video_is_started:
            ShootingSpeed.enable_sanctions()
            if not ShootingSpeed.get_is_ready_shoot():
                time.sleep(0.00000001)
                continue
            self.module_esp32_vim.update_data()
            if self._cap_laser is not None:
                self.module_esp32_laser.update_data()
            # try:
            # if not APIController.get_is_video_capture():
            #     esp32_name = json.loads(APIController.get_name().content).get("name", "esp32")
            # if esp32_name is None:
            #     self.connection_is_missing(esp32_name)
            # elif esp32_name == '':
            #     pass
            # else:
            #     self.connection_is_good(esp32_name)

            #
            frame_vim, frame_original_vim, fps_vim, esp32_vim_name, center_vim_bubbles_px, points_vim, is_camera_vim = (
                self.module_esp32_vim.frame, self.module_esp32_vim.frame_original, self.module_esp32_vim.fps,
                self.module_esp32_vim.esp32_name,
                self.module_esp32_vim.center_bubbles_px,
                self.module_esp32_vim.points, self.module_esp32_vim.is_camera)
            if self._cap_laser is not None:
                frame_laser, frame_original_laser, fps_laser, is_camera_laser, x_laser, y_laser = (
                self.module_esp32_laser.frame, self.module_esp32_laser.frame_original, self.module_esp32_laser.fps,
                self.module_esp32_laser.is_camera, self.module_esp32_laser.x, self.module_esp32_laser.y)

            if self.module_esp32_vim.frame is None or self.module_esp32_vim.frame_original is None:
                continue

            if self._cap_laser is not None:
                if self.module_esp32_laser.frame is None or self.module_esp32_laser.frame_original is None:
                    continue
                if frame_vim is None and frame_laser is None:
                    self.video_is_started = False
                    self.connection_is_missing(esp32_vim_name)
                    break
            if frame_vim is None:
                self.video_is_started = False
                self.connection_is_missing(esp32_vim_name)
                break

            GlobalController.get_label_fps_counter().setText(f"FPS = {round(fps_vim)}")
            # frame_original = frame.copy()
            height_vim, width_vim = frame_vim.shape[:2]
            if self._cap_laser is not None:
                height_laser, width_laser = frame_laser.shape[:2]
            # fps = self.cap.get(cv2.CAP_PROP_FPS)

            try:
                data_json = ConfigController('data/params_linear_reg.json').load()
                if not data_json:
                    raise
                # with open('data/params_linear_reg.json', 'r') as file:
                #     data_json = json.loads(file.read())
                value_a = data_json.get('a', 0)
                value_b = data_json.get('b', 0)
                units = data_json.get('units', "''")
                self.label_value.setText(f"ВИМ: {(center_vim_bubbles_px * value_a) + value_b}{units}")
            except:
                self.label_value.setText(f"ВИМ: {center_vim_bubbles_px}пикс.")
            logging.info("Определение пузырька успешное")
            # self.label_status.setText("Пузырек не удалось обнаружить")

            if self.video_saver_vim.get_out() is None and GlobalController.is_recording() and self.video_saver_vim.get_record_status() is False:
                self.video_saver_vim.initialize(
                    fps=fps_vim,
                    width=width_vim,
                    height=height_vim
                )
            if self._cap_laser is not None:
                if self.video_saver_laser.get_out() is None and GlobalController.is_recording() and self.video_saver_laser.get_record_status() is False:
                    self.video_saver_laser.initialize(
                        fps=fps_laser,
                        width=width_laser,
                        height=height_laser
                    )

            if is_camera_vim:
                temperature = DevicesController.get_vim_api_class().get_temperature()
            GlobalController.get_label_vim_temperature().setText(f"t = {temperature}°C")
            if GlobalController.is_recording():
                self.video_saver_vim.write_frame(frame_original_vim)
                if self._cap_laser is not None:
                    self.video_saver_laser.write_frame(frame_original_laser)
                current_time = datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S.%f")
                indicator = GlobalVariables.get_indicator_value()
                points_x, points_y = get_new_points(points_vim)
                self.file_saver.write_data(
                    [formatted_time, center_vim_bubbles_px, NivelTool.current_x, NivelTool.current_y,
                     NivelTool.current_t,
                     str(temperature), str(indicator), x_laser, y_laser, points_x, points_y])
                logging.info(
                    f"Проведена запись в файл:\n{[formatted_time, center_vim_bubbles_px, NivelTool.current_x, NivelTool.current_y, NivelTool.current_t, str(temperature), str(indicator), points_x, points_y]}")
            else:
                self.video_saver_vim.release()
                self.video_saver_laser.release()

            self.signal_send_frame_graphics_view_vim.emit(frame_vim)
            if self._cap_laser is not None:
                self.signal_send_frame_graphics_view_laser.emit(frame_laser)

            # except Exception as e:
            #     print(e)
        self.module_esp32_vim.stop_stream()
        logging.info(f"Стрим был остановлен")
        if DevicesController.get_vim_api_class().get_is_video_capture():
            DevicesController.get_vim_api_class().get_cap().release()
        self.connection_is_missing(esp32_vim_name)
        # self.graphics_view.scene.clear()
        self.video_saver_vim.release()
        self.video_saver_laser.release()
        ShootingSpeed.disable_sanctions()
