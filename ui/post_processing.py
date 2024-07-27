# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'post_processing.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(454, 164)
        icon = QIcon()
        icon.addFile(u":/resource/resource/moncenter_logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.action_main_window = QAction(MainWindow)
        self.action_main_window.setObjectName(u"action_main_window")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_start_processing = QPushButton(self.centralwidget)
        self.pushButton_start_processing.setObjectName(u"pushButton_start_processing")

        self.gridLayout.addWidget(self.pushButton_start_processing, 2, 0, 1, 2)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.pushButton_select_path = QPushButton(self.centralwidget)
        self.pushButton_select_path.setObjectName(u"pushButton_select_path")

        self.gridLayout.addWidget(self.pushButton_select_path, 1, 1, 1, 1)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")

        self.gridLayout.addWidget(self.label_time, 4, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 454, 18))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action_main_window)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.action_main_window.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u0432 \u0433\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e", None))
        self.pushButton_start_processing.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u0442\u044c \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443", None))
        self.pushButton_select_path.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0437\u043e\u0440", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u044c \u043a \u0432\u0438\u0434\u0435\u043e\u0444\u0430\u0439\u043b\u0443", None))
        self.label_time.setText("")
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u044e", None))
    # retranslateUi

