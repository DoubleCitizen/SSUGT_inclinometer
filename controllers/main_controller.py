import cv2
import threading

from PyQt5.QtWidgets import QMainWindow

from classes.GlobalController import GlobalController
from classes.NivelTool import NivelTool
from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.stream_controller import StreamController
from dialogs.dialog_esp32 import Esp32Dialog
from dialogs.dialog_linear_reg import InputDialog
from ui import main


class Ui_MainWindowController(QMainWindow, main.Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindowController, self).__init__()
        self.setupUi(self)
        self.segmentation: StreamController | None = None
        GlobalController.set_checkBox_segmentaion_show(self.checkBox_segmentaion_show)
        GlobalController.set_checkBox_view_points(self.checkBox_view_points)
        GlobalController.set_checkBox_enable_record(self.checkBox_enable_record)
        GlobalController.set_checkBox_rectangle_show(self.checkBox_rectangle_show)
        GlobalController.set_spinBox_points(self.spinBox_points)
        GlobalController.set_lineEdit_source_video(self.lineEdit_source_video)
        GlobalController.set_checkBox_start_position(self.checkBox_start_position)

    def closeEvent(self, event):
        # Здесь можно выполнить необходимые действия перед закрытием
        NivelTool.close_modem()
        self.stop_stream()
        print("hello world!")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.add_functions()
        self.segmentation = None

    def start_stream(self, cap):
        self.segmentation = StreamController(cap, self.graphicsView, self.label_value)
        self.segmentation.start_stream()

    def stop_stream(self):
        if self.segmentation is not None:
            self.segmentation.stop_stream()
        self.graphicsView.scene.clear()

    def add_functions(self):
        self.pushButton_apply_source.clicked.connect(lambda: self.apply_source())
        self.pushButton_stop_stream.clicked.connect(lambda: self.stop_stream())
        self.pushButton_start_position.clicked.connect(lambda: CoordinateSystemOffset.apply_start_position())

        self.add_actions()
        # self.checkBox_enable_record.clicked.connect(lambda self.)

    def add_actions(self):
        NivelTool.set_action_nivel_220(self.menu_Nivel_220)
        NivelTool.set_label_nivel_220(self.label_nivel)
        self.menu_tools.aboutToShow.connect(self.update_list_com_ports)
        self.action_dialog_regres.triggered.connect(self.open_dialog_parameters_reg)
        self.action_esp32.triggered.connect(self.open_dialog_esp32)

    def open_dialog_esp32(self):
        dialog = Esp32Dialog()
        dialog.exec()

    def open_dialog_parameters_reg(self):
        dialog = InputDialog()
        if dialog.exec():
            print('Данные сохранены')
        else:
            print('Данные отменены')

    def update_list_com_ports(self):
        NivelTool.update_list_com_ports()

    def apply_source(self):
        if self.segmentation is None or not self.segmentation.video_is_started:
            source_video = self.lineEdit_source_video.text()
            cap = cv2.VideoCapture(source_video)
            process = threading.Thread(target=lambda: self.start_stream(cap))
            process.start()
