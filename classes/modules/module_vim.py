import json
import logging
import multiprocessing
import os
import time

import numpy as np
from PySide6.QtGui import QIcon

from classes.APIController import APIController
from classes.GlobalController import GlobalController
from classes.consts import ProcessVIM
from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.segmentation_base import SegmentationBase


class ModuleVim:
    sources: list = []
    is_streaming: bool = False
    module_parent_conn, module_child_conn = multiprocessing.Pipe()
    module_parent_sync_conn, module_child_sync_conn = multiprocessing.Pipe()
    segmentation = SegmentationBase()
    vim_process = None
    vim_process_id = None
    esp32_name = ''
    points = []
    center_bubbles_px = 0
    fps = 0
    frame = np.zeros((1,1,3), dtype=np.uint8)
    is_camera = False

    @classmethod
    def add_source(cls, source: str):
        cls.sources.append(source)

    @classmethod
    def set_sources(cls, sources: list[str]):
        cls.sources = sources

    @classmethod
    def clear_sources(cls):
        cls.sources = []

    @classmethod
    def start_stream(cls):
        cls.is_streaming = True
        data_api_controller = APIController.get_all_data()
        cls.vim_process = multiprocessing.Process(target=cls.processing, args=(
            cls.module_child_conn, cls.module_child_sync_conn, cls.segmentation, data_api_controller,
            cls.sources[0])).start()

    @classmethod
    def stop_stream(cls):
        cls.is_streaming = False
        cls.module_parent_conn.send((cls.is_streaming, ProcessVIM.KILL_PROCESS))

    @classmethod
    def update_data(cls):
        if cls.module_parent_conn.poll():
            value, type_data = cls.module_parent_conn.recv()
            match type_data:
                case ProcessVIM.DATA_FRAME:
                    cls.points, cls.center_bubbles_px, cls.frame, cls.fps, cls.is_camera = value
                    cls.module_parent_sync_conn.send('Done')
                case ProcessVIM.PROCESS_ID:
                    cls.vim_process_id = value

    @staticmethod
    def processing(conn, sync_conn, segmentation, data_api_controller, source):
        vim_process_id = -1
        APIController.set_all_data(data_api_controller)
        APIController.check_is_video_capture(source)
        sync_data = "Done"


        while vim_process_id is not None:
            time.sleep(0.00001)
            if conn.poll(0.0001):
                value, type_data = conn.recv()
                match type_data:
                    case ProcessVIM.PROCESS_ID:
                        conn.send((ProcessVIM.PROCESS_ID, os.getpid()))
                    case ProcessVIM.API_CONTROLLER_DATA:
                        data_api_controller = value
                        APIController.set_all_data(data_api_controller)
                    case ProcessVIM.KILL_PROCESS:
                        return

            if sync_conn.poll(0.0001):
                sync_data = sync_conn.recv()
            if sync_data == "Done":
                frame, fps, is_camera = APIController.get_frame()
                points, frame, center_bubbles_px = segmentation.new_frame_processing(frame)
                CoordinateSystemOffset.set_temp_start_position(center_bubbles_px)
                points, frame, center_bubbles_px = CoordinateSystemOffset.get_new_image_coords(points, frame,
                                                                                               center_bubbles_px)
                conn.send(((points, center_bubbles_px, frame, fps, is_camera), ProcessVIM.DATA_FRAME))
                sync_data = None



    @classmethod
    def get_esp32_name(cls):
        if not APIController.get_is_video_capture():
            cls.esp32_name = json.loads(APIController.get_name().content).get("name", "esp32")
        if cls.esp32_name is None:
            cls.connection_is_missing(cls.esp32_name)
        elif cls.esp32_name == '':
            pass
        else:
            cls.connection_is_good(cls.esp32_name)

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
