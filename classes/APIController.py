import json
import time

import cv2
import numpy as np
import requests
import colorsys

from requests.exceptions import MissingSchema

from classes.GlobalController import GlobalController


class APIController:
    _ip = None
    _color_rgb = None
    _cap = None
    _is_video_capture: bool = False

    @classmethod
    def set_is_video_capture(cls, state: bool):
        cls._is_video_capture = state

    @classmethod
    def get_is_video_capture(cls):
        return cls._is_video_capture

    @classmethod
    def set_color_rgb(cls, rgb):
        if cls._is_video_capture:
            return
        cls._color_rgb = rgb
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

        # except ConnectionError:
        #     cls._is_video_capture = True
        #     cls._cap = cv2.VideoCapture(cap)

    @classmethod
    def get_cap(cls):
        return cls._cap

    @classmethod
    def get_frame(cls):
        if not cls._is_video_capture:
            timer = time.time()
            response = requests.get(cls._cap, timeout=5)

            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            time_get_frame = time.time() - timer
            fps = 1 / time_get_frame
        else:
            fps = cls._cap.get(cv2.CAP_PROP_FPS)
            ret, frame = cls._cap.read()

        return frame, fps

    @classmethod
    def get_name(cls):
        if cls._is_video_capture:
            return
        try:
            return requests.get(f"http://{cls._ip}/get_name")
        except:
            return None

    @classmethod
    def get_color_rgb(cls):
        return cls._color_rgb

    @classmethod
    def get_temperature(cls):
        if cls._is_video_capture:
            return
        try:
            temperature = requests.get(f"http://{cls._ip}/get_sensors")
            temperature = json.loads(temperature.content).get('temp', None)
            if temperature == -127.0:
                temperature = None
            return temperature
        except:
            pass

    @classmethod
    def set_ip(cls, value):
        cls._ip = value

    @classmethod
    def get_ip(cls):
        return cls._ip

    @classmethod
    def set_led_params_hsv(cls, h, s, v):
        requests.get(f"{cls._ip}/led?brig={v}&h={h}&s={s}")

    @classmethod
    def set_led_params_rgb(cls, r, g, b):
        rgb_color = (r, g, b)
        hsv_color = colorsys.rgb_to_hsv(*rgb_color)
        h, s, v = hsv_color
        requests.get(f"{cls._ip}/led?brig={v}&h={h}&s={s}")
