from py2neo.ogm import Property


class NotNullProperty(Property):

    def __set__(self, instance, value):
        if value is not None:
            super().__set__(instance, value)

