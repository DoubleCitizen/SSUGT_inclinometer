import json
import os
import queue
import socket
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QColor
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGridLayout, \
    QListWidget, QListWidgetItem, QColorDialog, QWidget
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
import pickle

from classes.APIController import APIController
from classes.GlobalController import GlobalController
from classes.config_controller import ConfigController


def scan_ip(addr: str, result_queue: queue.Queue):
    try:
        host = socket.gethostbyaddr(addr)
        result_queue.put(host)
    except socket.herror:
        result_queue.put(None)


class Esp32Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setWindowTitle("Подключение ESP32")

        # Параметр a
        self.list_widget_ip_addresses = QListWidget()
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
        self.lineEdit_stream = QLineEdit(":81/stream")
        self.lineEdit_placeholder.textChanged.connect(self.update_video_capture_info)
        self.lineEdit_stream.textChanged.connect(self.update_video_capture_info)

        self.refresh_ip_info()
        # Кнопка отправки

        layout.addWidget(self.list_widget_ip_addresses, 0, 0, 1, 2)
        layout.addWidget(self.pushButton_refresh, 1, 0)
        layout.addWidget(self.pushButton_connect, 1, 1)
        layout.addWidget(self.lineEdit_placeholder, 2, 0)
        layout.addWidget(self.lineEdit_stream, 2, 1)
        layout.addWidget(self.color_widget, 3, 0, 1, 2)
        layout.addWidget(self.button_color_picker, 4, 0, 1, 2)

        self.setLayout(layout)
        self.load()

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
            list_widget_ip_addresses_info = json_data['list_widget_ip_addresses_info']
            for ip_address in list_widget_ip_addresses_info:
                self.list_widget_ip_addresses.addItem(ip_address)
            self.lineEdit_placeholder.setText(json_data['lineEdit_placeholder_text'])
            self.lineEdit_stream.setText(json_data['lineEdit_stream_text'])
            rgb = json_data.get('rgb', (0, 0, 0))
            if rgb is None:
                rgb = (0, 0, 0)
            self.color_widget.setStyleSheet(f"background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
        except:
            pass

    def save(self):
        self.create_directory('data')
        config_controller = ConfigController("data/dialog_esp32.json")
        json_data = config_controller.load()
        list_widget_ip_addresses_info = self.get_all_texts(self.list_widget_ip_addresses)
        lineEdit_placeholder_text = self.lineEdit_placeholder.text()
        lineEdit_stream_text = self.lineEdit_stream.text()
        rgb = APIController.get_color_rgb()

        json_data.update({
            "list_widget_ip_addresses_info": list_widget_ip_addresses_info,
            "lineEdit_placeholder_text": lineEdit_placeholder_text,
            "lineEdit_stream_text": lineEdit_stream_text,
        })
        if rgb is not None:
            json_data.update({"rgb": rgb})

        config_controller.save(json_data)

        # self.color_dialog.setCo

    def update_video_capture_info(self):
        self.save()
        APIController.set_ip(self.lineEdit_placeholder.text() + "/")
        video_capture = self.lineEdit_placeholder.text() + self.lineEdit_stream.text()
        GlobalController.set_video_capture_source(video_capture)

    def connect_ip(self):
        network_info = self.list_widget_ip_addresses.currentItem().text().split('\t')
        ip = network_info[0]
        self.lineEdit_placeholder.setText(f"http://{ip}")
        self.save()

    @staticmethod
    def scan_network(network_range):
        arp = ARP(pdst=network_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=2, verbose=0)
        clients = []
        for sent, received in result[0]:
            try:
                client_name = socket.gethostbyaddr(received.psrc)[0]
                client_name = client_name
            except:
                client_name = "Unknown"
            clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'name': client_name})
        return clients

    def get_list_network(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = local_ip.rsplit('.', 1)
        network_range = f"{subnet[0]}.0/24"
        clients = self.scan_network(network_range)
        return clients

    def refresh_ip_info(self):
        threading.Thread(target=self._refresh_ip_info).start()

    def _refresh_ip_info(self):
        ip_list = self.get_list_network()
        self.list_widget_ip_addresses.clear()
        for network_info in ip_list:
            item = QListWidgetItem(f"{network_info['ip']}\t{network_info['name']}\t{network_info['mac']}")
            self.list_widget_ip_addresses.addItem(item)
        print(ip_list)

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
