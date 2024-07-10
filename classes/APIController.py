import json

import requests
import colorsys


class APIController:
    _ip = None
    _color_rgb = None

    @classmethod
    def set_color_rgb(cls, rgb):
        cls._color_rgb = rgb
        print(rgb)
        # hsv_color = colorsys.rgb_to_hsv(*cls._color_rgb)
        # h, s, v = hsv_color
        h, s, v = [x for x in colorsys.rgb_to_hsv(cls._color_rgb[0]/255,cls._color_rgb[1]/255,cls._color_rgb[2]/255)]
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
    def get_name(cls):
        try:
            requests.get(f"http://{cls._ip}/get_name")
        except:
            pass

    @classmethod
    def get_color_rgb(cls):
        return cls._color_rgb

    @classmethod
    def get_temperature(cls):
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
