import colorsys
import json
import os
import queue
import socket
import threading
import concurrent.futures

import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator, QColor, QAction
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, \
    QGridLayout, \
    QListWidget, QListWidgetItem, QColorDialog, QWidget, QMenu, QWidgetAction
import pickle

from classes.APIController import APIController
from classes.GlobalController import GlobalController
from classes.config_controller import ConfigController


class ChangeNameMenu(QMenu):
    def __init__(self, parent=None, name=""):
        super().__init__(parent)
        self._is_change_name = False
        self._text = name
        self.initUI()

    def _set_change_name(self, state):
        self._is_change_name = state

    def initUI(self):
        self.textbox = QLineEdit(self._text)
        self.textbox_action = QWidgetAction(self)
        self.textbox_action.setDefaultWidget(self.textbox)
        self.addAction(self.textbox_action)

        self.confirm_action = QAction("Подтвердить", self)
        self.confirm_action.triggered.connect(lambda: self._set_change_name(True))
        self.addAction(self.confirm_action)

        self.cancel_action = QAction("Отменить", self)
        self.cancel_action.triggered.connect(lambda: self._set_change_name(False))
        self.addAction(self.cancel_action)

    def exec(self, event):
        super().exec(event)
        if self._is_change_name:
            return self.textbox.text()


class EspListWidget(QListWidget):
    def __init__(self, refresh_ip):
        super().__init__()
        self.refresh_ip = refresh_ip

    def contextMenuEvent(self, event):
        menu = QMenu()
        action1 = QAction("Подключиться", self)
        action2 = QAction("Изменить имя", self)
        menu.addAction(action1)
        menu.addAction(action2)
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == action2:
            ip = self.selectedItems()[0].text().split('\t')[0]
            name = self.selectedItems()[0].text().split('\t')[-1]
            name = ChangeNameMenu(name=name).exec(self.mapToGlobal(event.pos()))
            try:
                requests.get(f"http://{ip}/set_name?name={name}")
                self.refresh_ip()
            except:
                pass


