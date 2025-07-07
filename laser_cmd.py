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

def start_processing(file_path: str, start_point_px: Optional[float] = None):

    if start_point_px is not None:
        CoordinateSystemOffset.set_start_position(start_point_px)

    # Установка имени видеофайла
    video_input_file_name = file_path


    # Создание объекта для чтения видео
    try:
        video = cv2.VideoCapture(video_input_file_name)
    except:
        print("Could not open video")
        return
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    file_saver = FileSaver()

    # Проверка на успешное открытие видеофайла
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    time_1 = time.time()
    is_first_frame = False

    current_frame = 0
    time_sec_sum = 0

    while True:
        # Чтение кадра из видео
        time_2 = time.time()
        ok, frame = video.read()

        # Если кадр не может быть прочитан, то видео закончилось
        if not ok:
            break
        center_bubbles_px = None
        points = None
        try:
            image = frame
            points, image, center_bubbles_px = segmentation.laser_frame_processing(image)
            points, image, center_bubbles_px = CoordinateSystemOffset.get_new_image_coords(points, image,
                                                                                           center_bubbles_px)
        except Exception as e:
            # print(e)
            pass


        current_frame += 1

        remaining_percentage = 100 - ((total_frames - current_frame) / total_frames * 100)
        remaining_time = (time_sec_sum / current_frame) * (total_frames - current_frame)
        print(f"\rОставшееся время: {remaining_time:.2f} сек. {remaining_percentage:.2f}%", end="")
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

    print(f"\rВремя заняло = {(time.time() - time_1):.2f} секунд", end="")

    # Освобождение ресурсов
    video.release()


# if __name__ == "__main__":
#     start_processing("C:\\Users\\26549\\PycharmProjects\\SSUGT_inclinometer\\3.mp4", 1, None)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка видеофайла для анализа пузырьков.")

    # Позиционный аргумент: путь к видеофайлу
    parser.add_argument("--file_path", type=str, help="Путь к видеофайлу (тип данных: str)")

    # Опциональные аргументы
    parser.add_argument("--start_point_px", type=float, default=None,
                        help="Начальная позиция в пикселях (тип данных: float, по умолчанию: None)")

    # Парсим аргументы
    args = parser.parse_args()

    # Запускаем обработку
    start_processing(
        file_path=args.file_path,
        start_point_px=args.start_point_px
    )