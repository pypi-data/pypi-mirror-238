from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLineEdit, QSizePolicy, QWidget


class FieldInput(QObject):

    def __init__(self, name, info):
        super().__init__()
        self.field = None
        self.info = info
        self.name = name

    def has_ui(self):
        return "hidden" not in self.info

    def add_tooltip(self):
        if self.field is not None and "description" in self.info:
            self.field.setToolTip(self.info["description"])

    def create_widget(self, parent) -> QWidget:
        self.field = QLineEdit(parent)
        self.field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_tooltip()
        return self.field

    def set_value(self, value):
        self.field.setText(str(value))

    def get_value(self):
        return self.field.text()
