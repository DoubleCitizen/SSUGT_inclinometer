import argparse
import sys
import time
from typing import Optional

import numpy as np
from datetime import datetime

import cv2

from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.segmentation_base import SegmentationBase
from classes.value_saver import FileSaver

segmentation = SegmentationBase()

def start_processing(file_path: str, count_draw_points: int = 1, start_point_px: Optional[float] = None):
    """Starts the video processing to detect bubbles and save coordinates.
    
    Args:
        file_path (str): The video input file name or path.
        count_draw_points (int, optional): The number of points to draw. Defaults to 1.
        start_point_px (Optional[float], optional): Optional start point in pixels to shift coordinate limits. Defaults to None.
    """

    if start_point_px is not None:
        CoordinateSystemOffset.set_start_position(start_point_px)

    # Set video file name
    video_input_file_name = file_path


    # Create object to read video
    try:
        video = cv2.VideoCapture(video_input_file_name)
    except:
        print("Could not open video")
        return
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    file_saver = FileSaver()

    # Check if video file opened successfully
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    time_1 = time.time()
    is_first_frame = False

    current_frame = 0
    time_sec_sum = 0

    while True:
        # Read frame from video
        time_2 = time.time()
        ok, frame = video.read()

        # If frame cannot be read, video has ended
        if not ok:
            break
        center_bubbles_px = None
        points = None
        try:
            image = frame
            points, image, center_bubbles_px = segmentation.vim_frame_processing(image, count_draw_points=count_draw_points)
            points, image, center_bubbles_px = CoordinateSystemOffset.get_new_image_coords(points, image,
                                                                                           center_bubbles_px)
        except Exception as e:
            # print(e)
            pass


        current_frame += 1

        remaining_percentage = 100 - ((total_frames - current_frame) / total_frames * 100)
        remaining_time = (time_sec_sum / current_frame) * (total_frames - current_frame)
        print(f"\rRemaining time: {remaining_time:.2f} sec. {remaining_percentage:.2f}%", end="")
        # time.sleep(0.0000000001)

        if not is_first_frame:
            file_saver.initialize(
                headers=['time', 'center_bubbles_px', 'points'],
                sep=';')
            is_first_frame = True

        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S.%f")
        if points is not None and isinstance(points, np.ndarray):
            points = points.tolist()
        file_saver.write_data(
            [formatted_time, center_bubbles_px, str(points)])
        time_sec_sum += time.time() - time_2

    print(f"\rTime taken = {(time.time() - time_1):.2f} seconds", end="")

    # Release resources
    video.release()


# if __name__ == "__main__":
#     start_processing("C:\\Users\\26549\\PycharmProjects\\SSUGT_inclinometer\\3.mp4", 1, None)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video file processing for bubble analysis.")

    # Positional argument: path to video file
    parser.add_argument("--file_path", type=str, help="Path to video file (data type: str)")

    # Optional arguments
    parser.add_argument("--count_draw_points", type=int, default=1,
                        help="Number of points to draw (data type: int, default: 1)")
    parser.add_argument("--start_point_px", type=float, default=None,
                        help="Start position in pixels (data type: float, default: None)")

    # Parse arguments
    args = parser.parse_args()

    # Start processing
    start_processing(
        file_path=args.file_path,
        count_draw_points=args.count_draw_points,
        start_point_px=args.start_point_px
    )