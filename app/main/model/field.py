from app.main.model.field_type import FieldType


class Field:

    def __init__(self, field_type: FieldType, value):
        self.field_type = field_type
        self.value = value

    @property
    def field_type(self):
        return self._field_type

    @field_type.setter
    def field_type(self, field_type: FieldType):
        self._field_type = field_type
