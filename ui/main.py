# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QWidget)

from widgets.graphicsviewvideo import QGraphicsViewVideo
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1290, 600)
        icon = QIcon()
        icon.addFile(u":/resource/resource/moncenter_logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.action5 = QAction(MainWindow)
        self.action5.setObjectName(u"action5")
        self.action_dialog_regres = QAction(MainWindow)
        self.action_dialog_regres.setObjectName(u"action_dialog_regres")
        self.action_esp32 = QAction(MainWindow)
        self.action_esp32.setObjectName(u"action_esp32")
        self.action_static_mode = QAction(MainWindow)
        self.action_static_mode.setObjectName(u"action_static_mode")
        self.action_static_mode.setCheckable(True)
        self.action_main_window = QAction(MainWindow)
        self.action_main_window.setObjectName(u"action_main_window")
        self.action_open_directory = QAction(MainWindow)
        self.action_open_directory.setObjectName(u"action_open_directory")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        palette = QPalette()
        brush = QBrush(QColor(246, 246, 246, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush)
        self.centralwidget.setPalette(palette)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 50))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_nivel = QLabel(self.frame_2)
        self.label_nivel.setObjectName(u"label_nivel")
        font = QFont()
        font.setPointSize(12)
        self.label_nivel.setFont(font)

        self.horizontalLayout.addWidget(self.label_nivel)

        self.label_vim_temp = QLabel(self.frame_2)
        self.label_vim_temp.setObjectName(u"label_vim_temp")
        self.label_vim_temp.setFont(font)

        self.horizontalLayout.addWidget(self.label_vim_temp)

        self.label_value = QLabel(self.frame_2)
        self.label_value.setObjectName(u"label_value")
        self.label_value.setFont(font)

        self.horizontalLayout.addWidget(self.label_value)


        self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 2)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(400, 160))
        self.frame_3.setMaximumSize(QSize(16777215, 160))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_status_esp_icon = QLabel(self.frame_5)
        self.label_status_esp_icon.setObjectName(u"label_status_esp_icon")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_status_esp_icon.sizePolicy().hasHeightForWidth())
        self.label_status_esp_icon.setSizePolicy(sizePolicy)
        self.label_status_esp_icon.setMinimumSize(QSize(32, 32))
        self.label_status_esp_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.label_status_esp_icon)

        self.label_status_esp_connect = QLabel(self.frame_5)
        self.label_status_esp_connect.setObjectName(u"label_status_esp_connect")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_status_esp_connect.sizePolicy().hasHeightForWidth())
        self.label_status_esp_connect.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(10)
        self.label_status_esp_connect.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_status_esp_connect)


        self.gridLayout_3.addWidget(self.frame_5, 0, 0, 1, 1)

        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.label, 2, 0, 1, 1)

        self.pushButton_stop_stream = QPushButton(self.frame_3)
        self.pushButton_stop_stream.setObjectName(u"pushButton_stop_stream")

        self.gridLayout_3.addWidget(self.pushButton_stop_stream, 5, 0, 1, 1)

        self.pushButton_apply_source = QPushButton(self.frame_3)
        self.pushButton_apply_source.setObjectName(u"pushButton_apply_source")

        self.gridLayout_3.addWidget(self.pushButton_apply_source, 4, 0, 1, 1)

        self.lineEdit_source_video = QLineEdit(self.frame_3)
        self.lineEdit_source_video.setObjectName(u"lineEdit_source_video")
        self.lineEdit_source_video.setEnabled(False)
        self.lineEdit_source_video.setMinimumSize(QSize(0, 30))

        self.gridLayout_3.addWidget(self.lineEdit_source_video, 3, 0, 1, 1)

        self.label_fps_counter = QLabel(self.frame_3)
        self.label_fps_counter.setObjectName(u"label_fps_counter")

        self.gridLayout_3.addWidget(self.label_fps_counter, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 1, 2, 1, 1)

        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, 1, -1, -1)
        self.comboBox_speed_frame = QComboBox(self.frame_4)
        self.comboBox_speed_frame.addItem("")
        self.comboBox_speed_frame.addItem("")
        self.comboBox_speed_frame.setObjectName(u"comboBox_speed_frame")

        self.gridLayout_4.addWidget(self.comboBox_speed_frame, 0, 1, 1, 1)

        self.lineEdit_speed_frame = QLineEdit(self.frame_4)
        self.lineEdit_speed_frame.setObjectName(u"lineEdit_speed_frame")
        self.lineEdit_speed_frame.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.lineEdit_speed_frame, 0, 0, 1, 1)

        self.checkBox_start_position = QCheckBox(self.frame_4)
        self.checkBox_start_position.setObjectName(u"checkBox_start_position")

        self.gridLayout_4.addWidget(self.checkBox_start_position, 1, 0, 1, 2)

        self.checkBox_segmentaion_show = QCheckBox(self.frame_4)
        self.checkBox_segmentaion_show.setObjectName(u"checkBox_segmentaion_show")

        self.gridLayout_4.addWidget(self.checkBox_segmentaion_show, 9, 0, 1, 2)

        self.checkBox_rectangle_show = QCheckBox(self.frame_4)
        self.checkBox_rectangle_show.setObjectName(u"checkBox_rectangle_show")

        self.gridLayout_4.addWidget(self.checkBox_rectangle_show, 8, 0, 1, 2)

        self.checkBox_view_points = QCheckBox(self.frame_4)
        self.checkBox_view_points.setObjectName(u"checkBox_view_points")

        self.gridLayout_4.addWidget(self.checkBox_view_points, 7, 0, 1, 2)

        self.spinBox_points = QSpinBox(self.frame_4)
        self.spinBox_points.setObjectName(u"spinBox_points")
        self.spinBox_points.setMinimum(1)

        self.gridLayout_4.addWidget(self.spinBox_points, 6, 0, 1, 2)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_4.addWidget(self.label_2, 5, 0, 1, 2)

        self.checkBox_enable_record = QCheckBox(self.frame_4)
        self.checkBox_enable_record.setObjectName(u"checkBox_enable_record")
        self.checkBox_enable_record.setChecked(False)
        self.checkBox_enable_record.setAutoRepeat(False)

        self.gridLayout_4.addWidget(self.checkBox_enable_record, 4, 0, 1, 2)

        self.pushButton_start_position = QPushButton(self.frame_4)
        self.pushButton_start_position.setObjectName(u"pushButton_start_position")

        self.gridLayout_4.addWidget(self.pushButton_start_position, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.frame_4, 2, 2, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.graphicsView = QGraphicsViewVideo(self.frame)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 1, 2, 1)

        self.frame_static_2 = QFrame(self.centralwidget)
        self.frame_static_2.setObjectName(u"frame_static_2")
        self.frame_static_2.setMinimumSize(QSize(200, 0))
        self.frame_static_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_static_2.setFrameShape(QFrame.NoFrame)
        self.frame_static_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_static_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_3 = QLabel(self.frame_static_2)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setPointSize(14)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)

        self.pushButton_time_point_start = QPushButton(self.frame_static_2)
        self.pushButton_time_point_start.setObjectName(u"pushButton_time_point_start")

        self.gridLayout_6.addWidget(self.pushButton_time_point_start, 1, 0, 1, 1)

        self.pushButton_time_point_end = QPushButton(self.frame_static_2)
        self.pushButton_time_point_end.setObjectName(u"pushButton_time_point_end")
        self.pushButton_time_point_end.setEnabled(False)

        self.gridLayout_6.addWidget(self.pushButton_time_point_end, 2, 0, 1, 1)

        self.lineEdit_indicator_value = QLineEdit(self.frame_static_2)
        self.lineEdit_indicator_value.setObjectName(u"lineEdit_indicator_value")

        self.gridLayout_6.addWidget(self.lineEdit_indicator_value, 3, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_static_2, 1, 0, 2, 1)

        self.frame_static_1 = QFrame(self.centralwidget)
        self.frame_static_1.setObjectName(u"frame_static_1")
        self.frame_static_1.setFrameShape(QFrame.NoFrame)
        self.frame_static_1.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_static_1)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_4 = QLabel(self.frame_static_1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_timer = QLabel(self.frame_static_1)
        self.label_timer.setObjectName(u"label_timer")
        self.label_timer.setFont(font2)
        self.label_timer.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_timer, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_static_1, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1290, 18))
        self.menu_tools = QMenu(self.menubar)
        self.menu_tools.setObjectName(u"menu_tools")
        self.menu_tools.setEnabled(True)
        self.menu_Nivel_220 = QMenu(self.menu_tools)
        self.menu_Nivel_220.setObjectName(u"menu_Nivel_220")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menu_tools.addAction(self.menu_Nivel_220.menuAction())
        self.menu_tools.addAction(self.action_dialog_regres)
        self.menu_tools.addAction(self.action_esp32)
        self.menu.addAction(self.action_static_mode)
        self.menu_2.addAction(self.action_main_window)
        self.menu_2.addAction(self.action_open_directory)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0418\u041c \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440", None))
        self.action5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.action_dialog_regres.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u043b\u0438\u043d\u0435\u0439\u043d\u043e\u0439 \u0440\u0435\u0433\u0440\u0435\u0441\u0441\u0438\u0438", None))
        self.action_esp32.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c esp32", None))
        self.action_static_mode.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043e\u0431\u0440\u0430\u0437\u0438\u0442\u044c \u0440\u0435\u0436\u0438\u043c \u0441\u0442\u0430\u0442\u0438\u043a\u0438", None))
        self.action_main_window.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u0432 \u0433\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e", None))
        self.action_open_directory.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u044e", None))
        self.label_nivel.setText(QCoreApplication.translate("MainWindow", u"Nivel", None))
        self.label_vim_temp.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430 \u0412\u0418\u041c", None))
        self.label_value.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0418\u041c", None))
        self.label_status_esp_icon.setText("")
        self.label_status_esp_connect.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f \u043a \u0412\u0418\u041c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0432\u0438\u0434\u0435\u043e\u043f\u043e\u0442\u043e\u043a\u0430", None))
        self.pushButton_stop_stream.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u043f\u043e\u0442\u043e\u043a", None))
        self.pushButton_apply_source.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a", None))
        self.label_fps_counter.setText(QCoreApplication.translate("MainWindow", u"FPS = 0", None))
        self.comboBox_speed_frame.setItemText(0, QCoreApplication.translate("MainWindow", u"\u0413\u0446", None))
        self.comboBox_speed_frame.setItemText(1, QCoreApplication.translate("MainWindow", u"1 \u043a\u0430\u0434\u0440 \u0437\u0430 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0435\u043a\u0443\u043d\u0434", None))

        self.lineEdit_speed_frame.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u043b-\u0432\u043e \u0413\u0446 \u0438\u043b\u0438 \u0441\u0435\u043a\u0443\u043d\u0434 \u0432 \u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438 \u043e\u0442 \u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0438\u0432\u0430\u044e\u0449\u0435\u0433\u043e \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u0430 \u0441\u044a\u0435\u043c\u043a\u0438", None))
        self.checkBox_start_position.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043d\u0430\u0447\u0430\u043b\u043e \u043e\u0442\u0441\u0447\u0435\u0442\u0430", None))
        self.checkBox_segmentaion_show.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0441\u0435\u0433\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044e", None))
        self.checkBox_rectangle_show.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043e\u0431\u0440\u0430\u0437\u0438\u0442\u044c \u043f\u0440\u044f\u043c\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a", None))
        self.checkBox_view_points.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043e\u0431\u0440\u0430\u0437\u0438\u0442\u044c \u0442\u043e\u0447\u043a\u0438", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0433\u0443\u043b\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0447\u0430\u0441\u0442\u043e\u0442\u0443 \u0437\u0430\u043f\u0438\u0441\u0438 \u0442\u043e\u0447\u0435\u043a", None))
        self.checkBox_enable_record.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButton_start_position.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043c\u0435\u0441\u0442\u0438\u0442\u044c \u043d\u0430\u0447\u0430\u043b\u043e \u043e\u0442\u0441\u0447\u0435\u0442\u0430", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b \u0440\u0435\u0436\u0438\u043c\u0430 \u0441\u0442\u0430\u0442\u0438\u043a\u0438", None))
        self.pushButton_time_point_start.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e \u0442\u043e\u0447\u043a\u0443", None))
        self.pushButton_time_point_end.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e \u0442\u043e\u0447\u043a\u0443", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0435\u043a\u0443\u043d\u0434\u043e\u043c\u0435\u0440", None))
        self.label_timer.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.menu_tools.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b", None))
        self.menu_Nivel_220.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c Nivel 220", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0436\u0438\u043c\u044b", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u044e", None))
    # retranslateUi