class Esp32Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setWindowTitle("Подключение ESP32")

        # Параметр a
        self.list_widget_ip_addresses = EspListWidget(self.refresh_ip_info)
        self.pushButton_refresh = QPushButton("Обновить")
        self.pushButton_refresh.clicked.connect(self.refresh_ip_info)

        self.pushButton_connect = QPushButton("Подключиться")
        self.pushButton_connect.clicked.connect(self.connect_ip)
        self.pushButton_connect.clicked.connect(self.update_video_capture_info)
        self.button_color_picker = QPushButton("Выбрать цвет", self)
        self.button_color_picker.clicked.connect(self.openColorDialog)
        self.color_dialog = QColorDialog()

        self.color_widget = QLabel()
        self.color_widget.setStyleSheet("background-color: rgb(0, 0, 0)")  # Красный цвет

        self.lineEdit_placeholder = QLineEdit("http://0.0.0.0")
        self.lineEdit_placeholder.setAlignment(Qt.AlignRight)
        self.lineEdit_stream = QLineEdit("/get_image")
        self.comboBox = QComboBox()
        self.comboBox.addItems([
            "/get_image (получение кадра по requests)",
            ":81/stream (НЕ РАБОТАЕТ!!! получение непрерывных кадров VideoCapture)"
        ])
        self.comboBox.currentIndexChanged.connect(self.combobox_index_changed)
        self.lineEdit_placeholder.textChanged.connect(self.update_video_capture_info)
        self.lineEdit_stream.textChanged.connect(self.update_video_capture_info)

        self.refresh_ip_info()
        # Кнопка отправки

        layout.addWidget(self.list_widget_ip_addresses, 0, 0, 1, 2)
        layout.addWidget(self.pushButton_refresh, 1, 0)
        layout.addWidget(self.pushButton_connect, 1, 1)
        layout.addWidget(self.lineEdit_placeholder, 2, 0)
        layout.addWidget(self.lineEdit_stream, 2, 1)
        layout.addWidget(self.comboBox, 3, 0, 1, 2)
        layout.addWidget(self.color_widget, 4, 0, 1, 2)
        layout.addWidget(self.button_color_picker, 5, 0, 1, 2)

        self.setLayout(layout)
        self.load()

    def combobox_index_changed(self):
        match self.comboBox.currentIndex():
            case 0:
                self.lineEdit_stream.setText("/get_image")
            case 1:
                self.lineEdit_stream.setText(":81/stream")
        self.update_video_capture_info()

    def openColorDialog(self):
        color = self.color_dialog.getColor()
        rgb = color.getRgb()[:-1]
        APIController.set_color_rgb(rgb)
        self.save()
        self.color_widget.setStyleSheet(f"background-color: rgb({int(rgb[0])}, {int(rgb[1])}, {int(rgb[2])})")

    @staticmethod
    def get_all_texts(list_widget):
        texts = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            texts.append(item.text())
        return texts

    @staticmethod
    def create_directory(folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return
        else:
            os.makedirs(folder_path)

    def load(self):
        self.create_directory('data')
        try:
            json_data = ConfigController("data/dialog_esp32.json").load()
            self.lineEdit_placeholder.setText(json_data['lineEdit_placeholder_text'])
            self.lineEdit_stream.setText(json_data['lineEdit_stream_text'])
            self.comboBox.setCurrentIndex(json_data['current_index'])
        except:
            pass

    def save(self):
        self.create_directory('data')
        config_controller = ConfigController("data/dialog_esp32.json")
        json_data = config_controller.load()
        lineEdit_placeholder_text = self.lineEdit_placeholder.text()
        lineEdit_stream_text = self.lineEdit_stream.text()
        index_combobox = self.comboBox.currentIndex()

        json_data.update({
            "lineEdit_placeholder_text": lineEdit_placeholder_text,
            "lineEdit_stream_text": lineEdit_stream_text,
            "current_index": index_combobox,
        })

        config_controller.save(json_data)

        # self.color_dialog.setCo

    def update_video_capture_info(self):
        self.save()
        ip = self.lineEdit_placeholder.text()
        ip = ip.replace('http://', '')
        ip = ip.replace('/', '')
        APIController.set_ip(ip)
        video_capture = self.lineEdit_placeholder.text() + self.lineEdit_stream.text()
        GlobalController.set_video_capture_source(video_capture)

    def connect_ip(self):
        try:
            network_info = self.list_widget_ip_addresses.currentItem().text().split('\t')[0]
        except:
            network_info = self.lineEdit_placeholder.text()
            network_info = network_info.replace("http://", "")
        ip = network_info
        try:
            request = requests.get(f"http://{ip}/get_led_params", timeout=2)
        except:
            self.refresh_ip_info()
            return
        hsv = json.loads(request.content)
        # rgb = colorsys.hsv_to_rgb(hsv.get("hue", 0), hsv.get("saturation", 0), hsv.get("brightness", 0))
        h = hsv['hue'] / 255.0  # нормализация hue в диапазоне от 0 до 1
        s = hsv['saturation'] / 255.0  # нормализация saturation в диапазоне от 0 до 1
        v = hsv['brightness'] / 255.0  # нормализация brightness в диапазоне от 0 до 1

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = [int(x * 255) for x in (r, g, b)]  # преобразование к целочисленному представлению
        # r, g, b = [int(x) for x in colorsys.hsv_to_rgb(hsv.get("hue", 0), hsv.get("saturation", 0), hsv.get("brightness", 0))]
        print(f"hsv = {hsv}")
        print(f"rgb = {r} {g} {b}")
        self.color_widget.setStyleSheet(f"background-color: rgb({r}, {g}, {b})")
        self.lineEdit_placeholder.setText(f"http://{ip}")
        self.save()

    def scan_network(self, network_range):
        q = queue.Queue()
        for ip in range(0, 256):
            ip = f"{network_range}.{ip}"
            t = threading.Thread(target=self.check_ip, args=(ip, q))
            t.start()
            # t.join()  # Wait for the thread to finish

        results = []
        while not q.empty():
            results.append(q.get())

        return results

    @staticmethod
    def check_ip(ip, q):
        try:
            result = requests.get(f"http://{ip}/get_name")
            if result.status_code == 200:
                q.put((ip, result))
        except:
            q.put(None)

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS
        local_ip = s.getsockname()
        s.close()
        return local_ip

    def get_list_network(self):
        # hostname = socket.gethostname()
        # local_ip = socket.gethostbyname(hostname)
        subnet = self.get_local_ip()[0].rsplit('.', 1)
        clients = self.scan_network(subnet[0])
        return clients

    def refresh_ip_info(self):
        self.list_widget_ip_addresses.clear()
        clients = self.get_list_network()
        clients = [_ for _ in clients if _ is not None]
        # self.list_widget_ip_addresses.addItem
        for client in clients:
            ip = client[0]
            try:
                name = json.loads(client[1].content).get("name", "esp32")
            except:
                name = "esp32"
            self.list_widget_ip_addresses.addItem(f"{ip}\t{name}")
        # threading.Thread(target=self._refresh_ip_info).start()

    @staticmethod
    def create_directory(folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return
        else:
            os.makedirs(folder_path)

    def submit(self):
        # Получение значений
        value_a = self.input_a.text()
        value_b = self.input_b.text()
        units = self.combo_units.currentText()

        # Проверка на ввод только чисел
        try:
            value_a = float(value_a)
            value_b = float(value_b)
            print(f'Параметр "a": {value_a}, Параметр "b": {value_b}, Единицы измерения: {units}')
            data_json = {'a': value_a, 'b': value_b, 'units': units}
            current_directory = os.getcwd()
            self.create_directory(current_directory.replace('\\', '/') + '/data')
            with open('data/params_linear_reg.json', 'w+') as file:
                file.write(json.dumps(data_json))
            self.accept()
        except ValueError:
            print('Пожалуйста, введите только числовые значения для параметров "a" и "b".')


if __name__ == '__main__':
    app = QApplication([])
    dialog = Esp32Dialog()
    if dialog.exec_():
        print('Данные отправлены')
    else:
        print('Отправка отменена')
