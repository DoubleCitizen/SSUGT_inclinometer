import json
import logging
import multiprocessing
import os
import threading
import time

import numpy as np
from PySide6.QtGui import QIcon

from classes.APIController import APIController
from classes.GlobalController import GlobalController
from classes.consts import ProcessVIM
from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.segmentation_base import SegmentationBase


class ModuleVim:
    def __init__(self, source: str | None = None):
        self._source = source
        self._source: None | str = None
        self.is_streaming: bool = False
        self.module_parent_conn, self.module_child_conn = multiprocessing.Pipe()
        self.module_parent_sync_conn, self.module_child_sync_conn = multiprocessing.Pipe()
        self.segmentation = SegmentationBase()
        self.vim_process = None
        self.vim_process_id = None
        self._esp32_name = ''
        self._points = []
        self._center_bubbles_px = 0
        self._fps = 0
        self._frame: np.ndarray = np.zeros((1, 1, 3), dtype=np.uint8)
        self._frame_original: np.ndarray = np.zeros((1, 1, 3), dtype=np.uint8)
        self._is_camera = False
        self._thread = threading.Thread(target=self.send_data)

    @property
    def frame_original(self) -> np.ndarray:
        return self._frame_original

    @property
    def is_camera(self) -> bool:
        return self._is_camera

    @property
    def points(self) -> list:
        return self._points

    @property
    def center_bubbles_px(self) -> float:
        return self._center_bubbles_px

    @property
    def esp32_name(self) -> str:
        return self._esp32_name

    @property
    def fps(self) -> int:
        return self._fps

    @property
    def frame(self) -> np.ndarray:
        return self._frame

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, source: str):
        self._source = source

    def set_source(self, source: str):
        self._source = source

    def clear_source(self):
        self._source = None

    def start_stream(self):
        self.is_streaming = True
        data_api_controller = APIController.get_all_data()
        self._thread.start()
        self.vim_process = multiprocessing.Process(target=self.processing, args=(
            self.module_child_conn, self.module_child_sync_conn, self.segmentation, data_api_controller,
            self._source)).start()

    def stop_stream(self):
        self.module_parent_conn.send((self.is_streaming, ProcessVIM.KILL_PROCESS))
        self.is_streaming = False

    def send_data(self):
        while self.is_streaming:
            time.sleep(0.00001)
            is_segmentation = GlobalController.is_segmentaion_show()
            is_draw_rectangle = GlobalController.is_draw_rectangle()
            is_draw_point = GlobalController.is_draw_points()
            count_draw_points = GlobalController.get_count_draw_points()
            is_draw_start_position = GlobalController.is_draw_start_position()
            self.module_parent_conn.send(
                ((is_segmentation, is_draw_rectangle, is_draw_point, count_draw_points, is_draw_start_position), ProcessVIM.DRAW_OPTIONS))

    def update_data(self):
        if self.module_parent_conn.poll():
            value, type_data = self.module_parent_conn.recv()
            match type_data:
                case ProcessVIM.DATA_FRAME:
                    self._points, self._center_bubbles_px, self._frame, self._frame_original, self._fps, self._is_camera = value
                    self.module_parent_sync_conn.send('Done')
                case ProcessVIM.PROCESS_ID:
                    self.vim_process_id = value

    @staticmethod
    def processing(conn, sync_conn, segmentation, data_api_controller, source):
        vim_process_id = -1
        APIController.set_all_data(data_api_controller)
        APIController.check_is_video_capture(source)
        sync_data = "Done"
        is_segmentation = False
        is_draw_rectangle = False
        is_draw_point = False
        is_draw_start_position = False
        count_draw_points = 1
        while vim_process_id is not None:
            time.sleep(0.00001)
            if sync_conn.poll(0.00001):
                sync_data = sync_conn.recv()
            if sync_data == "Done":
                frame_original, fps, is_camera = APIController.get_frame()
                points, frame, center_bubbles_px = segmentation.new_frame_processing(frame_original.copy(),
                                                                                     is_segmentation,
                                                                                     is_draw_rectangle, is_draw_point,
                                                                                     count_draw_points)
                if len(points) <= 0:
                    continue
                CoordinateSystemOffset.set_temp_start_position(center_bubbles_px)
                points, frame, center_bubbles_px = CoordinateSystemOffset.get_new_image_coords(points, frame,
                                                                                               center_bubbles_px, is_draw_start_position)
                conn.send(((points, center_bubbles_px, frame, frame_original, fps, is_camera), ProcessVIM.DATA_FRAME))
                sync_data = None

            if conn.poll(0.00001):
                value, type_data = conn.recv()
                match type_data:
                    case ProcessVIM.PROCESS_ID:
                        conn.send((ProcessVIM.PROCESS_ID, os.getpid()))
                    case ProcessVIM.API_CONTROLLER_DATA:
                        data_api_controller = value
                        APIController.set_all_data(data_api_controller)
                    case ProcessVIM.DRAW_OPTIONS:
                        is_segmentation, is_draw_rectangle, is_draw_point, count_draw_points, is_draw_start_position = value
                    case ProcessVIM.KILL_PROCESS:
                        return

    def get_esp32_name(self):
        if not APIController.get_is_video_capture():
            self._esp32_name = json.loads(APIController.get_name().content).get("name", "esp32")
        if self._esp32_name is None:
            self.connection_is_missing(self._esp32_name)
        elif self._esp32_name == '':
            pass
        else:
            self.connection_is_good(self._esp32_name)

    @staticmethod
    def connection_is_missing(esp32_name):
        logging.info(f"Разорвано соединение с ВИМ: {esp32_name}")
        text_status = f"Разорвано соединение с ВИМ: {esp32_name}"
        icon = QIcon(u":/resource/resource/close.png")
        pixmap = icon.pixmap(16, 16)  # Установите размер иконки
        GlobalController.get_label_status_esp_connect().setText(f"{text_status}")
        GlobalController.get_status_esp_icon().setText("")
        GlobalController.get_status_esp_icon().setPixmap(pixmap)

    @staticmethod
    def connection_is_good(esp32_name):
        logging.info(f"Успешное соединение с ВИМ: {esp32_name}")
        text_status = f"Успешное соединение с ВИМ: {esp32_name}"
        icon = QIcon(u":/resource/resource/check.png")
        pixmap = icon.pixmap(16, 16)  # Установите размер иконки
        GlobalController.get_label_status_esp_connect().setText(f"{text_status}")
        GlobalController.get_status_esp_icon().setText("")
        GlobalController.get_status_esp_icon().setPixmap(pixmap)