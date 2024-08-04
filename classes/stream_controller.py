import json
import time
from datetime import datetime

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QLabel, QCheckBox
from PySide6 import QtCore

from classes.APIController import APIController
from classes.GlobalController import GlobalController
from classes.GlobalVarialbles import GlobalVariables
from classes.NivelTool import NivelTool
from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.math_module import MathModule
from classes.segmentation_base import SegmentationBase
from classes.value_saver import FileSaver
from classes.video_saver import VideoSaver
from widgets.graphicsviewvideo import QGraphicsViewVideo
from widgets.qgraphicsviewplot import QGraphicsViewPlot


class StreamController(QObject):

    def __init__(self, cap, graphics_view, label_value, signal_send_frame_graphics_view):
        super().__init__()
        self.cap = cap
        self.label_value: QLabel = label_value
        # Получить общие кадры и FPS
        # self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.graphics_view: QGraphicsViewVideo = graphics_view
        self.video_is_started = False
        self.segmentation = SegmentationBase()
        self.video_saver = VideoSaver()
        self.file_saver = FileSaver()
        self.signal_send_frame_graphics_view = signal_send_frame_graphics_view

    def send_frame_on_graphics_view(self, frame: np.ndarray):
        self.graphics_view.image_cv(frame)

    def stop_stream(self):
        self.video_is_started = False

    def connection_is_missing(self, esp32_name):
        text_status = f"Разорвано соединение с ВИМ: {esp32_name}"
        icon = QIcon(u":/resource/resource/close.png")
        pixmap = icon.pixmap(16, 16)  # Установите размер иконки
        GlobalController.get_label_status_esp_connect().setText(f"{text_status}")
        GlobalController.get_status_esp_icon().setText("")
        GlobalController.get_status_esp_icon().setPixmap(pixmap)

    def connection_is_good(self, esp32_name):
        text_status = f"Успешное соединение с ВИМ: {esp32_name}"
        icon = QIcon(u":/resource/resource/check.png")
        pixmap = icon.pixmap(16, 16)  # Установите размер иконки
        GlobalController.get_label_status_esp_connect().setText(f"{text_status}")
        GlobalController.get_status_esp_icon().setText("")
        GlobalController.get_status_esp_icon().setPixmap(pixmap)

    def start_stream(self):
        self.video_is_started = True
        esp32_name = ''
        APIController.check_is_video_capture(self.cap)
        image = np.zeros((1, 1))

        while self.video_is_started:
            try:
                if not APIController.get_is_video_capture():
                    esp32_name = json.loads(APIController.get_name().content).get("name", "esp32")
                if esp32_name is None:
                    self.connection_is_missing(esp32_name)
                elif esp32_name == '':
                    pass
                else:
                    self.connection_is_good(esp32_name)

                frame, fps = APIController.get_frame()
                if frame is None:
                    self.video_is_started = False
                    self.connection_is_missing(esp32_name)
                    break
                GlobalController.get_label_fps_counter().setText(f"FPS = {round(fps)}")
                frame_original = frame.copy()
                height, width = frame.shape[:2]
                # fps = self.cap.get(cv2.CAP_PROP_FPS)
                center_bubbles_px = None
                points = np.array([])

                try:
                    image = frame
                    points, image, center_bubbles_px = self.segmentation.new_frame_processing(image)
                    CoordinateSystemOffset.set_temp_start_position(center_bubbles_px)
                    points, image, center_bubbles_px = CoordinateSystemOffset.get_new_image_coords(points, image,
                                                                                                   center_bubbles_px)
                    try:
                        with open('data/params_linear_reg.json', 'r') as file:
                            data_json = json.loads(file.read())
                        value_a = data_json.get('a', 0)
                        value_b = data_json.get('b', 0)
                        units = data_json.get('units', "''")
                        self.label_value.setText(f"ВИМ: {(center_bubbles_px * value_a) + value_b}{units}")
                    except:
                        self.label_value.setText(f"ВИМ: {center_bubbles_px}пикс.")

                    # if GlobalController.is_draw_rectangle() or GlobalController.is_segmentaion_show():
                    # frame = cv2.cvtColor(crop_image, cv2.COLOR_GRAY2BGR)
                    # cv2.imshow("crop_image", crop_image)
                    # math_module = MathModule(x_array, y_array)

                    # X, v = math_module.coeff_mat_estimator2()
                    # a, b, c = X

                    # self.draw_parabola(a, b, c)
                    # if time.time() - timer_1 > 1:
                    #     timer_1 = time.time()
                    #     QMetaObject.invokeMethod(self.graphics_view_plot, "draw_parabola", QtCore.Qt.QueuedConnection,
                    #                              Q_ARG(float, a), Q_ARG(float, b),
                    #                              Q_ARG(float, c))
                    # QMetaObject.invokeMethod(self.graphics_view_plot, "plot_build",
                    #                          Q_ARG(np.ndarray, frame))
                    # self.label_status.setText("Детект прошел успешно")
                except Exception as e:
                    print(e)
                    # self.label_status.setText("Пузырек не удалось обнаружить")

                if self.video_saver.get_out() is None and GlobalController.is_recording() and self.video_saver.get_record_status() is False:
                    self.video_saver.initialize(
                        fps=fps,
                        width=width,
                        height=height
                    )
                    self.file_saver.initialize(
                        headers=['time', 'center_bubbles_px', 'nivel_x', 'nivel_y', 'nivel_t', 'temperature',
                                 'watch_indicator', 'points'],
                        sep=';')
                temperature = APIController.get_temperature()
                GlobalController.get_label_vim_temperature().setText(f"t = {temperature}°C")
                if GlobalController.is_recording():
                    self.video_saver.write_frame(frame_original)
                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%H:%M:%S.%f")
                    indicator = GlobalVariables.get_indicator_value()
                    self.file_saver.write_data(
                        [formatted_time, center_bubbles_px, NivelTool.current_x, NivelTool.current_y,
                         NivelTool.current_t,
                         str(temperature), str(indicator), str(points.tolist())])
                else:
                    self.video_saver.release()

                key = cv2.waitKey(1)
                self.signal_send_frame_graphics_view.emit(image)
                print("stream")

                if key == ord('q'):
                    break
            except Exception as e:
                print(e)
        if APIController.get_is_video_capture():
            self.cap.release()
        self.connection_is_missing(esp32_name)
        self.graphics_view.scene.clear()
        self.video_saver.release()
