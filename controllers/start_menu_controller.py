from PySide6.QtWidgets import QMainWindow

from controllers import post_processing_controller
from controllers.develop import develop_menu_controller
from controllers.laser_and_vim_controller import UiVIMLaserController
from controllers.main_controller import Ui_MainWindowController
from ui import start_menu


class Ui_MainWindow(QMainWindow, start_menu.Ui_MainWindow):
    """Main window UI constructor for the start menu."""
    def __init__(self):
        """Initializes the start menu interface."""
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        """Sets up the UI elements on the given window."""
        self.MainWindow = MainWindow
        super().setupUi(MainWindow)
        self.add_functions()

    def add_functions(self):
        """Binds controller actions to the interface buttons."""
        self.add_push_buttons()

    def add_push_buttons(self):
        """Maps push buttons to specific window transition callbacks."""
        self.pushButton_vim.clicked.connect(lambda: self.open_main_window())
        self.pushButton_laser_and_vim.clicked.connect(lambda: self.open_laser_and_vim_window())
        self.pushButton_post_processing.clicked.connect(lambda: self.open_post_processing_window())
        self.pushButton_develop_tool.clicked.connect(lambda: self.open_develop_menu())

    def open_develop_menu(self):
        """Opens the developer tools sub-menu."""
        main_window = develop_menu_controller.Ui_MainWindow()
        main_window.setupUi(self.MainWindow)

    def open_main_window(self):
        """Opens the primary VIM inclinometer module."""
        main_window = Ui_MainWindowController()
        main_window.setupUi(self.MainWindow)

    def open_laser_and_vim_window(self):
        """Opens the split system module (Laser and VIM)."""
        main_window = UiVIMLaserController()
        main_window.setupUi(self.MainWindow)

    def open_post_processing_window(self):
        """Opens the post-processing module interface."""
        post_processing_window = post_processing_controller.Ui_MainWindow()
        post_processing_window.setupUi(self.MainWindow)
