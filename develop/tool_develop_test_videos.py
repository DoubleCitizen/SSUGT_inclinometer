import sys
import cv2
from PySide6.QtCore import Qt, QThread, Signal, QMutex
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QCheckBox, QSpinBox

from classes.GlobalController import GlobalController
from classes.segmentation_base import SegmentationBase


class VideoPlayer(QThread):
    """Background thread to process arbitrary video frames testing."""
    frameChanged = Signal(QImage)
    seekRequested = Signal(int)

    def __init__(self, video_path):
        """Initializes the background testing video thread."""
        super().__init__()
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.frame_pos = 0
        self.mutex = QMutex()
        self.segmentation = SegmentationBase()
        self.seekRequested.connect(self.seek)

    def run(self):
        """Processes target video buffer sequentially emitting segments."""
        while True:
            self.mutex.lock()

            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            if ret:
                # points, frame, center_bubbles_px = self.segmentation.v2_frame_proccesing(frame)
                frame = self.segmentation.v2_frame_proccesing(frame)
                if len(frame.shape) > 2:
                    height, width, channel = frame.shape
                    bytes_per_line = channel * width
                    q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
                else:
                    height, width = frame.shape
                    channel = 1
                    bytes_per_line = channel * width
                    q_img = QImage(frame.data, width, height, bytes_per_line,
                                   QImage.Format.Format_Grayscale8).rgbSwapped()

                self.frameChanged.emit(q_img)
            self.mutex.unlock()
            self.msleep(30)  # Approximately 30 FPS

    def seek(self, pos):
        """Navigates the internal CV2 capture state to specific timestamps/frames."""
        self.mutex.lock()
        try:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        except cv2.error as e:
            print(f"Error seeking to frame {pos}: {e}")
            self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        finally:
            self.mutex.unlock()


class MainWindow(QWidget):
    """Main window embedding local video testing UI features."""
    def __init__(self, video_path):
        """Instantiates default configurations loading given testing path."""
        super().__init__()

        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.cap.release()

        self.video_player = VideoPlayer(video_path)
        self.video_player.frameChanged.connect(self.update_frame)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, self.total_frames - 1)
        self.slider.valueChanged.connect(self.seek_frame)

        self.checkbox_segmentaion_show = QCheckBox("Показать сегментацию")
        self.checkbox_draw_rectangle = QCheckBox("Показать прямоугольник")
        self.checkbox_draw_points = QCheckBox("Показать точки")
        self.spinbox_points = QSpinBox()
        self.spinbox_points.setValue(100)
        GlobalController.set_checkBox_segmentaion_show(self.checkbox_segmentaion_show)
        GlobalController.set_checkBox_view_points(self.checkbox_draw_points)
        GlobalController.set_checkBox_rectangle_show(self.checkbox_draw_rectangle)
        GlobalController.set_spinBox_points(self.spinbox_points)

        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.checkbox_segmentaion_show)
        self.layout.addWidget(self.checkbox_draw_rectangle)
        self.layout.addWidget(self.checkbox_draw_points)
        self.layout.addWidget(self.spinbox_points)

        self.video_player.start()

    def update_frame(self, q_img):
        """Transposes incoming QImage signals into widget display mapping."""
        self.label.setPixmap(QPixmap.fromImage(q_img).scaled(640, 480, Qt.KeepAspectRatio))

    def seek_frame(self, pos):
        """Issues command forcing testing track sequences towards pos."""
        self.video_player.seekRequested.emit(pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("../bad_videos/2024_08_10 20_51_12.avi")
    # window = MainWindow("3.mkv")
    window.show()
    sys.exit(app.exec())
