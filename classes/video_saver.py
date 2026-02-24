import os
from datetime import datetime

import cv2


class VideoSaver:
    """Handles continuous video frame recording to AVI files.
    
    Attributes:
        _out (cv2.VideoWriter | None): File writer hook for cv2.
        _name (str): Core filename identifier for exports.
        _is_recording (bool): Flags if writer actively commits.
        width (int): Target frame width.
        height (int): Target frame height.
        fps (int): Export metadata framerate bounds.
    """
    def __init__(self, name):
        """Initializes VideoSaver structure.
        
        Args:
            name (str): Project or run name identifier string.
        """
        self._out = None
        self._name = name
        self._is_recording = False
        self.width = 0
        self.height = 0
        self.fps = 30

    def get_out(self):
        """Retrieves underlying video writer instance.
        
        Returns:
            cv2.VideoWriter | None: Active VideoWriter or None if inactive.
        """
        return self._out

    def get_record_status(self):
        """Checks if a recording session is currently active.
        
        Returns:
            bool: Recording active status.
        """
        return self._is_recording

    @staticmethod
    def create_directory(folder_path):
        """Ensures an output directory is present, creating hierarchy if needed.
        
        Args:
            folder_path (str): The desired directory path to initialize.
        """
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return
        else:
            os.makedirs(folder_path)

    def initialize(self, fps, width, height):
        """Bootstraps a cv2.VideoWriter and configures the target file layout.
        
        Args:
            fps (float): Write framerate target.
            width (int): Frame capture width bounding box.
            height (int): Frame capture height bounding box.
        """
        # Get current time
        current_time = datetime.now()
        self.fps = fps
        self.width = width
        self.height = height

        # Format time into string format
        formatted_time = current_time.strftime("%Y_%m_%d %H_%M_%S")
        current_directory = os.getcwd()
        self.create_directory(current_directory.replace('\\', '/') + '/data')

        filename = current_directory + f"/data/{self._name}-" + formatted_time + ".avi"

        # fourcc = cv2.VideoWriter_fourcc(*'avc1')
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self._out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    def write_frame(self, frame):
        """Encodes and streams a single frame out to the video file.
        
        Args:
            frame (np.ndarray): The image array buffer.
        """
        self._is_recording = True
        self._out.write(frame)

    def release(self):
        """Finalizes the output stream cleanly, unlocking the file."""
        if self._out is None:
            return
        self._out.release()
        self._out = None
        self._is_recording = False
