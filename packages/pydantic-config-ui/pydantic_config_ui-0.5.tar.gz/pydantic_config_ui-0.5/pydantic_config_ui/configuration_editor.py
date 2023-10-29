import json
import logging
from typing import Type

from PySide6.QtCore import QSettings
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QFileDialog, QLabel, QDialog, QVBoxLayout, QSizePolicy, QMessageBox
from pydantic import ValidationError, BaseModel

from .configuration_common import get_settings_name, create_tab, save_configuration, get_configuration_field
from .recent_combobox import RecentCombobox
from .ui_config_dialog import Ui_ConfigBaseDialog

logger = logging.getLogger(__name__)


class ConfigurationEditor(QDialog):

    def __init__(self, model: Type[BaseModel],
                 model_data: BaseModel = None, config_file: str = "", title: str = "",
                 logo: QPixmap = None, settings: QSettings = None, parent: QWidget = None):

        super(ConfigurationEditor, self).__init__(parent)
        self.configuration_model = model
        self.configuration = model() if model_data is None else model_data
        self.with_recent_box = model_data is None
        self.file_accessible = False
        self.configuration_map = {}
        self.configuration_error = {}
        self.configuration_name = ""
        self.configuration_schema = model.schema()
        self.setWindowTitle(self.configuration_schema["title"])
        self.last_folder = ""
        self.settings = settings

        if self.with_recent_box:
            self.recent_file_list = RecentCombobox(20, self)
            self.recent_file_list.signal_entry_changed.connect(self.change_configuration)

        self.create_form(title, logo)

        if settings:
            self.restoreGeometry(self.settings.value(get_settings_name("config_geometry")))
            if self.with_recent_box:
                trl = self.settings.value(get_settings_name("recent_files"))
                if trl:
                    self.recent_file_list.set_entries(str(trl).split("|"))

        if config_file and self.with_recent_box:
            self.recent_file_list.add_or_update_entry(config_file)

        if self.with_recent_box:
            self.configuration_name = self.recent_file_list.current_entry()
        else:
            self.update_configuration_form()

    def create_form(self, title, logo):
        window = Ui_ConfigBaseDialog()
        window.setupUi(self)

        window.title.setText(title)
        if logo is not None:
            window.logo.setPixmap(logo)

        if self.with_recent_box:
            window.layout_dialog.layout().insertWidget(1, self.recent_file_list)

        groups = {"default": window.arguments.layout()}

        # create form layout widgets
        for name, field in self.configuration_schema["properties"].items():

            # create input element (line_edit, checkbox, ...)
            configuration_field = get_configuration_field(self.configuration_model, name, field)
            self.configuration_map[name] = configuration_field

            if configuration_field.has_ui():
                # create from label
                label = QLabel(self)
                label.setText(field.get("title", name))
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                # create new tab if not exists
                group_name = field.get("ui_group", "default")
                if group_name not in groups:
                    new_form_layout = create_tab(group_name, window)
                    groups[group_name] = new_form_layout

                # embed the input widget by adding a error field label
                form_field = QWidget()
                form_field_layout = QVBoxLayout(form_field)
                form_field_layout.setContentsMargins(2, 0, 2, 0)
                form_field_layout.setSpacing(1)
                err_label = QLabel(self)
                err_label.setVisible(False)
                err_label.setStyleSheet("color:red")
                form_field_layout.addStretch()
                form_field_layout.addWidget(configuration_field.create_widget(form_field))
                form_field_layout.addWidget(err_label)
                form_field_layout.addStretch()
                self.configuration_error[name] = err_label
                groups[group_name].addRow(label, form_field)

        window.button_cancel.clicked.connect(self.button_cancel_click)
        window.button_ok.clicked.connect(self.button_ok_click)
        window.button_load.clicked.connect(self.read_configuration)
        window.button_save_as.clicked.connect(self.save_configuration)

    def update_configuration_form(self):
        if self.configuration:
            for name, field in self.configuration_schema["properties"].items():
                self.configuration_map[name].set_value(getattr(self.configuration, name))

    def load_configuration(self, config_file_name: str) -> bool:
        try:
            with open(config_file_name) as json_config:
                jc = json_config.read()
                self.configuration = self.configuration_model.model_validate_json(jc)
                self._set_configuration_name(config_file_name)
                self.update_configuration_form()
            return True
        except FileNotFoundError as e:
            logger.error(self.tr("configuration file '{0}' not found").format(e.filename))
        except ValidationError as validation_errors:
            errors = json.loads(validation_errors.json())
            elist = []
            for e in errors:
                if len(e["loc"]) == 0:
                    elist.append(e["msg"])
                else:
                    elist.append(f'{e["loc"][0]}: {e["msg"]}')
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText(self.tr("Configuration contains Errors"))
            msg_box.setInformativeText(self.tr("Please correct before loading again."))
            msg_box.setDetailedText("\n".join(elist))
            msg_box.exec()
        return False

    def button_cancel_click(self):
        self.reject()

    def show_error_msg(self, name, msg):
        if self.configuration_map[name].has_ui():
            self.configuration_error[name].setText(msg)
            self.configuration_error[name].setVisible(True if len(msg) > 0 else False)

    def set_configuration_value(self, name, value):
        try:
            setattr(self.configuration, name, value)
            self.show_error_msg(name, "")
            return True
        except ValidationError as e:
            err = json.loads(e.json())
            txt = err[0]["msg"]
            self.show_error_msg(name, txt)
        return False

    def _check_configuration(self) -> bool:
        all_fine = True
        for name, field in self.configuration_schema["properties"].items():
            all_fine = all_fine and self.set_configuration_value(name, self.configuration_map[name].get_value())

        return all_fine

    def _set_configuration_name(self, cname):
        self.configuration_name = cname
        if self.with_recent_box:
            self.recent_file_list.add_or_update_entry(self.configuration_name)

    def _save(self):
        save_configuration(self.configuration_name, self.configuration)

    def button_ok_click(self):
        if self._check_configuration():
            self._save()
            if self.settings and self.with_recent_box:
                self.settings.setValue("pydantic-config-ui/recent_files",
                                       "|".join(self.recent_file_list.get_entries()))
            self.accept()

    def save_configuration(self):
        if self._check_configuration():
            filename, ret_filter = QFileDialog.getSaveFileName(parent=self,
                                                               caption=self.tr('Save Configuration'),
                                                               dir='.',
                                                               filter='*.json')
            if filename:
                if not filename.endswith(".json"):
                    filename = f"{filename}.json"
                self._set_configuration_name(filename)
                self._save()

    def read_configuration(self):
        filename, ret_filter = QFileDialog.getOpenFileName(parent=self,
                                                           caption=self.tr('Read Configuration'),
                                                           dir='.',
                                                           filter='*.json')
        if filename:
            self.load_configuration(filename)

    def change_configuration(self, new_configuration):
        logger.info(f"switch configuration from '{self.configuration_name}' to '{new_configuration}'")
        load_result = True

        if new_configuration == "":
            return
        if self.configuration_name == "":
            load_result = self.load_configuration(new_configuration)
        elif self.configuration_name != new_configuration:
            if self.file_accessible:
                if self._check_configuration():
                    self._save()
                    load_result = self.load_configuration(new_configuration)
                elif self.with_recent_box:
                    self.recent_file_list.add_or_update_entry(self.configuration_name)
            else:
                load_result = self.load_configuration(new_configuration)

        self.file_accessible = load_result

        if not load_result:
            msg_box = QMessageBox()
            msg_box.setText(self.tr("Missing Configuration"))
            msg_box.setInformativeText(self.tr("Remove '{0}' from recent list?").format(new_configuration))
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if msg_box.exec_() == QMessageBox.Ok:
                self.recent_file_list.remove_first_entry()
            else:
                self.file_accessible = False
                self.configuration_name = new_configuration
                self.configuration = self.configuration_model()
                self.update_configuration_form()

