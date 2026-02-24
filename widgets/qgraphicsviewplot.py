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
    """Custom QGraphicsView for embedding a matplotlib plot.
    
    Attributes:
        scene (QGraphicsScene): The scene containing the plot.
        figure (plt.Figure): The matplotlib figure.
        ax (plt.Axes): The matplotlib axes.
        canvas (FigureCanvasQTAgg): The canvas widget.
        proxy (QGraphicsProxyWidget): Proxy widget to host the canvas in the scene.
    """
    def __init__(self, parent=None):
        """Initializes the QGraphicsViewPlot with a matplotlib figure.
        
        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
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
        """Draws a parabola based on the general quadratic equation.
        
        Args:
            a (float): Coefficient a (x^2 term).
            b (float): Coefficient b (x term).
            c (float): Constant c.
        """
        # Parabola coefficients
        self.ax.clear()

        # Generate x values
        D = abs(b ** 2 - 4 * a * c)
        x1 = (-b ** 2 - math.sqrt(D)) / (2 * a)
        x2 = (-b ** 2 + math.sqrt(D)) / (2 * a)
        x = np.linspace(x1, x2, 400)

        # Calculate y values using the general parabola equation
        y = a * x ** 2 + b * x + c

        # Plot parabola
        self.ax.plot(x, y, label=f'{a}x^2 + {b}x + {c}')
        #
        # # Add title and axis labels
        self.ax.set_title('Parabola: General Equation')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        # Update canvas
        self.canvas.draw()

        # Ensure the event loop continues
        QtWidgets.QApplication.processEvents()

    def update_plot(self):
        """Updates the plot display with the current image map (deprecated/placeholder method)."""
        self.scene.clear()
        if self.qImg is not None:
            self.pixmap = QPixmap.fromImage(self.qImg)
        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        self.drawPolygon()
        self.fitInView(self.pixmapItem, QtCore.Qt.KeepAspectRatio)
