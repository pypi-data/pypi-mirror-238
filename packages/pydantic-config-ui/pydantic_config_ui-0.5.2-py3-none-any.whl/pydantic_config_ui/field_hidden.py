from .field_input import FieldInput


class FieldHidden(FieldInput):
    def __init__(self, name, info):
        super().__init__(name, info)
        self.value = ""

    def has_ui(self) -> bool:
        return False

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value
