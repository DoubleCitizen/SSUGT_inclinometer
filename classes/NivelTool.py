import time
from functools import partial

import serial.tools.list_ports
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMenu, QAction, QLabel
from serial.serialutil import PortNotOpenError, SerialException
from serial.tools.list_ports_common import ListPortInfo


class NivelTool:
    _action_nivel: None | QMenu = None
    _list_com_ports: list[ListPortInfo] = []
    _list_actions: list = []
    _submenu_nivel: QMenu = None
    _label_nivel: QLabel = None
    _cmd = None
    _modem = None
    _answer = None
    _read_timeout = None
    _quantity = None
    _timer = None
    _port_disconnect = "Отключится"
    _selected_port = _port_disconnect
    _current_x = 'NaN'
    _current_y = 'NaN'
    _current_t = 'NaN'


    @classmethod
    @property
    def current_x(cls):
        return cls._current_x


    @classmethod
    @property
    def current_y(cls):
        return cls._current_y


    @classmethod
    @property
    def current_t(cls):
        return cls._current_t

    @classmethod
    def set_action_nivel_220(cls, action_nivel):
        cls._action_nivel = action_nivel

    @classmethod
    def set_label_nivel_220(cls, label_nivel):
        cls._label_nivel = label_nivel

    @classmethod
    def update_list_com_ports(cls):
        ports = serial.tools.list_ports.comports()
        cls._submenu_nivel = cls._action_nivel
        cls._submenu_nivel.clear()
        cls._list_com_ports = []
        cls._list_actions = []
        # Добавление действий в подменю

        # Создание действия
        cls._list_actions.append(QAction(cls._port_disconnect, cls._submenu_nivel))
        if cls._port_disconnect == cls._selected_port:
            cls._list_actions[-1].setEnabled(False)
        cls._list_actions[-1].triggered.connect(partial(cls.set_selected_port, cls._port_disconnect))
        cls._submenu_nivel.addAction(cls._list_actions[-1])

        for port in ports:
            cls._list_com_ports.append(port)
            # Создание действия
            cls._list_actions.append(QAction(port.description, cls._submenu_nivel))
            if port.device == cls._selected_port:
                cls._list_actions[-1].setEnabled(False)
            cls._list_actions[-1].triggered.connect(partial(cls.set_selected_port, port))
            cls._submenu_nivel.addAction(cls._list_actions[-1])

        return ports

    @classmethod
    def set_selected_port(cls, port):
        if str == type(port):
            cls._selected_port = cls._port_disconnect
        else:
            cls._selected_port = port.device
        cls.destroy_nivel_220()
        if cls._selected_port != cls._port_disconnect:
            cls.initialize_nivel_220()

    @classmethod
    def destroy_nivel_220(cls):
        cls._label_nivel.setText("")
        if cls._timer is not None:
            cls._timer.stop()
        if cls._modem is not None:
            cls._modem.close()

    @classmethod
    def start_timer_update_info_label(cls):
        if cls._timer is not None:
            cls._timer.stop()

        # Создаем таймер
        cls._timer = QTimer()
        # Устанавливаем интервал в 800 миллисекунд
        cls._timer.setInterval(800)
        # Соединяем сигнал таймера со слотом (методом для вызова)
        cls._timer.timeout.connect(cls.update_info_label)
        # Запускаем таймер
        cls._timer.start()

    @classmethod
    def get_info_from_vim(cls, data):
        if data.find('X') == -1:
            return
        x_index = [data.find('X:'), data.find('Y:') - 2]
        y_index = [data.find('Y:'), data.find('T:') - 2]
        t_index = [data.find('T:'), data.find('T:') + 7]
        line = [data[x_index[0]:x_index[1]], data[y_index[0]:y_index[1]], data[t_index[0]:t_index[1]]]
        x = {line[0][0]: float(line[0][2:])}
        y = {line[1][0]: float(line[1][2:])}
        t = {line[2][0]: float(line[2][2:])}
        result = {}
        result.update(x)
        result.update(y)
        result.update(t)
        return result

    @classmethod
    def update_info_label(cls):
        cls._quantity = cls._modem.in_waiting
        if cls._quantity > 0:

            cls._answer = str(cls._modem.read(cls._quantity))
            cls._answer = cls.get_info_from_vim(cls._answer)
            result_text = f"X = {str(cls._answer.get('X', 'Ошибка'))}, Y = {str(cls._answer.get('Y', 'Ошибка'))}"
            cls._current_x = cls._answer.get('X', 'NaN')
            cls._current_y = cls._answer.get('Y', 'NaN')
            cls._current_t = cls._answer.get('T', 'NaN')
            cls._label_nivel.setText(result_text)
        else:
            # read_timeout is depends on port speed

            # with following formula it works:

            # 0.1 sec + 1.0 sec / baud rate (bits per second) * 10.0 bits (per character) * 10.0 times

            # example for 115200 baud rate:

            # 0.1 + 1.0 / 115200 * 10.0 * 10.0 ~ 0.1 sec

            time.sleep(cls._read_timeout)
            cls._modem.write(cls._cmd.encode())

        quantity = cls._modem.in_waiting

    @classmethod
    def close_modem(cls):
        if cls._modem is not None:
            cls._modem.close()

    @classmethod
    def initialize_nivel_220(cls):
        try:
            cls._modem = serial.Serial(cls._selected_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1,
                                       rtscts=False, dsrdtr=False)
            cls._modem.close()
            cls._modem.open()

            cls._cmd = "N4C1 G A"
            cls._modem.write(cls._cmd.encode())
            cls._answer = ""
            cls._read_timeout = 0.3  # задержка на чтение

            cls.start_timer_update_info_label()
        except:
            cls._label_nivel.setText("Порт закрыт")
