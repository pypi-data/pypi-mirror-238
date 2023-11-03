import logging
import inspect
from functools import lru_cache
from os import path
from typing import Type

from PySide6.QtCore import QTranslator, QLocale, QCoreApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSpacerItem, QSizePolicy, QApplication
from pydantic import BaseModel

from .field_array import FieldArray
from .field_checkbox import FieldCheckbox
from .field_file_select import FieldFileSelect
from .field_folder_select import FieldFolderSelect
from .field_hidden import FieldHidden
from .field_input import FieldInput

logger = logging.getLogger(__name__)

settings_base: str = "pydantic-config-ui/"


def add_translator(app, i18n_project, i18n_folder):
    config_translator = QTranslator(app)
    i18n_file = f"{i18n_project}{QLocale().name()}"
    if not config_translator.load(QLocale(), i18n_project, directory=i18n_folder):
        logger.warning("can't load translator")
        logger.error(f"can't load translation for {i18n_file} from {i18n_folder}")
    else:
        app.installTranslator(config_translator)
        logger.info(f"load translation for {i18n_file} from {i18n_folder}")


def add_default_translator(app):
    i18n_folder = path.abspath(path.join(path.dirname(__file__), 'i18n'))
    add_translator(app, "pydantic_config_ui_", i18n_folder)


def get_settings_name(entry: str) -> str:
    return f"{settings_base}{entry}"


def create_tab(group_name, window):
    # tab with vertical layout
    new_tab = QWidget()
    new_tab.setObjectName(f"tab_{group_name}")
    new_vertical_layout = QVBoxLayout(new_tab)
    new_vertical_layout.setObjectName(f"verticalLayout_{group_name}")
    # form widget, this contains the elements later
    new_form = QWidget(new_tab)
    new_form.setObjectName(f"form_{group_name}")
    new_form_layout = QFormLayout(new_form)
    new_form_layout.setObjectName(f"formLayout_{group_name}")
    new_form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
    new_form_layout.setContentsMargins(-1, 0, -1, 0)
    # build tab by adding a spacer
    new_vertical_layout.addWidget(new_form)
    new_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    new_vertical_layout.addItem(new_vertical_spacer)
    # add to existing argument_tabs and store layout for later usage
    window.argument_tabs.addTab(new_tab, group_name)
    return new_form_layout


def save_configuration(filename: str, config: Type[BaseModel]):
    if filename:
        try:
            with open(filename, "w") as file_obj:
                file_obj.write(config.model_dump_json(indent=4))
        except FileNotFoundError as e:
            pass


@lru_cache(maxsize=5)
def has_configuration_method(model: Type[BaseModel]) -> bool:
    members = [x[0] for x in inspect.getmembers(model)]
    return "get_configuration_field" in members


def get_type(field):
    if "type" in field:
        return field["type"]

    if "anyOf" in field:
        for t in field["anyOf"]:
            if t["type"].lower() != "null":
                return t["type"]

    return None


def get_configuration_field(model: Type[BaseModel], name: str, field) -> FieldInput:
    field_type = get_type(field)

    if has_configuration_method(model):
        model_field = model.get_configuration_field(name, field)
        if model_field is not None:
            return model_field

    if field_type == "hidden":
        return FieldHidden(name, field)

    if field_type == "string" and field.get("ui_type", "") == "file":
        return FieldFileSelect(name, field)

    if field_type == "string" and field.get("ui_type", "") == "folder":
        return FieldFolderSelect(name, field)

    if field_type == "array":
        return FieldArray(name, field)

    if field_type in ("string", "integer"):
        return FieldInput(name, field)

    if field_type == "boolean":
        return FieldCheckbox(name, field)

    logger.error(f"missing UI field class {field_type} for {name}.")

    return FieldHidden(name, field)
