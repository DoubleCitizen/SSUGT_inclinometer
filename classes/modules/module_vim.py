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
        self._source: None | str = source
        self.is_streaming: bool = False
        self.module_parent_conn, self.module_child_conn = multiprocessing.Pipe()
        self.module_parent_sync_conn, self.module_child_sync_conn = multiprocessing.Pipe()
        self.segmentation = SegmentationBase()
        self.vim_process: multiprocessing.Process | None = None
        self.vim_process_id = None
        self._esp32_name = ''
        self._points = []
        self._center_bubbles_px = 0
        self._fps = 0
        self._frame: np.ndarray = np.zeros((1, 1, 3), dtype=np.uint8)
        self._frame_original: np.ndarray = np.zeros((1, 1, 3), dtype=np.uint8)
        self._is_camera = False
        self._thread = threading.Thread(target=self._prepare_send_data)
        self._is_segmentation: bool | None = None
        self._is_draw_rectangle: bool | None = None
        self._is_draw_point: bool | None = None
        self._count_draw_points: int | None = None
        self._is_draw_start_position: bool | None = None

    @property
    def is_segmentation(self):
        if self._is_segmentation is None:
            return GlobalController.is_segmentaion_show()
        return self._is_segmentation

    @property
    def is_draw_rectangle(self):
        if self._is_draw_rectangle is None:
            return GlobalController.is_draw_rectangle()
        return self._is_draw_rectangle

    @property
    def is_draw_point(self):
        if self._is_draw_point is None:
            return GlobalController.is_draw_points()
        return self._is_draw_point

    @property
    def count_draw_points(self):
        if self._count_draw_points is None:
            return GlobalController.get_count_draw_points()
        return self._count_draw_points

    @property
    def is_draw_start_position(self):
        if self._is_draw_start_position is None:
            return GlobalController.is_draw_start_position()
        return self._is_draw_start_position

    @is_segmentation.setter
    def is_segmentation(self, is_segmentation):
        self._is_segmentation = is_segmentation

    @is_draw_rectangle.setter
    def is_draw_rectangle(self, is_draw_rectangle):
        self._is_draw_rectangle = is_draw_rectangle

    @is_draw_point.setter
    def is_draw_point(self, is_draw_point):
        self._is_draw_point = is_draw_point

    @count_draw_points.setter
    def count_draw_points(self, count_draw_points):
        self._count_draw_points = count_draw_points

    @is_draw_start_position.setter
    def is_draw_start_position(self, is_draw_start_position):
        self._is_draw_start_position = is_draw_start_position

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
            self._source))
        self.vim_process.start()

    def stop_stream(self):
        self.is_streaming = False
        self.vim_process.terminate()

    def _prepare_send_data(self):
        is_segmentation = False
        is_draw_rectangle = False
        is_draw_point = False
        count_draw_points = 1
        is_draw_start_position = False
        while self.is_streaming:
            time.sleep(0.00001)
            new_is_segmentation = self.is_segmentation
            new_is_draw_rectangle = self.is_draw_rectangle
            new_is_draw_point = self.is_draw_point
            new_count_draw_points = self.count_draw_points
            new_is_draw_start_position = self.is_draw_start_position
            if is_segmentation != new_is_segmentation or \
                    is_draw_rectangle != new_is_draw_rectangle or \
                    is_draw_point != new_is_draw_point or \
                    count_draw_points != new_count_draw_points or \
                    is_draw_start_position != new_is_draw_start_position:
                is_segmentation = new_is_segmentation
                is_draw_rectangle = new_is_draw_rectangle
                is_draw_point = new_is_draw_point
                count_draw_points = new_count_draw_points
                is_draw_start_position = new_is_draw_start_position
                self._send_data(is_segmentation, is_draw_rectangle, is_draw_point, count_draw_points,
                                is_draw_start_position)

    def _send_data(self, is_segmentation, is_draw_rectangle, is_draw_point, count_draw_points, is_draw_start_position):
        self.module_parent_conn.send(
            ((is_segmentation, is_draw_rectangle, is_draw_point, count_draw_points, is_draw_start_position),
             ProcessVIM.DRAW_OPTIONS))

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
                                                                                               center_bubbles_px,
                                                                                               is_draw_start_position)
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
