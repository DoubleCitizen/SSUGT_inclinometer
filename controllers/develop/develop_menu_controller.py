from PySide6.QtWidgets import QMainWindow

from controllers import post_processing_controller, start_menu_controller
from controllers.develop import develop_video_tool_controller
from ui import develop_tool_menu


class Ui_MainWindow(QMainWindow, develop_tool_menu.Ui_MainWindow):
    """Development tools menu module constructor."""
    def __init__(self):
        """Initializes development menu."""
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        """Sets up UI layouts for the developer menu."""
        self.MainWindow = MainWindow
        super().setupUi(MainWindow)
        self.add_functions()

    def add_functions(self):
        """Registers signals to functional callbacks."""
        self.add_push_buttons()

    def add_push_buttons(self):
        """Binds action handlers to menu buttons."""
        self.pushButton_back.clicked.connect(lambda: self.open_start_menu())
        self.pushButton_video_analyzer.clicked.connect(lambda: self.open_develop_video_tool())

    def open_start_menu(self):
        """Returns the user back to the primary start screen."""
        main_window = start_menu_controller.Ui_MainWindow()
        main_window.setupUi(self.MainWindow)

    def open_develop_video_tool(self):
        """Transitions into the development video analysis interface."""
        main_window = develop_video_tool_controller.Ui_MainWindow()
        main_window.setupUi(self.MainWindow)
