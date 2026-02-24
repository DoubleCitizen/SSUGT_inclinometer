# import requests
import logging
import multiprocessing
import os
import signal
import sys
from datetime import datetime

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
    """Terminates the current process.

    Gets the current process ID and sends a SIGTERM signal to terminate it.
    """
    pid = os.getpid()
    try:
        os.kill(pid, signal.SIGTERM)  # Sends SIGTERM signal
        print(f"Process with PID {pid} terminated.")
    except ProcessLookupError:
        print(f"Process with PID {pid} not found.")
    except PermissionError:
        print(f"No permissions to terminate process with PID {pid}.")


if __name__ == "__main__":
    """Main execution block to start the application.
    
    Sets up multiprocessing freeze support, logging to a file in the 'logs' folder,
    and initializes the PySide6 application window.
    """
    # Specify the folder name
    multiprocessing.freeze_support()
    folder_name = 'logs'

    # Check if the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # Create folder if it does not exist
        print(f"Folder '{folder_name}' has been created.")
    else:
        print(f"Folder '{folder_name}' already exists.")
    # Get current date and time in YYYY-MM-DD_HH-MM-SS format
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logging.basicConfig(level=logging.INFO, filename=f"logs/py_log_{current_datetime}.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = Ui_MainWindow()  # Use your class here
    MainWindow.setupUi(MainWindow)
    MainWindow.show()
    app.exec()
    kill_process()
    sys.exit()
    # cap = cv2.VideoCapture("inklin.mp4")
    # segmentation = SegmentationBase(cap)
    # segmentation.start_stream()
