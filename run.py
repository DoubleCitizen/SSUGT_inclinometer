# import requests
import os
import signal
import sys

import numpy as np
import cv2
from PySide6 import QtWidgets
from PySide6.QtCore import QLibraryInfo

from classes.stream_controller import StreamController
from controllers.start_menu_controller import Ui_MainWindow

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)


def kill_process():
    """Завершает процесс с заданным PID.

    Args:
        pid: ID процесса, который нужно завершить.
    """
    pid = os.getpid()
    try:
        os.kill(pid, signal.SIGTERM)  # Отправляет сигнал SIGTERM
        print(f"Процесс с PID {pid} завершен.")
    except ProcessLookupError:
        print(f"Процесс с PID {pid} не найден.")
    except PermissionError:
        print(f"Нет прав для завершения процесса с PID {pid}.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = Ui_MainWindow()  # Используйте ваш класс здесь
    MainWindow.setupUi(MainWindow)
    MainWindow.show()
    app.exec()
    kill_process()
    sys.exit()
    # cap = cv2.VideoCapture("inklin.mp4")
    # segmentation = SegmentationBase(cap)
    # segmentation.start_stream()
