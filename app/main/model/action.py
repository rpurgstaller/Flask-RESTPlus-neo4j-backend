class Action:

    def __init__(self, data, action_type, date):
        self.data = data
        self._action_type = action_type
        self.date = date

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def action_type(self):
        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        self._action_type = action_type

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date
