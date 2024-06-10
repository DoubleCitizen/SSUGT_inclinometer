import requests
import colorsys


class APIController:
    _ip = None
    _color_rgb = None

    @classmethod
    def set_color_rgb(cls, rgb):
        cls._color_rgb = rgb
        hsv_color = colorsys.rgb_to_hsv(*cls._color_rgb)
        h, s, v = hsv_color
        try:
            requests.get(f"http://{cls._ip}/led?brig={v}&h={h}&s={s}")
        except:
            pass

    @classmethod
    def get_color_rgb(cls):
        return cls._color_rgb

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

