# import requests
import os
import sys

import numpy as np
import cv2
from PyQt5.QtCore import QLibraryInfo
from pyqt5_plugins.examplebutton import QtWidgets

from classes.stream_controller import StreamController
from controllers.main_controller import Ui_MainWindowController

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindowController()  # Используйте ваш класс здесь
    MainWindow.show()
    sys.exit(app.exec_())
    # cap = cv2.VideoCapture("inklin.mp4")
    # segmentation = SegmentationBase(cap)
    # segmentation.start_stream()
