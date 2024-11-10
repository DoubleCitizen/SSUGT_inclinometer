import os
import threading
import time

import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtWidgets import QMainWindow, QFileDialog, QSlider

from classes.GlobalController import GlobalController
from classes.segmentation_base import SegmentationBase
from ui import develop_video_tool


class VideoPlayer(QThread):
    frameChanged = Signal(np.ndarray, np.ndarray)
    seekRequested = Signal(int)
    pause_video_signal = Signal()
    start_video_signal = Signal()

    def __init__(self, horizontalSlider_video, video_path=None):
        super().__init__()
        self._is_seek_changed = False
        self._is_pause_video = False
        self.video_path = video_path
        self.horizontalSlider_video: QSlider = horizontalSlider_video
        self.cap = None
        if self.video_path:
            self.cap = cv2.VideoCapture(video_path)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.horizontalSlider_video.setRange(0, self.total_frames - 1)
        self.frame_pos = 0
        self.mutex_1 = QMutex()
        self.mutex_2 = QMutex()
        self.segmentation = SegmentationBase()
        self.seekRequested.connect(self.seek)
        self.pause_video_signal.connect(self.pause_video)
        self.start_video_signal.connect(self.start_video)

    def set_video(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.horizontalSlider_video.setRange(0, self.total_frames - 1)

    def run(self):
        while True:
            if not self.cap or self._is_seek_changed or self._is_pause_video:
                time.sleep(0.1)
                continue
            self.mutex_1.lock()

            ret, frame_original = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.horizontalSlider_video.setValue(0)
                ret, frame_original = self.cap.read()
            if ret:
                points, frame, center_bubbles_px = self.segmentation.v2_frame_proccesing(frame_original.copy())
                # points, frame, center_bubble = self.segmentation.new_frame_processing(frame_original.copy())
                self.horizontalSlider_video.setValue(self.horizontalSlider_video.value() + 1)
                self.frameChanged.emit(frame_original, frame)
            self.mutex_1.unlock()
    def pause_video(self):
        self._is_pause_video = True

    def start_video(self):
        self._is_pause_video = False

    def seek(self, pos):
        self.mutex_2.lock()
        self._is_seek_changed = True
        if not self.cap:
            self.mutex_2.unlock()
            return
        try:
            # self.cap.release()
            # self.cap = cv2.VideoCapture(self.video_path)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        except cv2.error as e:
            print(f"Error seeking to frame {pos}: {e}")
            self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        finally:
            self._is_seek_changed = False
            self.mutex_2.unlock()


class Ui_MainWindow(QMainWindow, develop_video_tool.Ui_MainWindow):
    def __init__(self):
        self._is_pause_video = False
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self._is_pause_video = False
        self.MainWindow = MainWindow
        self.combobox_initialize()
        self.video_player = VideoPlayer(self.horizontalSlider_video)
        self.video_player.frameChanged.connect(self.update_frame)
        self.horizontalSlider_video.sliderReleased.connect(self.seek_frame)
        self.horizontalSlider_video.sliderPressed.connect(self.pause_video_from_slider)
        self.video_player.start(priority=QThread.Priority.LowestPriority)
        self.add_functions()

    def combobox_initialize(self):
        self.comboBox_detectors.addItem("Детектор пузырька V1")

    def update_frame(self, frame_original: np.ndarray, frame: np.ndarray):
        self.graphicsView_original_video.image_cv(frame_original)
        self.graphicsView_segm_video.image_cv(frame)

    def pause_video_from_slider(self):
        self.video_player.pause_video()

    def seek_frame(self):
        # time.sleep(1)
        # threading.Thread(self.video_player.seek(pos)).start()
        self.video_player.seekRequested.emit(self.horizontalSlider_video.value())
        if not self._is_pause_video:
            self.start_video()

    def add_functions(self):
        self.pushButton_select_path.clicked.connect(lambda: self.get_save_path())
        self.pushButton_pause_video.clicked.connect(lambda: self.pause_video())
        self.pushButton_start_video.clicked.connect(lambda: self.start_video())
        GlobalController.set_checkBox_segmentaion_show(self.checkbox_segmentaion_show)
        GlobalController.set_checkBox_view_points(self.checkbox_draw_points)
        GlobalController.set_checkBox_rectangle_show(self.checkbox_draw_rectangle)
        GlobalController.set_spinBox_points(self.spinBox)

    def start_video(self):
        self._is_pause_video = False
        self.pushButton_pause_video.setDisabled(False)
        self.pushButton_start_video.setDisabled(True)
        self.video_player.start_video_signal.emit()

    def pause_video(self):
        self._is_pause_video = True
        self.pushButton_pause_video.setDisabled(True)
        self.pushButton_start_video.setDisabled(False)
        self.video_player.pause_video_signal.emit()

    def get_save_path(self):
        """
        Вставка пути где будет создан новый проект
        """

        self.save_path, _ = QFileDialog.getOpenFileNames(None, "Открытие видеофайла", str(os.getcwd()),
                                                         "Все файлы (*.*)")
        if len(self.save_path) == 0:
            self.save_path = ""
            return
        self.save_path = self.save_path[0]

        self.lineEdit_path_videos.setText(str(self.save_path))
        self.video_player.set_video(self.save_path)
        self.pushButton_start_video.setDisabled(True)
        self.pushButton_pause_video.setDisabled(False)
