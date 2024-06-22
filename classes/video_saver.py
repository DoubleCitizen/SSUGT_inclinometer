import os
from datetime import datetime

import cv2


class VideoSaver:
    def __init__(self):
        self._out = None
        self._is_recording = False
        self.width = 0
        self.height = 0
        self.fps = 30

    def get_out(self):
        return self._out
    def get_record_status(self):
        return self._is_recording

    @staticmethod
    def create_directory(folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return
        else:
            os.makedirs(folder_path)

    def initialize(self, fps, width, height):
        # Получение текущего времени
        current_time = datetime.now()
        self.fps = fps
        self.width = width
        self.height = height

        # Форматирование времени в строку в нужном формате
        formatted_time = current_time.strftime("%Y_%m_%d %H_%M_%S")
        current_directory = os.getcwd()
        self.create_directory(current_directory.replace('\\', '/') + '/data')

        filename = current_directory + "/data/" + formatted_time + ".avi"

        # fourcc = cv2.VideoWriter_fourcc(*'avc1')
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self._out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    def write_frame(self, frame):
        self._is_recording = True
        self._out.write(frame)

    def release(self):
        if self._out is None:
            return
        self._out.release()
        self._out = None
        self._is_recording = False
