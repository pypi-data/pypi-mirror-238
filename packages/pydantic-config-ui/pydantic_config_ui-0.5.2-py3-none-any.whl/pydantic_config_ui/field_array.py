from .field_input import FieldInput


class FieldArray(FieldInput):

    def __init__(self, name, info):
        super().__init__(name, info)

    def set_value(self, value):
        self.field.setText(",".join(value))

    def get_value(self):
        return self.field.text().split(",")
