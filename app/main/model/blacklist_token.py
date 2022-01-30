import datetime

from app.main.model.md_model import MdModel


class BlacklistToken(MdModel):

    PROPERTY_NAME_TOKEN = 'token'
    PROPERTY_NAME_BLACKLISTED_ON = 'blacklisted_on'

    LABEL_NAME_TOKEN = 'BlacklistToken'

    __primarykey__ = '__id__'

    __primarylabel__ = LABEL_NAME_TOKEN

    def __init__(self, token: str):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    @property
    def blacklisted_on(self):
        return self._blacklisted_on

    @blacklisted_on.setter
    def blacklisted_on(self, blacklisted_on: datetime):
        self._blacklisted_on = blacklisted_on
