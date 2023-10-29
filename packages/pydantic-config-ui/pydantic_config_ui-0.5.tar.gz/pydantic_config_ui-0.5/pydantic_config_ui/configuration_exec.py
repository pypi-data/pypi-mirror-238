import logging
from typing import Type, Callable

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QObject, Signal, QThread, QSettings
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, \
    QFrame, QLabel, QSpacerItem, QSizePolicy
from pydantic import BaseModel

from .configuration_common import get_settings_name
from .configuration_editor import ConfigurationEditor

logger = logging.getLogger(__name__)


class MySignal(QObject):
    sig = Signal(str)


class QTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = MySignal()

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.appendPlainText.sig.connect(self.widget.appendHtml)

    def clear(self):
        self.widget.clear()

    def emit(self, record):
        msg = self.format(record)
        if msg.startswith("ERROR"):
            msg = f'<font color="red">{msg}</font>'
        if msg.startswith("WARNING"):
            msg = f'<font color="blue">{msg}</font>'
        self.appendPlainText.sig.emit(msg)


class MainConfiguration(QMainWindow):

    def __init__(self, configuration_model: Type[BaseModel],
                 configuration_file: str,
                 callback: Callable[[Type[BaseModel]], None],
                 title: str = "",
                 logo: QPixmap = None,
                 settings: QSettings = None):
        """
        Combine edit the configuration and execute a given callback function with the configuration.

        :param configuration_model: The pydantic model, defines the elements for the dialog
        :param configuration_file: The configuration file, which contains the persisted configuration in json format.With no filename given, the last edited file from the recent list is used.
        :param callback: The callback function is called after the dialog is closed with Ok
        :param title: An optional title which is shown in the dialog.
        :param logo: An optional logo as QPixmap which is shown in the dialog, please adjust the size, this isn't part og the dialog usage.
        :param settings: Optional settings, but needed if you like to restore geometry and recent file list.
        """
        super(MainConfiguration, self).__init__()
        self.configuration_file = configuration_file
        self.configuration_model = configuration_model
        self.configuration = None
        self.callback = callback
        self.callback_thread = MyLongThread(callback)
        self.callback_thread.signal.sig.connect(self.callback_finish)
        self.settings = settings

        # add textbox as logging handler
        self.log_text_box = QTextEditLogger(self)
        self.log_text_box.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
        logging.getLogger().addHandler(self.log_text_box)

        self._configuration_editor = ConfigurationEditor(self.configuration_model,
                                                         None,
                                                         self.configuration_file,
                                                         title, logo,
                                                         settings, self)
        if self.settings:
            self.restoreGeometry(self.settings.value(get_settings_name("main_geometry")))

        button_clean_log = QPushButton(self.tr("Clean Log"))
        self.button_config = QPushButton(self.tr("Edit Configuration"))
        self.button_execute = QPushButton(self.tr("Execute"))
        button_finish = QPushButton(self.tr("Finish"))
        button_clean_log.clicked.connect(self.button_clean_log_click)
        self.button_config.clicked.connect(self.button_config_click)
        self.button_execute.clicked.connect(self.button_execute_click)
        button_finish.clicked.connect(self.button_finish_clicked)

        # button bar
        btn_widget = QWidget()
        btn_widget.setFixedHeight(50)
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.addStretch()
        btn_layout.addWidget(button_clean_log)
        btn_layout.addWidget(self.button_config)
        btn_layout.addWidget(self.button_execute)
        btn_layout.addWidget(button_finish)

        # title frame
        title_frame = QFrame(self)
        title_frame.setObjectName(u"titleFrame")
        title_frame.setFrameShape(QFrame.StyledPanel)
        title_frame.setFrameShadow(QFrame.Raised)
        layout_title = QHBoxLayout(title_frame)
        layout_title.setObjectName(u"layout_title")
        layout_title.setContentsMargins(4, 4, 4, 4)
        title_label = QLabel(title_frame)
        title_label.setObjectName(u"title")
        title_label.setText(title)
        layout_title.addWidget(title_label)
        horizontal_spacer = QSpacerItem(250, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout_title.addItem(horizontal_spacer)
        logo_label = QLabel(title_frame)
        logo_label.setObjectName(u"logo")
        layout_title.addWidget(logo_label)
        if logo is not None:
            logo_label.setPixmap(logo)

        layout = QVBoxLayout()
        layout.addWidget(title_frame)
        layout.addWidget(self.log_text_box.widget)
        layout.addWidget(btn_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def showEvent(self, event):
        super().showEvent(event)
        self.button_config_click()

    def button_config_click(self):
        self._configuration_editor.show()
        form_ret = self._configuration_editor.exec()
        if form_ret:
            self.configuration_file = self._configuration_editor.configuration_name
            self.configuration = self._configuration_editor.configuration
            self.button_execute.show()
            self.button_execute_click()
        else:
            self.configuration = None
            self.button_execute.hide()
            logger.warning(self.tr("config edit canceled -- no execution possible"))

    def button_clean_log_click(self):
        self.log_text_box.clear()

    def button_execute_click(self):
        if self.callback and self.configuration:
            if not self.callback_thread.isRunning():
                self.callback_thread.exiting = False
                self.callback_thread.configuration = self.configuration
                self.button_execute.hide()
                self.button_config.hide()
                self.callback_thread.start()

    def button_finish_clicked(self):
        if self.callback_thread.isRunning():
            msg_stop = QMessageBox()
            msg_stop.setText(self.tr("Process is running."))
            msg_stop.setInformativeText(self.tr("Really stop the process?"))
            msg_stop.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_stop.setButtonText(QMessageBox.Ok, self.tr("Yes"))
            msg_stop.setButtonText(QMessageBox.Cancel, self.tr("No"))
            msg_stop.setDefaultButton(QMessageBox.Cancel)
            ret = msg_stop.exec_()
            if ret == QMessageBox.Ok:
                self.callback_thread.requestInterruption()
                logger.info(self.tr("request thread interruption"))
        else:
            if self.settings:
                self.settings.setValue(get_settings_name("config_geometry"), self._configuration_editor.saveGeometry())
                self.settings.setValue(get_settings_name("main_geometry"), self.saveGeometry())
            self.close()

    def callback_finish(self, data):
        self.button_execute.show()
        self.button_config.show()
        logger.info(f"{self.tr('callback finished with')} {data}")


class MyLongThread(QThread):
    def __init__(self, callback, parent=None):
        QThread.__init__(self, parent)
        self.signal = MySignal()
        self.callback = callback
        self.configuration = None

    def run(self):
        if self.configuration is None:
            self.signal.sig.emit(self.tr("Missing configuration"))
        else:
            self.callback(self.configuration)
            self.signal.sig.emit(self.tr("Ready"))
