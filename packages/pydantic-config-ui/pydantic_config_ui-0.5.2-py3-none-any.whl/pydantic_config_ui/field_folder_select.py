from functools import partial
from pathlib import Path

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QSizePolicy, QPushButton, QFileDialog, QHBoxLayout

from .field_file_select import FieldFileSelect


class FieldFolderSelect(FieldFileSelect):

    def __init__(self, name, info):
        super().__init__(name, info)
        self.pattern = ""

    def set_tooltip(self, btn: QPushButton):
        btn.setToolTip(self.tr('select a folder'))

    def select_file(self, pattern, parent):
        start_dir = "."
        if self.get_value():
            start_dir = str(Path(self.get_value()).parent.absolute())
        elif self.last_folder:
            start_dir = self.last_folder
        folder = QFileDialog.getExistingDirectory(parent=parent,
                                                           caption=self.tr('Select Folder'),
                                                           dir=start_dir)
        if folder:
            self.set_value(folder)
            self.last_folder = str(Path(folder).parent.absolute())
