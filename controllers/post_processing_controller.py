import multiprocessing
import os
import sys
import threading

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication

from classes.post_processing import start_processing
from controllers import start_menu_controller
from ui import post_processing


class Ui_MainWindow(QMainWindow, post_processing.Ui_MainWindow):
    signal_progressbar = Signal(int)
    signal_time_label = Signal(float)

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.signal_progressbar.connect(self.set_value_progress_bar)
        self.signal_time_label.connect(self.set_time_label)
        self.save_path = ""
        self.progressBar.setVisible(False)
        self.label_time.setVisible(False)
        self.add_functions()

    def set_time_label(self, seconds: float):
        minutes, seconds = divmod(seconds, 60)
        if minutes > 0:
            self.label_time.setText(f"Осталось {round(minutes)} мин {round(seconds)} с")
        else:
            self.label_time.setText(f"Осталось {round(seconds)} с")

    def set_value_progress_bar(self, percent: int):
        if percent == 400:
            self.progressBar.setVisible(False)
            self.label_time.setVisible(False)
        else:
            self.progressBar.setValue(percent)

    def add_functions(self):
        self.pushButton_select_path.clicked.connect(lambda: self.get_save_path())
        self.pushButton_start_processing.clicked.connect(self.start_processing)
        self.action_main_window.triggered.connect(self.open_start_window)

    def open_start_window(self):
        start_menu_window = start_menu_controller.Ui_MainWindow()
        start_menu_window.setupUi(self.MainWindow)

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

        self.lineEdit.setText(str(self.save_path))

    def start_processing(self):
        if not os.path.exists(self.save_path):
            return
        self.progressBar.setVisible(True)
        self.label_time.setVisible(True)
        t = threading.Thread(target=start_processing, args=(self.save_path, self.signal_progressbar, self.signal_time_label))
        t.start()
