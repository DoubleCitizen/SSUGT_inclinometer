import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPolygonF, QPen, QColor
from PyQt5.QtWidgets import QSizePolicy, QGraphicsPolygonItem
from pyqt5_plugins.examplebutton import QtWidgets
from pyqt5_plugins.examplebuttonplugin import QtGui


class QGraphicsViewVideo(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qImg = None
        self.scene = QtWidgets.QGraphicsScene()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.polygon_points = []

    @QtCore.pyqtSlot(np.ndarray)
    def image_cv(self, frame):
        """ Применение изображения из матрицы OpenCV """
        height, width, channel = frame.shape

        # print(height, width)
        # cv2.imshow("img_rgb", frame)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        qImg = QImage(img_rgb, width, height, QImage.Format_RGB888)
        self.qImg = qImg
        self.scene.clear()
        if self.qImg is not None:
            self.pixmap = QPixmap.fromImage(self.qImg)
        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        self.setScene(self.scene)
        self.fitInView(self.pixmapItem, QtCore.Qt.KeepAspectRatio)

    def update_image(self):
        self.scene.clear()
        if self.qImg is not None:
            self.pixmap = QPixmap.fromImage(self.qImg)
        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        self.drawPolygon()
        self.fitInView(self.pixmapItem, QtCore.Qt.KeepAspectRatio)
