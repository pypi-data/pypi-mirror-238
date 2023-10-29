from functools import partial
from pathlib import Path

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QSizePolicy, QPushButton, QFileDialog, QHBoxLayout

from .field_input import FieldInput


class FieldFileSelect(FieldInput):

    def __init__(self, name, info):
        super().__init__(name, info)
        self.last_folder = None
        self.pattern = self.info.get("ui_pattern", "*.*")

    def create_widget(self, parent) -> QWidget:
        self.field = QLineEdit(parent)
        self.field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        file_btn = QPushButton("...")
        file_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.set_tooltip(file_btn)
        self.field.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        file_btn.setFixedWidth(30)
        file_btn.clicked.connect(partial(self.select_file, self.pattern, parent))
        form_edit = QWidget()
        file_layout = QHBoxLayout(form_edit)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.addWidget(self.field)
        file_layout.addWidget(file_btn)

        return form_edit

    def set_tooltip(self, btn:QPushButton):
        btn.setToolTip(f"{self.tr('file pattern is')} {self.pattern}")

    def select_file(self, pattern, parent):
        last_name = self.get_value()
        start_dir = "."
        if last_name:
            start_dir = str(Path(last_name).parent.absolute())
        elif self.last_folder:
            start_dir = self.last_folder
        filename, ret_filter = QFileDialog.getOpenFileName(parent=parent,
                                                           caption=self.tr('Select File'),
                                                           dir=start_dir,
                                                           filter=pattern)
        if filename:
            self.set_value(filename)
            self.last_folder = str(Path(filename).parent.absolute())
