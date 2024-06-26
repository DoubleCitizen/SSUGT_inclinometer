# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1290, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_nivel = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_nivel.setFont(font)
        self.label_nivel.setText("")
        self.label_nivel.setObjectName("label_nivel")
        self.horizontalLayout.addWidget(self.label_nivel)
        self.label_value = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_value.setFont(font)
        self.label_value.setText("")
        self.label_value.setObjectName("label_value")
        self.horizontalLayout.addWidget(self.label_value)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphicsView = QGraphicsViewVideo(self.frame)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 2, 1)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(400, 160))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 160))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_apply_source = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_apply_source.setObjectName("pushButton_apply_source")
        self.gridLayout_3.addWidget(self.pushButton_apply_source, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_source_video = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_source_video.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_source_video.setObjectName("lineEdit_source_video")
        self.gridLayout_3.addWidget(self.lineEdit_source_video, 1, 0, 1, 1)
        self.pushButton_stop_stream = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_stop_stream.setObjectName("pushButton_stop_stream")
        self.gridLayout_3.addWidget(self.pushButton_stop_stream, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 1, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_4.setContentsMargins(-1, 1, -1, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_start_position = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_start_position.setObjectName("pushButton_start_position")
        self.gridLayout_4.addWidget(self.pushButton_start_position, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 4, 0, 1, 1)
        self.checkBox_rectangle_show = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_rectangle_show.setObjectName("checkBox_rectangle_show")
        self.gridLayout_4.addWidget(self.checkBox_rectangle_show, 7, 0, 1, 1)
        self.checkBox_enable_record = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_enable_record.setChecked(False)
        self.checkBox_enable_record.setAutoRepeat(False)
        self.checkBox_enable_record.setObjectName("checkBox_enable_record")
        self.gridLayout_4.addWidget(self.checkBox_enable_record, 3, 0, 1, 1)
        self.checkBox_view_points = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_view_points.setObjectName("checkBox_view_points")
        self.gridLayout_4.addWidget(self.checkBox_view_points, 6, 0, 1, 1)
        self.checkBox_segmentaion_show = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_segmentaion_show.setObjectName("checkBox_segmentaion_show")
        self.gridLayout_4.addWidget(self.checkBox_segmentaion_show, 8, 0, 1, 1)
        self.spinBox_points = QtWidgets.QSpinBox(self.frame_4)
        self.spinBox_points.setMinimum(1)
        self.spinBox_points.setObjectName("spinBox_points")
        self.gridLayout_4.addWidget(self.spinBox_points, 5, 0, 1, 1)
        self.checkBox_start_position = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_start_position.setObjectName("checkBox_start_position")
        self.gridLayout_4.addWidget(self.checkBox_start_position, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1290, 18))
        self.menubar.setObjectName("menubar")
        self.menu_tools = QtWidgets.QMenu(self.menubar)
        self.menu_tools.setEnabled(True)
        self.menu_tools.setObjectName("menu_tools")
        self.menu_Nivel_220 = QtWidgets.QMenu(self.menu_tools)
        self.menu_Nivel_220.setObjectName("menu_Nivel_220")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action5 = QtWidgets.QAction(MainWindow)
        self.action5.setObjectName("action5")
        self.action_dialog_regres = QtWidgets.QAction(MainWindow)
        self.action_dialog_regres.setObjectName("action_dialog_regres")
        self.action_esp32 = QtWidgets.QAction(MainWindow)
        self.action_esp32.setObjectName("action_esp32")
        self.menu_tools.addAction(self.menu_Nivel_220.menuAction())
        self.menu_tools.addAction(self.action_dialog_regres)
        self.menu_tools.addAction(self.action_esp32)
        self.menubar.addAction(self.menu_tools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ВИМ менеджер"))
        self.pushButton_apply_source.setText(_translate("MainWindow", "Применить источник"))
        self.label.setText(_translate("MainWindow", "Источник видеопотока"))
        self.pushButton_stop_stream.setText(_translate("MainWindow", "Выключить поток"))
        self.pushButton_start_position.setText(_translate("MainWindow", "Сместить начало отсчета"))
        self.label_2.setText(_translate("MainWindow", "Регулировать частоту записи точек"))
        self.checkBox_rectangle_show.setText(_translate("MainWindow", "Отобразить прямоугольник"))
        self.checkBox_enable_record.setText(_translate("MainWindow", "Начать запись"))
        self.checkBox_view_points.setText(_translate("MainWindow", "Отобразить точки"))
        self.checkBox_segmentaion_show.setText(_translate("MainWindow", "Показать сегментацию"))
        self.checkBox_start_position.setText(_translate("MainWindow", "Показать начало отсчета"))
        self.menu_tools.setTitle(_translate("MainWindow", "Инструменты"))
        self.menu_Nivel_220.setTitle(_translate("MainWindow", "Подключить Nivel 220"))
        self.action5.setText(_translate("MainWindow", "5"))
        self.action_dialog_regres.setText(_translate("MainWindow", "Изменить параметры линейной регрессии"))
        self.action_esp32.setText(_translate("MainWindow", "Подключить esp32"))
from widgets.graphicsviewvideo import QGraphicsViewVideo
