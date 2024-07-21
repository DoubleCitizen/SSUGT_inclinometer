# import requests
import os
import sys

import numpy as np
import cv2
from PyQt5.QtCore import QLibraryInfo
from pyqt5_plugins.examplebutton import QtWidgets

from classes.stream_controller import StreamController
from controllers.start_menu_controller import Ui_MainWindow

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()  # Используйте ваш класс здесь
    MainWindow.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    # cap = cv2.VideoCapture("inklin.mp4")
    # segmentation = SegmentationBase(cap)
    # segmentation.start_stream()
