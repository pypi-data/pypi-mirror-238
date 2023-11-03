import logging

from PySide6.QtCore import QStringListModel, Signal, QObject
from PySide6.QtWidgets import QComboBox

logger = logging.getLogger(__name__)


class RecentCombobox(QComboBox):
    signal_entry_changed = Signal(str)

    def __init__(self, max_entries, parent=None):
        super().__init__(parent)
        self.max_entries = max_entries
        self.recent_entries = QStringListModel()
        self.update_model = False

        self.currentTextChanged.connect(self.index_changed)
        self.setModel(self.recent_entries)

    def index_changed(self, entry):
        if not self.update_model:
            self.update_recent_entries(entry)
            self.signal_entry_changed.emit(entry)

    def current_entry(self):
        if self.recent_entries.rowCount() > 0:
            return self.recent_entries.stringList()[0]
        return ""

    def set_entries(self, entry_list):
        self.recent_entries.setStringList([e for e in entry_list if e])

    def get_entries(self):
        return self.recent_entries.stringList()

    def add_or_update_entry(self, e):
        self.update_recent_entries(e)

    def remove_first_entry(self):
        self.recent_entries.removeRow(0)

    def update_recent_entries(self, entry):
        """
        using QStringListModel
        1. if not in model, insert at position 0 and show
        2. if in model, move to position 0
        :param entry: the selected or new string
        :return: no return value
        """
        entries_list = self.recent_entries.stringList()

        row = -1
        if entry in entries_list:
            row = entries_list.index(entry)

        if 0 == row or not entry:
            # entry at first position or empty
            return

        self.update_model = True
        if row > 0:
            # move to head
            logger.debug(f"move {entry} to head")
            self.recent_entries.moveRow(self.recent_entries.index(row).parent(), row,
                                        self.recent_entries.index(0).parent(), 0)
        else:
            logger.debug(f"add {entry}")
            self.recent_entries.insertRow(0)
            self.recent_entries.setData(self.recent_entries.index(0), entry)

        if 0 < self.max_entries < self.recent_entries.rowCount():
            logger.debug("remove entries")
            self.recent_entries.removeRows(self.max_entries, self.recent_entries.rowCount() - self.max_entries)

        self.update_model = False

        self.setCurrentIndex(0)
