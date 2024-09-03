import cv2
import numpy as np
from matplotlib import pyplot as plt

from classes.GlobalController import GlobalController


class SegmentationBase:
    def __init__(self):
        self.crop_x = 0
        self.crop_y = 0
        self.crop_w = 0
        self.crop_h = 0

    @staticmethod
    def delete_polygons(image):
        # Находим контуры на бинарном изображении
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Инициализация переменных для хранения максимальной площади и соответствующего контура
        max_area = 0
        max_contour = None

        # Перебор контуров для нахождения самого большого
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        # Создание копии исходного изображения для вывода результата
        result = image.copy()

        # Закрашивание всех контуров, кроме самого большого, в черный цвет
        for contour in contours:
            if contour is not max_contour:
                cv2.drawContours(result, [contour], 0, 0, -1)
        return result, max_contour

    @staticmethod
    def delete_closers_contours(cropped_image, edges, contours):
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=9)
        # Находжение контуров
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Минимальная площадь контура
        max_area = float(0)

        height_img, width_img = edges.shape[:2]

        # Список контуров, которые нужно сохранить
        valid_contours = []
        idx = 0
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            print(area)
            if x < width_img * 0.15:
                continue
            if y < height_img * 0.1:
                continue
            if x + w > width_img * 0.85:
                continue
            if y + h > height_img * 0.9:
                continue
            if area > max_area:
                max_area = area
                idx = i
                # valid_contours.append(c)

        # Вывод результата
        result = edges.copy() * 0
        c = contours[idx]
        cv2.drawContours(result, [c], -1, (255, 255, 255), 2)
        # cv2.drawContours(result, contours, -1, (255, 255, 255), 2)
        # cv2.drawContours()

        return result

    def v2_frame_proccesing(self, frame_original):
        frame_original.copy()
        frame = cv2.cvtColor(frame_original, cv2.COLOR_BGR2GRAY)
        frame = cv2.medianBlur(frame, 5)
        ret_th, thresh = cv2.threshold(frame, 0, 255, cv2.THRESH_OTSU)

        thresh, max_contour = self.delete_polygons(thresh)
        x, y, w, h = cv2.boundingRect(max_contour)
        cropped_image = frame[y:y + h, x:x + w]  # обрезка изображения
        ret_th, thresh = cv2.threshold(cropped_image, 0, 255, cv2.THRESH_OTSU)
        # edges = cv2.Canny(cropped_image, 100, 200)
        v = np.median(cropped_image)
        sigma = 0.33
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        # Применение функции Canny с автоматически определёнными порогами
        edges = cv2.Canny(cropped_image, lower, upper)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(edges, contours, 0, 0, -1)
        result = self.delete_closers_contours(cropped_image, edges, contours)

        return result

    def new_frame_processing(self, frame_original):
        frame_result = frame_original.copy()
        frame = cv2.cvtColor(frame_original, cv2.COLOR_BGR2GRAY)
        ret_th, thresh = cv2.threshold(frame, 0, 255, cv2.THRESH_OTSU)

        # Найти контуры
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # Найти самый большой контур (прямоугольник)
        max_area = 0
        max_contour = None

        for c in cnts:
            area = cv2.contourArea(c)
            if area > max_area:
                max_area = area
                max_contour = c

        # Получить ограничивающий прямоугольник
        x, y, w, h = cv2.boundingRect(max_contour)
        # Условие если новый прямоугольник отличается больше, чем на 10 процентов, тогда мы заменяем значения
        if abs((x - self.crop_x) / (x + self.crop_x)) > 0.1 or abs((y - self.crop_y) / (y + self.crop_y)) > 0.1:
            self.crop_x, self.crop_y, self.crop_w, self.crop_h = x, y, w, h

        x, y, w, h = self.crop_x, self.crop_y, self.crop_w, self.crop_h
        cropped = frame[y:y + h, x:x + w]
        mask = thresh[y:y + h, x:x + w]
        # mask = cv2.bitwise_not(mask)
        cropped[mask == 0] = 255

        # frame_copy = frame.copy()

        # cv2.imshow("frame", frame)
        # Применить медианный фильтр с ядром размером 3x3
        cropped = cv2.medianBlur(cropped, 5)

        ret_th, thresh = cv2.threshold(cropped, 0, 255, cv2.THRESH_OTSU)
        # cv2.imshow("thresh", thresh)

        # Найти контуры
        cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # thresh = cv2.medianBlur(thresh, 5)

        # Найти самый большой контур (прямоугольник)
        area_list = []

        for c in cnts:
            area = cv2.contourArea(c)
            if len(area_list) == 0 or area > area_list[-1][0]:
                area_list.append([area, c])

        height_t, width_t = thresh.shape[:2]
        sorted_area_list = sorted(area_list, key=lambda x: x[0])
        index_delete_later = []
        for i in range(len(sorted_area_list)):
            if sorted_area_list[i][0] > (height_t * width_t) * 0.15:
                index_delete_later.append(i)
            for j in range(len(sorted_area_list[i][1])):
                if abs(sorted_area_list[i][1][j][0][0] - width_t) / width_t < 0.01 or abs(
                        sorted_area_list[i][1][j][0][0] - width_t) / width_t > 0.99:
                    index_delete_later.append(i)
                    break
                if abs(sorted_area_list[i][1][j][0][1] - height_t) / height_t < 0.05 or abs(
                        sorted_area_list[i][1][j][0][1] - height_t) / height_t > 0.95:
                    index_delete_later.append(i)
                    break
        temp_sorted_list = []
        for i in range(len(sorted_area_list)):
            if not i in index_delete_later:
                temp_sorted_list.append(sorted_area_list[i])
        sorted_area_list = temp_sorted_list

        # print(len(sorted_area_list))
        try:
            x, y, w, h = cv2.boundingRect(sorted_area_list[-1][1])
            if len(sorted_area_list) < 3:
                x, y, w, h = cv2.boundingRect(sorted_area_list[-1][1])

        except IndexError:
            try:
                x, y, w, h = cv2.boundingRect(sorted_area_list[-1][1])
            except IndexError:
                print(IndexError)
                return [], frame_original, 0
        cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 0, 0), 1)
        # Создание графика с точками
        # Транспонирование массива
        cv2.drawContours(cropped, sorted_area_list[-1][1], -1, (0, 255, 0), 2)
        # cv2.imshow("cropped", cropped)
        xy_array = sorted_area_list[-1][1]

        transposed_array = np.transpose(xy_array)

        # Разделение транспонированного массива на два массива
        split_array = np.split(transposed_array, 2)

        # Преобразование каждого массива в одномерный
        x_array: np.array = split_array[0].flatten()
        y_array: np.array = split_array[1].flatten()

        x_2, y_2, w_2, h_2 = self.crop_x, self.crop_y, self.crop_w, self.crop_h

        x_array += x_2
        y_array += y_2

        merged_array = np.hstack((x_array.reshape(-1, 1), y_array.reshape(-1, 1)))
        # Получаем индексы отсортированных значений x
        sorted_indices = np.argsort(merged_array[:, 0])

        # Сортируем merged_array по значениям x
        sorted_merged_array = merged_array[sorted_indices]

        x, y, w, h = x + x_2, y + y_2, w, h
        new_frame = None
        if GlobalController.is_segmentaion_show():
            new_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        if GlobalController.is_draw_rectangle():
            if new_frame is None:
                new_frame = cv2.rectangle(frame_original, (x, y), (x + w, y + h), (0, 255, 0), 5)
            else:
                new_frame = cv2.rectangle(new_frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
        if GlobalController.is_draw_points():
            if new_frame is None:
                new_frame = frame_original

            for i in range(0, x_array.shape[0], GlobalController.get_spinBox_points().value()):
                x_cir = x_array[i]
                y_cir = y_array[i]
                radius = 5
                color = (255, 0, 0)
                thickness = 2
                new_frame = cv2.circle(new_frame, (x_cir, y_cir), radius, color, thickness)
        if new_frame is not None:
            frame_result = new_frame

        center_bubbles_px = (x + (x + w)) / 2

        return sorted_merged_array, frame_result, center_bubbles_px

    def frame_processing(self, frame_original, draw_rect=False, draw_segm=False):
        frame_result = frame_original.copy()
        frame = cv2.cvtColor(frame_original, cv2.COLOR_BGR2GRAY)
        ret_th, thresh = cv2.threshold(frame, 0, 255, cv2.THRESH_OTSU)

        # Найти контуры
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # Найти самый большой контур (прямоугольник)
        max_area = 0
        max_contour = None

        for c in cnts:
            area = cv2.contourArea(c)
            if area > max_area:
                max_area = area
                max_contour = c

        # Получить ограничивающий прямоугольник
        x, y, w, h = cv2.boundingRect(max_contour)
        # Условие если новый прямоугольник отличается больше, чем на 10 процентов, тогда мы заменяем значения
        if abs((x - self.crop_x) / (x + self.crop_x)) > 0.1 or abs((y - self.crop_y) / (y + self.crop_y)) > 0.1:
            self.crop_x, self.crop_y, self.crop_w, self.crop_h = x, y, w, h

        x, y, w, h = self.crop_x, self.crop_y, self.crop_w, self.crop_h
        cropped = frame[y:y + h, x:x + w]
        mask = thresh[y:y + h, x:x + w]
        # mask = cv2.bitwise_not(mask)
        cropped[mask == 0] = 255

        # frame_copy = frame.copy()

        # cv2.imshow("frame", frame)
        # Применить медианный фильтр с ядром размером 3x3
        cropped = cv2.medianBlur(cropped, 5)

        ret_th, thresh = cv2.threshold(cropped, 0, 255, cv2.THRESH_OTSU)

        # Найти контуры
        cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # thresh = cv2.medianBlur(thresh, 5)

        # Найти самый большой контур (прямоугольник)
        max_area = 0
        max_area_2 = 0
        max_contour = None
        area_list = []

        for c in cnts:
            area = cv2.contourArea(c)
            if len(area_list) == 0 or area > area_list[-1][0]:
                # max_area = area
                # max_contour = c
                area_list.append([area, c])

        sorted_area_list = sorted(area_list, key=lambda x: x[0])
        try:
            x, y, w, h = cv2.boundingRect(sorted_area_list[-3][1])
            if len(sorted_area_list) < 3:
                x, y, w, h = cv2.boundingRect(sorted_area_list[-2][1])

        except IndexError:
            x, y, w, h = cv2.boundingRect(sorted_area_list[0][1])
        cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 0, 0), 1)
        # x, y, w, h = cv2.boundingRect(sorted_area_list[-3][1])
        # cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 0, 0), 2)
        # Создание графика с точками
        # Транспонирование массива
        cv2.drawContours(cropped, sorted_area_list[-3][1], -1, (0, 255, 0), 2)
        xy_array = sorted_area_list[-3][1]

        condition = xy_array[1] < 65

        # находим индексы элементов, которые соответствуют условию
        indices = np.where(condition)[0]

        # удаляем элементы из массива A по найденным индексам
        # xy_array = np.delete(xy_array, indices)
        # new_xy_array = np.array([])
        # for xy in xy_array:
        #     if xy[0][1] > 65:
        #         new_xy_array = np.append(new_xy_array, xy[0])
        # # print(new_xy_array)
        # xy_array = new_xy_array

        # xy_array = np.where(xy_array[1] < 65, xy_array, xy_array )
        reshaped_data = xy_array.reshape(-1, xy_array.shape[-1])
        # np.savetxt('data.csv', reshaped_data, delimiter=',')
        transposed_array = np.transpose(xy_array)

        # Разделение транспонированного массива на два массива
        split_array = np.split(transposed_array, 2)

        # Преобразование каждого массива в одномерный
        x_array: np.array = split_array[0].flatten()
        y_array: np.array = split_array[1].flatten()
        # plt.scatter(x_array, y_array)
        # plt.xlabel('X')  # подпись оси x
        # plt.ylabel('Y')  # подпись оси y
        # plt.title('Scatter Plot')  # заголовок графика
        # plt.grid(True)  # включение сетки
        # plt.show()  # вывод графика

        # cv2.imshow("frame_copy", cropped)
        # cv2.imshow("frame2", thresh)
        # Обрезка каждого канала отдельно
        x_2, y_2, w_2, h_2 = self.crop_x, self.crop_y, self.crop_w, self.crop_h
        # cropped_blue = frame_original[y_2:y_2 + h_2, x_2:x_2 + w_2, 0]  # Blue channel
        # cropped_green = frame_original[y_2:y_2 + h_2, x_2:x_2 + w_2, 1]  # Green channel
        # cropped_red = frame_original[y_2:y_2 + h_2, x_2:x_2 + w_2, 2]  # Red channel
        #
        # # Объединение каналов в цветное изображение
        # cropped_color = cv2.merge([cropped_blue, cropped_green, cropped_red])
        x, y, w, h = x + x_2, y + y_2, w, h
        if draw_rect and draw_segm:
            frame_result = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            frame_result = cv2.rectangle(frame_result.copy(), (x, y), (x + w, y + h), (0, 255, 0), 5)
        elif draw_rect:
            frame_result = cv2.rectangle(frame_original.copy(), (x, y), (x + w, y + h), (0, 255, 0), 5)
        elif draw_segm:
            frame_result = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        center_bubbles_px = abs(x - (x + w)) / 2

        return x_array, y_array, frame_result, center_bubbles_px


if __name__ == "__main__":
    segm = SegmentationBase()

    vid = cv2.VideoCapture("C:\\Users\\26549\\PycharmProjects\\SSUGT_inclinometer\\1.mkv")

    ret, frame = vid.read()

    segm.new_frame_processing(frame)
