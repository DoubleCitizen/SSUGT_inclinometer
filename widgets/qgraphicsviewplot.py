import math

import cv2
import numpy as np
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QPolygonF, QPen, QColor
from PySide6.QtWidgets import QSizePolicy, QGraphicsPolygonItem, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class QGraphicsViewPlot(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Create a matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.figure)

        # Wrap the canvas in a proxy widget
        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(self.canvas)

        # Add the proxy widget to the scene
        self.scene.addItem(self.proxy)

    @QtCore.Slot(float, float, float)
    def draw_parabola(self, a, b, c):
        # Коэффициенты параболы
        self.ax.clear()

        # Генерация значений x
        D = abs(b ** 2 - 4 * a * c)
        x1 = (-b ** 2 - math.sqrt(D)) / (2 * a)
        x2 = (-b ** 2 + math.sqrt(D)) / (2 * a)
        x = np.linspace(x1, x2, 400)

        # Вычисление значений y по общему уравнению параболы
        y = a * x ** 2 + b * x + c

        # Построение параболы
        self.ax.plot(x, y, label=f'{a}x^2 + {b}x + {c}')
        #
        # # Добавление заголовка и подписей осей
        self.ax.set_title('Парабола: общее уравнение')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        # Обновление холста
        self.canvas.draw()

        # Ensure the event loop continues
        QtWidgets.QApplication.processEvents()

    def update_plot(self):
        self.scene.clear()
        if self.qImg is not None:
            self.pixmap = QPixmap.fromImage(self.qImg)
        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        self.drawPolygon()
        self.fitInView(self.pixmapItem, QtCore.Qt.KeepAspectRatio)
