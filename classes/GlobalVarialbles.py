from datetime import timedelta


class GlobalVariables:
    _time_static = 0
    _indicator_value = None

    @classmethod
    def set_indicator_value(cls, value):
        cls._indicator_value = value

    @classmethod
    def get_indicator_value(cls):
        return cls._indicator_value

    @classmethod
    def add_time_static(cls, seconds):
        cls._time_static += seconds

    @classmethod
    def set_time_static(cls, seconds):
        cls._time_static = seconds

    @classmethod
    def get_time_static(cls):
        return cls._time_static

    @classmethod
    def get_str_time_static(cls):
        minutes, seconds = divmod(cls._time_static, 60)
        text_time = f"{minutes:02d}:{seconds:02d}"
        return text_time
