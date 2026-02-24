import json
import time

import cv2
import numpy as np
import requests
import colorsys
import logging


class APIController:
    """Controller for handling API interactions with ESP32 modules.
    
    Attributes:
        _ip (str): IP address of the ESP32 module.
        _color_rgb (tuple): Current RGB color tuple.
        _cap (cv2.VideoCapture | str): Video capture object or stream URL.
        _is_video_capture (bool): Flag indicating if the source is a direct video capture.
        _conn_multiprocessing (multiprocessing.Connection): Connection for multiprocessing synchronization.
    """
    def __init__(self):
        """Initializes the APIController with default attributes."""
        self._ip = None
        self._color_rgb = None
        self._cap = None
        self._is_video_capture: bool = False
        self._conn_multiprocessing = None

    def get_all_data(self):
        """Retrieves all core data attributes.
        
        Returns:
            tuple: A tuple containing (ip, color_rgb, cap, is_video_capture).
        """
        return self._ip, self._color_rgb, self._cap, self._is_video_capture

    def set_all_data(self, data):
        """Sets all core data attributes.
        
        Args:
            data (tuple): A tuple containing (ip, color_rgb, cap, is_video_capture).
        """
        self._ip, self._color_rgb, self._cap, self._is_video_capture = data

    def set_conn_multiprocessing(self, conn):
        """Sets the multiprocessing connection.
        
        Args:
            conn (multiprocessing.Connection): The connection object.
        """
        self._conn_multiprocessing = conn

    def synchronize_data(self):
        """Synchronizes controller data via multiprocessing connection."""
        if self._conn_multiprocessing is not None:
            self._conn_multiprocessing.send((self.get_all_data(), 'APIController_data'))

    def set_is_video_capture(self, state: bool):
        """Sets the flag indicating if the source is a direct video capture.
        
        Args:
            state (bool): True if using video capture, False if HTTP stream.
        """
        self._is_video_capture = state
        self.synchronize_data()

    def get_is_video_capture(self):
        """Gets the video capture flag.
        
        Returns:
            bool: Video capture flag status.
        """
        return self._is_video_capture

    def set_color_rgb(self, rgb):
        """Sets the RGB color.
        
        Args:
            rgb (tuple): Tuple of RGB values (r, g, b).
        """
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
        """Checks if the video stream URL is accessible, falling back to cv2.VideoCapture.
        
        Args:
            cap (str): Video capture stream URL.
        """
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
        """Retrieves the video capture object or URL.
        
        Returns:
            cv2.VideoCapture | str | None: The active capture source.
        """
        return self._cap

    def get_frame(self):
        """Retrieves a single frame from the video capture or ESP32 stream.
        
        Returns:
            tuple: A tuple containing the frame (np.ndarray), FPS (float), and is_camera (bool) flag.
        """
        get_frame_time = time.time()
        logging.info("Request for frame acquisition sent")
        if not self._is_video_capture:
            timer = time.time()
            try:
                response = requests.get(self._cap, timeout=20)
            except requests.exceptions.Timeout:
                logging.critical("ESP32 frame acquisition request timed out")
            except requests.exceptions.RequestException as e:
                logging.critical(f"Error occurred during ESP32 frame acquisition request: {e}")

            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            time_get_frame = time.time() - timer
            fps = 1 / time_get_frame
            logging.info("Received frame from ESP32")
            is_camera = True
        else:
            fps = self._cap.get(cv2.CAP_PROP_FPS)
            ret, frame = self._cap.read()
            if ret:
                logging.info("Received frame via cap.read()")
            else:
                logging.error(f"Error receiving frame via cap.read()")
            is_camera = False
        return frame, fps, is_camera

    def get_name(self):
        """Retrieves the name of the ESP32 module.

        Returns:
            requests.Response | None: Response object containing the name, or None if failed.
        """
        if self._is_video_capture:
            logging.error(f"Error receiving ESP32 name\nhttp://{self._ip}/get_name")
            return
        try:
            logging.info(f"Received frame from URL:\nhttp://{self._ip}/get_name")
            return requests.get(f"http://{self._ip}/get_name")
        except Exception as e:
            logging.critical(f"Error receiving ESP32 name\n{e}\nhttp://{self._ip}/get_name")
            return None

    def get_color_rgb(self):
        """Retrieves the current RGB color.

        Returns:
            tuple: Current RGB color.
        """
        logging.info(f"Received RGB color from ESP32 {self._color_rgb}")
        return self._color_rgb

    def get_temperature(self):
        """Retrieves the temperature from the ESP32 module.

        Returns:
            float | None: Temperature value, or None if unavailable/failed.
        """
        logging.info(f"Request sent to get temperature value")
        if self._is_video_capture:
            return
        try:
            temperature = requests.get(f"http://{self._ip}/get_sensors")
            temperature = json.loads(temperature.content).get('temp', None)
            logging.info(f"Received temperature {temperature}\nurl: http://{self._ip}/get_sensors")
            if temperature == -127.0:
                temperature = None
            return temperature
        except:
            logging.error(f"Failed to get temperature value")
            pass

    def set_ip(self, value):
        """Sets the IP address for the module.

        Args:
            value (str): The IP address.
        """
        logging.info(f"IP address set for polling: {value}")
        self._ip = value
        self.synchronize_data()

    def get_ip(self):
        """Retrieves the current IP address.

        Returns:
            str: IP address.
        """
        logging.info(f"Received IP request: {self._ip}")
        return self._ip

    def set_led_params_hsv(self, h, s, v):
        """Sets the LED color using HSV parameters.

        Args:
            h (int): Hue value.
            s (int): Saturation value.
            v (int): Value/Brightness.
        """
        logging.info(f"Request sent to change ESP32 color\nurl: {self._ip}/led?brig={v}&h={h}&s={s}")
        requests.get(f"{self._ip}/led?brig={v}&h={h}&s={s}")

    def set_led_params_rgb(self, r, g, b):
        """Sets the LED color using RGB parameters by converting to HSV.

        Args:
            r (int): Red value.
            g (int): Green value.
            b (int): Blue value.
        """
        rgb_color = (r, g, b)
        hsv_color = colorsys.rgb_to_hsv(*rgb_color)
        h, s, v = hsv_color
        logging.info(f"Request sent to change ESP32 color\nurl: {self._ip}/led?brig={v}&h={h}&s={s}")
        requests.get(f"{self._ip}/led?brig={v}&h={h}&s={s}")
