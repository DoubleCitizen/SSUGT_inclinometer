# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start_menu.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(465, 346)
        icon = QIcon()
        icon.addFile(u":/resource/resource/moncenter_logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_vim = QPushButton(self.centralwidget)
        self.pushButton_vim.setObjectName(u"pushButton_vim")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_vim.sizePolicy().hasHeightForWidth())
        self.pushButton_vim.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u":/resource/resource/esp32.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_vim.setIcon(icon1)
        self.pushButton_vim.setIconSize(QSize(100, 100))

        self.verticalLayout.addWidget(self.pushButton_vim)

        self.pushButton_laser_and_vim = QPushButton(self.centralwidget)
        self.pushButton_laser_and_vim.setObjectName(u"pushButton_laser_and_vim")
        sizePolicy.setHeightForWidth(self.pushButton_laser_and_vim.sizePolicy().hasHeightForWidth())
        self.pushButton_laser_and_vim.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u":/resource/resource/esp32_esp32.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_laser_and_vim.setIcon(icon2)
        self.pushButton_laser_and_vim.setIconSize(QSize(100, 100))

        self.verticalLayout.addWidget(self.pushButton_laser_and_vim)

        self.pushButton_post_processing = QPushButton(self.centralwidget)
        self.pushButton_post_processing.setObjectName(u"pushButton_post_processing")
        sizePolicy.setHeightForWidth(self.pushButton_post_processing.sizePolicy().hasHeightForWidth())
        self.pushButton_post_processing.setSizePolicy(sizePolicy)
        icon3 = QIcon()
        icon3.addFile(u":/resource/resource/post_processing.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_post_processing.setIcon(icon3)
        self.pushButton_post_processing.setIconSize(QSize(100, 100))

        self.verticalLayout.addWidget(self.pushButton_post_processing)

        self.pushButton_develop_tool = QPushButton(self.centralwidget)
        self.pushButton_develop_tool.setObjectName(u"pushButton_develop_tool")
        sizePolicy.setHeightForWidth(self.pushButton_develop_tool.sizePolicy().hasHeightForWidth())
        self.pushButton_develop_tool.setSizePolicy(sizePolicy)
        self.pushButton_develop_tool.setIconSize(QSize(100, 100))

        self.verticalLayout.addWidget(self.pushButton_develop_tool)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 465, 18))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e \u0412\u0418\u041c", None))
        self.pushButton_vim.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u0432 \u0412\u0418\u041c \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440", None))
        self.pushButton_laser_and_vim.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u0432 \u0412\u0418\u041c + Laser \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440", None))
        self.pushButton_post_processing.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u0432 \u043f\u043e\u0441\u0442 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443 \u0412\u0418\u041c", None))
        self.pushButton_develop_tool.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u043e\u0432", None))
    # retranslateUi

