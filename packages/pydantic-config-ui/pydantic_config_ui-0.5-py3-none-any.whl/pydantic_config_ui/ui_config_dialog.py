# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_ConfigBaseDialog(object):
    def setupUi(self, ConfigBaseDialog):
        if not ConfigBaseDialog.objectName():
            ConfigBaseDialog.setObjectName(u"ConfigBaseDialog")
        ConfigBaseDialog.resize(558, 331)
        self.layout_dialog = QVBoxLayout(ConfigBaseDialog)
        self.layout_dialog.setObjectName(u"layout_dialog")
        self.layout_dialog.setContentsMargins(8, 8, 8, 8)
        self.titleFrame = QFrame(ConfigBaseDialog)
        self.titleFrame.setObjectName(u"titleFrame")
        self.titleFrame.setFrameShape(QFrame.StyledPanel)
        self.titleFrame.setFrameShadow(QFrame.Raised)
        self.layout_title = QHBoxLayout(self.titleFrame)
        self.layout_title.setObjectName(u"layout_title")
        self.layout_title.setContentsMargins(4, 4, 4, 4)
        self.title = QLabel(self.titleFrame)
        self.title.setObjectName(u"title")

        self.layout_title.addWidget(self.title)

        self.horizontalSpacer = QSpacerItem(250, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_title.addItem(self.horizontalSpacer)

        self.logo = QLabel(self.titleFrame)
        self.logo.setObjectName(u"logo")

        self.layout_title.addWidget(self.logo)


        self.layout_dialog.addWidget(self.titleFrame)

        self.argument_tabs = QTabWidget(ConfigBaseDialog)
        self.argument_tabs.setObjectName(u"argument_tabs")
        self.arguments_default = QWidget()
        self.arguments_default.setObjectName(u"arguments_default")
        self.verticalLayout = QVBoxLayout(self.arguments_default)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 4, 0, 4)
        self.arguments = QWidget(self.arguments_default)
        self.arguments.setObjectName(u"arguments")
        self.formLayout = QFormLayout(self.arguments)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(5, 0, 5, 0)

        self.verticalLayout.addWidget(self.arguments)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.argument_tabs.addTab(self.arguments_default, "")

        self.layout_dialog.addWidget(self.argument_tabs)

        self.button_bar = QWidget(ConfigBaseDialog)
        self.button_bar.setObjectName(u"button_bar")
        self.layout_button_bar = QHBoxLayout(self.button_bar)
        self.layout_button_bar.setObjectName(u"layout_button_bar")
        self.layout_button_bar.setContentsMargins(0, 4, 0, 4)
        self.button_save_as = QPushButton(self.button_bar)
        self.button_save_as.setObjectName(u"button_save_as")

        self.layout_button_bar.addWidget(self.button_save_as)

        self.button_load = QPushButton(self.button_bar)
        self.button_load.setObjectName(u"button_load")

        self.layout_button_bar.addWidget(self.button_load)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_button_bar.addItem(self.horizontalSpacer_2)

        self.button_cancel = QPushButton(self.button_bar)
        self.button_cancel.setObjectName(u"button_cancel")

        self.layout_button_bar.addWidget(self.button_cancel)

        self.button_ok = QPushButton(self.button_bar)
        self.button_ok.setObjectName(u"button_ok")

        self.layout_button_bar.addWidget(self.button_ok)


        self.layout_dialog.addWidget(self.button_bar)


        self.retranslateUi(ConfigBaseDialog)

        self.argument_tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ConfigBaseDialog)
    # setupUi

    def retranslateUi(self, ConfigBaseDialog):
        ConfigBaseDialog.setWindowTitle(QCoreApplication.translate("ConfigBaseDialog", u"Form", None))
        self.title.setText(QCoreApplication.translate("ConfigBaseDialog", u"Title for the Configuration", None))
        self.logo.setText(QCoreApplication.translate("ConfigBaseDialog", u"Optional Logo", None))
        self.argument_tabs.setTabText(self.argument_tabs.indexOf(self.arguments_default), QCoreApplication.translate("ConfigBaseDialog", u"Arguments", None))
        self.button_save_as.setText(QCoreApplication.translate("ConfigBaseDialog", u"Save As", None))
        self.button_load.setText(QCoreApplication.translate("ConfigBaseDialog", u"Load", None))
        self.button_cancel.setText(QCoreApplication.translate("ConfigBaseDialog", u"Cancel", None))
        self.button_ok.setText(QCoreApplication.translate("ConfigBaseDialog", u"Ok", None))
    # retranslateUi

