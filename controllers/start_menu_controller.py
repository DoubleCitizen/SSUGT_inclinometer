from PyQt5.QtWidgets import QMainWindow

from controllers import post_processing_controller
from controllers.main_controller import Ui_MainWindowController
from ui import start_menu


class Ui_MainWindow(QMainWindow, start_menu.Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        super().setupUi(MainWindow)
        self.add_functions()

    def add_functions(self):
        self.add_push_buttons()

    def add_push_buttons(self):
        self.pushButton_vim.clicked.connect(lambda: self.open_main_window())
        self.pushButton_post_processing.clicked.connect(lambda: self.open_post_processing_window())

    def open_main_window(self):
        main_window = Ui_MainWindowController()
        main_window.setupUi(self.MainWindow)

    def open_post_processing_window(self):
        post_processing_window = post_processing_controller.Ui_MainWindow()
        post_processing_window.setupUi(self.MainWindow)
