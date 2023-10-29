from PySide6.QtGui import Qt
from PySide6.QtWidgets import QCheckBox, QSizePolicy, QWidget

from .field_input import FieldInput


class FieldCheckbox (FieldInput):
    def __init__(self, name, info):
        super().__init__(name, info)
        self.field = None

    def create_widget(self, parent) -> QWidget:
        self.field = QCheckBox("")
        self.field.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.field.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.add_tooltip()
        return self.field

    def set_value(self, value):
        self.field.setChecked(value)

    def get_value(self):
        return  self.field.isChecked()
