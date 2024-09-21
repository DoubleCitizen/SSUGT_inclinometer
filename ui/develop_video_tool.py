# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'develop_video_tool.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

from widgets.graphicsviewvideo import QGraphicsViewVideo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 70))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_start_video = QPushButton(self.frame_2)
        self.pushButton_start_video.setObjectName(u"pushButton_start_video")

        self.gridLayout_4.addWidget(self.pushButton_start_video, 3, 0, 1, 1)

        self.pushButton_pause_video = QPushButton(self.frame_2)
        self.pushButton_pause_video.setObjectName(u"pushButton_pause_video")

        self.gridLayout_4.addWidget(self.pushButton_pause_video, 3, 1, 1, 1)

        self.graphicsView_segm_video = QGraphicsViewVideo(self.frame_2)
        self.graphicsView_segm_video.setObjectName(u"graphicsView_segm_video")

        self.gridLayout_4.addWidget(self.graphicsView_segm_video, 1, 0, 1, 2)

        self.graphicsView_original_video = QGraphicsViewVideo(self.frame_2)
        self.graphicsView_original_video.setObjectName(u"graphicsView_original_video")

        self.gridLayout_4.addWidget(self.graphicsView_original_video, 0, 0, 1, 2)

        self.horizontalSlider_video = QSlider(self.frame_2)
        self.horizontalSlider_video.setObjectName(u"horizontalSlider_video")
        self.horizontalSlider_video.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_video, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setMaximumSize(QSize(200, 16777215))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy2)
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lineEdit_path_videos = QLineEdit(self.frame_4)
        self.lineEdit_path_videos.setObjectName(u"lineEdit_path_videos")

        self.gridLayout_3.addWidget(self.lineEdit_path_videos, 0, 0, 1, 1)

        self.pushButton_select_path = QPushButton(self.frame_4)
        self.pushButton_select_path.setObjectName(u"pushButton_select_path")

        self.gridLayout_3.addWidget(self.pushButton_select_path, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy3)
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.spinBox = QSpinBox(self.frame_5)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(500)

        self.gridLayout_2.addWidget(self.spinBox, 4, 0, 1, 1)

        self.checkbox_draw_rectangle = QCheckBox(self.frame_5)
        self.checkbox_draw_rectangle.setObjectName(u"checkbox_draw_rectangle")
        self.checkbox_draw_rectangle.setChecked(True)

        self.gridLayout_2.addWidget(self.checkbox_draw_rectangle, 2, 0, 1, 1)

        self.checkbox_draw_points = QCheckBox(self.frame_5)
        self.checkbox_draw_points.setObjectName(u"checkbox_draw_points")
        self.checkbox_draw_points.setChecked(True)

        self.gridLayout_2.addWidget(self.checkbox_draw_points, 3, 0, 1, 1)

        self.checkbox_segmentaion_show = QCheckBox(self.frame_5)
        self.checkbox_segmentaion_show.setObjectName(u"checkbox_segmentaion_show")

        self.gridLayout_2.addWidget(self.checkbox_segmentaion_show, 1, 0, 1, 1)

        self.comboBox_detectors = QComboBox(self.frame_5)
        self.comboBox_detectors.setObjectName(u"comboBox_detectors")

        self.gridLayout_2.addWidget(self.comboBox_detectors, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_5)


        self.gridLayout.addWidget(self.frame_3, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 18))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0434\u0435\u043e \u0430\u043d\u0430\u043b\u0438\u0437\u0430\u0442\u043e\u0440", None))
        self.pushButton_start_video.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.pushButton_pause_video.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0443\u0437\u0430", None))
        self.pushButton_select_path.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0437\u043e\u0440", None))
        self.checkbox_draw_rectangle.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043f\u0440\u044f\u043c\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a", None))
        self.checkbox_draw_points.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0442\u043e\u0447\u043a\u0438", None))
        self.checkbox_segmentaion_show.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0441\u0435\u0433\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044e", None))
    # retranslateUi

