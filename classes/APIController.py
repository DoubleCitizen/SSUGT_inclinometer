import json
import time

import cv2
import numpy as np
import requests
import colorsys
import logging


class APIController:
    def __init__(self):
        self._ip = None
        self._color_rgb = None
        self._cap = None
        self._is_video_capture: bool = False
        self._conn_multiprocessing = None

    def get_all_data(self):
        return self._ip, self._color_rgb, self._cap, self._is_video_capture

    def set_all_data(self, data):
        self._ip, self._color_rgb, self._cap, self._is_video_capture = data

    def set_conn_multiprocessing(self, conn):
        self._conn_multiprocessing = conn

    def synchronize_data(self):
        if self._conn_multiprocessing is not None:
            self._conn_multiprocessing.send((self.get_all_data(), 'APIController_data'))

    def set_is_video_capture(self, state: bool):
        self._is_video_capture = state
        self.synchronize_data()

    def get_is_video_capture(self):
        return self._is_video_capture

    def set_color_rgb(self, rgb):
        if self._is_video_capture:
            return
        self._color_rgb = rgb
        self.synchronize_data()
        print(rgb)
        # hsv_color = colorsys.rgb_to_hsv(*self._color_rgb)
        # h, s, v = hsv_color
        h, s, v = [x for x in
                   colorsys.rgb_to_hsv(self._color_rgb[0] / 255, self._color_rgb[1] / 255, self._color_rgb[2] / 255)]
        h *= 255
        s *= 255
        v *= 255
        try:
            print(f"rgb = {rgb}")
            print(f"hsv = {h} {s} {v}")
            requests.get(f"http://{self._ip}/led?brig={int(v)}&h={int(h)}&s={int(s)}")
        except:
            pass

    def check_is_video_capture(self, cap):
        try:
            response = requests.get(cap, timeout=5)
            self._is_video_capture = False
            self._cap = cap
        except:
            self._is_video_capture = True
            self._cap = cv2.VideoCapture(cap)
        self.synchronize_data()
        # except ConnectionError:
        #     self._is_video_capture = True
        #     self._cap = cv2.VideoCapture(cap)

    def get_cap(self):
        return self._cap

    def get_frame(self):
        get_frame_time = time.time()
        logging.info("Отправлен запрос на получении кадра")
        if not self._is_video_capture:
            timer = time.time()
            try:
                response = requests.get(self._cap, timeout=20)
            except requests.exceptions.Timeout:
                logging.critical("Запрос на получение кадра esp32 превысил время ожидания")
            except requests.exceptions.RequestException as e:
                logging.critical(f"Произошла в запросе на получение кадра esp32: {e}")

            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            time_get_frame = time.time() - timer
            fps = 1 / time_get_frame
            logging.info("Был получен кадр от esp32")
            is_camera = True
        else:
            fps = self._cap.get(cv2.CAP_PROP_FPS)
            ret, frame = self._cap.read()
            if ret:
                logging.info("Был получен кадр через cap.read()")
            else:
                logging.error(f"Ошибка в получении кадра cap.read()")
            is_camera = False
        return frame, fps, is_camera

    def get_name(self):
        if self._is_video_capture:
            logging.error(f"Ошибка получения имени esp32\nhttp://{self._ip}/get_name")
            return
        try:
            logging.info(f"Был получен кадр по урлу:\nhttp://{self._ip}/get_name")
            return requests.get(f"http://{self._ip}/get_name")
        except Exception as e:
            logging.critical(f"Ошибка получения имени esp32\n{e}\http://{self._ip}/get_name")
            return None

    def get_color_rgb(self):
        logging.info(f"Был получен цвет RGB с esp32 {self._color_rgb}")
        return self._color_rgb

    def get_temperature(self):
        logging.info(f"Отправлен запрос на получение значение температуры")
        if self._is_video_capture:
            return
        try:
            temperature = requests.get(f"http://{self._ip}/get_sensors")
            temperature = json.loads(temperature.content).get('temp', None)
            logging.info(f"Была получена температура {temperature}\nurl: http://{self._ip}/get_sensors")
            if temperature == -127.0:
                temperature = None
            return temperature
        except:
            logging.error(f"Сбой в получении значении температуры")
            pass

    def set_ip(self, value):
        logging.info(f"Был установлен ip адрес для опроса: {value}")
        self._ip = value
        self.synchronize_data()

    def get_ip(self):
        logging.info(f"Получен запрос ip: {self._ip}")
        return self._ip

    def set_led_params_hsv(self, h, s, v):
        logging.info(f"Отправлен запрос на изменение цвета esp32\nurl: {self._ip}/led?brig={v}&h={h}&s={s}")
        requests.get(f"{self._ip}/led?brig={v}&h={h}&s={s}")

    def set_led_params_rgb(self, r, g, b):
        rgb_color = (r, g, b)
        hsv_color = colorsys.rgb_to_hsv(*rgb_color)
        h, s, v = hsv_color
        logging.info(f"Отправлен запрос на изменение цвета esp32\nurl: {self._ip}/led?brig={v}&h={h}&s={s}")
        requests.get(f"{self._ip}/led?brig={v}&h={h}&s={s}")
