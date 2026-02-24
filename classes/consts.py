class SpeedFrame:
    """Constants regarding speed frame metrics modes."""
    MODE_HZ = 0
    MODE_SECONDS_PER_FRAME = 1


class ProcessVIM:
    """Constants defining thread process keys and events."""
    PROCESS_ID = 'process_id'
    API_CONTROLLER_DATA = 'APIController_data'
    DATA_FRAME_VIM = 'DATA_FRAME_VIM'
    DATA_FRAME_LASER = 'DATA_FRAME_LASER'
    VIDEO_IS_OVER = 'VIDEO_IS_OVER'
    KILL_PROCESS = 'kill_process'
    IS_SEGMENTATION_SHOW = 'IS_SEGMENTATION_SHOW'
    IS_DRAW_RECTANGLE = 'IS_DRAW_RECTANGLE'
    IS_DRAW_POINTS = 'IS_DRAW_POINTS'
    COUNT_DRAW_POINTS = 'COUNT_DRAW_POINTS'
    DRAW_OPTIONS = 'DRAW_OPTIONS'

class TypeDevices:
    """Constants defining connected device types."""
    ESP32_VIM = 'ESP32_VIM'
    ESP32_LASER = 'ESP32_LASER'