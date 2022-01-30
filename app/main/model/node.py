from app.main.model.field_type import FieldType


class Node:

    def __init__(self, title: str, fields: list[FieldType]):
        self.title = title
        self.fields = fields

    def add_field(self, field: FieldType):
        self.fields.add(field)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields: list[FieldType]):
        self._fields = fields


