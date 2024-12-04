import json
import time

import cv2
import numpy as np
import requests
import colorsys
import logging


class APIController:
    _ip = None
    _color_rgb = None
    _cap = None
    _is_video_capture: bool = False
    _conn_multiprocessing = None

    @classmethod
    def get_all_data(cls):
        return cls._ip, cls._color_rgb, cls._cap, cls._is_video_capture

    @classmethod
    def set_all_data(cls, data):
        cls._ip, cls._color_rgb, cls._cap, cls._is_video_capture = data

    @classmethod
    def set_conn_multiprocessing(cls, conn):
        cls._conn_multiprocessing = conn

    @classmethod
    def synchronize_data(cls):
        if cls._conn_multiprocessing is not None:
            cls._conn_multiprocessing.send((cls.get_all_data(), 'APIController_data'))

    @classmethod
    def set_is_video_capture(cls, state: bool):
        cls._is_video_capture = state
        cls.synchronize_data()

    @classmethod
    def get_is_video_capture(cls):
        return cls._is_video_capture

    @classmethod
    def set_color_rgb(cls, rgb):
        if cls._is_video_capture:
            return
        cls._color_rgb = rgb
        cls.synchronize_data()
        print(rgb)
        # hsv_color = colorsys.rgb_to_hsv(*cls._color_rgb)
        # h, s, v = hsv_color
        h, s, v = [x for x in
                   colorsys.rgb_to_hsv(cls._color_rgb[0] / 255, cls._color_rgb[1] / 255, cls._color_rgb[2] / 255)]
        h *= 255
        s *= 255
        v *= 255
        try:
            print(f"rgb = {rgb}")
            print(f"hsv = {h} {s} {v}")
            requests.get(f"http://{cls._ip}/led?brig={int(v)}&h={int(h)}&s={int(s)}")
        except:
            pass

    @classmethod
    def check_is_video_capture(cls, cap):
        try:
            response = requests.get(cap, timeout=5)
            cls._is_video_capture = False
            cls._cap = cap
        except:
            cls._is_video_capture = True
            cls._cap = cv2.VideoCapture(cap)
        cls.synchronize_data()
        # except ConnectionError:
        #     cls._is_video_capture = True
        #     cls._cap = cv2.VideoCapture(cap)

    @classmethod
    def get_cap(cls):
        return cls._cap

    @classmethod
    def get_frame(cls):
        get_frame_time = time.time()
        logging.info("Отправлен запрос на получении кадра")
        if not cls._is_video_capture:
            timer = time.time()
            try:
                response = requests.get(cls._cap, timeout=20)
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
            fps = cls._cap.get(cv2.CAP_PROP_FPS)
            ret, frame = cls._cap.read()
            if ret:
                logging.info("Был получен кадр через cap.read()")
            else:
                logging.error(f"Ошибка в получении кадра cap.read()")
            is_camera = False
        return frame, fps, is_camera

    @classmethod
    def get_name(cls):
        if cls._is_video_capture:
            logging.error("Ошибка получения имени esp32\nhttp://{cls._ip}/get_name")
            return
        try:
            logging.info(f"Был получен кадр по урлу:\nhttp://{cls._ip}/get_name")
            return requests.get(f"http://{cls._ip}/get_name")
        except Exception as e:
            logging.critical(f"Ошибка получения имени esp32\n{e}\http://{cls._ip}/get_name")
            return None

    @classmethod
    def get_color_rgb(cls):
        logging.info(f"Был получен цвет RGB с esp32 {cls._color_rgb}")
        return cls._color_rgb

    @classmethod
    def get_temperature(cls):
        logging.info(f"Отправлен запрос на получение значение температуры")
        if cls._is_video_capture:
            return
        try:
            temperature = requests.get(f"http://{cls._ip}/get_sensors")
            temperature = json.loads(temperature.content).get('temp', None)
            logging.info(f"Была получена температура {temperature}\nurl: http://{cls._ip}/get_sensors")
            if temperature == -127.0:
                temperature = None
            return temperature
        except:
            logging.error(f"Сбой в получении значении температуры")
            pass

    @classmethod
    def set_ip(cls, value):
        logging.info(f"Был установлен ip адрес для опроса: {value}")
        cls._ip = value
        cls.synchronize_data()

    @classmethod
    def get_ip(cls):
        logging.info(f"Получен запрос ip: {cls._ip}")
        return cls._ip

    @classmethod
    def set_led_params_hsv(cls, h, s, v):
        logging.info(f"Отправлен запрос на изменение цвета esp32\nurl: {cls._ip}/led?brig={v}&h={h}&s={s}")
        requests.get(f"{cls._ip}/led?brig={v}&h={h}&s={s}")

    @classmethod
    def set_led_params_rgb(cls, r, g, b):
        rgb_color = (r, g, b)
        hsv_color = colorsys.rgb_to_hsv(*rgb_color)
        h, s, v = hsv_color
        logging.info(f"Отправлен запрос на изменение цвета esp32\nurl: {cls._ip}/led?brig={v}&h={h}&s={s}")
        requests.get(f"{cls._ip}/led?brig={v}&h={h}&s={s}")
