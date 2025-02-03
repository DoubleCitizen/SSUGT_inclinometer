import sys
import time
from datetime import datetime

import cv2

from classes.coordinate_system_offset import CoordinateSystemOffset
from classes.segmentation_base import SegmentationBase
from classes.value_saver import FileSaver

segmentation = SegmentationBase()

def start_processing(file_path, signal_progressbar, signal_time_label):

    # Установка имени видеофайла
    video_input_file_name = file_path


    # Создание объекта для чтения видео
    try:
        video = cv2.VideoCapture(video_input_file_name)
    except:
        signal_progressbar.emit(400)
        return
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    file_saver = FileSaver()

    # Проверка на успешное открытие видеофайла
    if not video.isOpened():
        print("Could not open video")
        signal_progressbar.emit(400)
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
            points, image, center_bubbles_px = segmentation.vim_frame_processing(image)
            points, image, center_bubbles_px = CoordinateSystemOffset.get_new_image_coords(points, image,
                                                                                           center_bubbles_px)
        except Exception as e:
            print(e)


        current_frame += 1

        remaining_percentage = 100 - ((total_frames - current_frame) / total_frames * 100)
        remaining_time = (time_sec_sum / current_frame) * (total_frames - current_frame)
        signal_time_label.emit(remaining_time)
        # print(f"Оставшееся время: {remaining_time:.2f} секунд")
        time.sleep(0.0000000001)

        # print(f"Оставшиеся кадры: {remaining_percentage:.2f}%")
        signal_progressbar.emit(round(remaining_percentage))

        if not is_first_frame:
            file_saver.initialize(
                headers=['time', 'center_bubbles_px', 'points'],
                sep=';')
            is_first_frame = True

        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S.%f")
        if points is not None:
            points = points.tolist()
        file_saver.write_data(
            [formatted_time, center_bubbles_px, str(points)])
        time_sec_sum += time.time() - time_2

    print(f"Время заняло = {time.time() - time_1} секунд")

    # Освобождение ресурсов
    video.release()
    signal_progressbar.emit(400)
