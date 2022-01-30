from __future__ import annotations

import datetime
import re

import jwt
import shortuuid
from py2neo.ogm import Property, Label

from .md_model import MdModel
from .. import flask_bcrypt
from ..config import key
from ..service.blacklist_service import is_token_blacklisted
from ..util.decorator.property_decorator import not_null_property, regexp_property
from ..util.exceptions.auth_exceptions import TokenAlreadyBlacklistedError, InvalidUsernameError, InvalidPasswordError
from ..util.exceptions.user_exceptions import EmailValidationError, UserNotFoundError


class User(MdModel):
    """
    Model of a User - used for authentication
    """

    REGEXP_EMAIL = '[^@]+@[^@]+\\.[^@]+'

    SIGNING_ALGORITHM: str = 'HS256'

    PROPERTY_NAME_USERNAME: str = 'username'
    PROPERTY_NAME_PASSWORD: str = 'password'
    PROPERTY_NAME_EMAIL: str = 'email'
    PROPERTY_NAME_PUBLIC_ID: str = 'public_id'
    PROPERTY_NAME_CREATED_ON: str = 'created_on'
    PROPERTY_NAME_MODIFIER: str = 'modifier'
    PROPERTY_NAME_DELETED_ON: str = 'deleted_on'
    PROPERTY_NAME_DELETED_BY: str = 'deleted_by'

    LABEL_NAME_USER: str = 'User'
    LABEL_NAME_ACTIVE: str = 'Active'
    LABEL_NAME_DELETED: str = 'Deleted'

    __primarykey__ = PROPERTY_NAME_PUBLIC_ID

    _public_id = Property(PROPERTY_NAME_PUBLIC_ID)
    _username = Property(PROPERTY_NAME_USERNAME)
    _email = Property(PROPERTY_NAME_EMAIL)
    _password_hash = Property(PROPERTY_NAME_PASSWORD)
    _created_on = Property(PROPERTY_NAME_CREATED_ON)
    _modifier = Property(PROPERTY_NAME_MODIFIER)
    _deleted_on = Property(PROPERTY_NAME_DELETED_ON)
    _deleted_by = Property(PROPERTY_NAME_DELETED_BY)

    __primarylabel__ = LABEL_NAME_USER

    _active = Label(LABEL_NAME_ACTIVE)

    def __init__(self, username: str, password: str, email: str, public_id: str, created_on: datetime, active: bool):
        super().__init__()
        self.username = username
        self.password = password
        self.email = email
        self.public_id = public_id
        self.created_on = created_on
        self.active = active

    @classmethod
    def create(cls, username: str, password: str, email: str, active: bool = True) -> User:
        return User(username=username, password=password, email=email, public_id=str(shortuuid.uuid()),
                    created_on=datetime.datetime.utcnow(), active=active)

    @classmethod
    def get_user_from_token(cls, auth_token: str):
        identity = User.decode_auth_token(auth_token)
        return cls.get(identity)

    @staticmethod
    def authenticate(username: str, password: str):
        user = User.match_by_username(username)

        if user is None:
            raise InvalidUsernameError()
        if not user.check_password(password):
            raise InvalidPasswordError()

        return User.encode_auth_token(user.identity)

    @staticmethod
    def decode_auth_token(auth_token: str):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        payload = jwt.decode(auth_token, key, algorithms=[User.SIGNING_ALGORITHM])
        if is_token_blacklisted(auth_token):
            raise TokenAlreadyBlacklistedError()

        return payload['sub']

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            key,
            algorithm=User.SIGNING_ALGORITHM
        )

    @property
    def node_id(self):
        return self.__node__.identity

    @node_id.setter
    def node_id(self, identifier):
        raise AttributeError('node id: write-only field')

    @property
    def public_id(self):
        return self._public_id

    @public_id.setter
    def public_id(self, public_id):
        self._public_id = public_id

    @property
    def username(self):
        return self._username

    @username.setter
    @not_null_property
    def username(self, username):
        self._username = username

    @property
    def email(self):
        return self._email

    @email.setter
    @not_null_property
    @regexp_property(regexp=REGEXP_EMAIL)
    def email(self, email):
        self._email = email

    @property
    def created_on(self):
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        self._created_on = created_on

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self._password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    @property
    def deleted(self):
        return self._deleted

    def set_deleted_on(self, modifier):
        self._active = False
        self._deleted_on = datetime.datetime.utcnow()
        self._deleted_by = modifier

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self._password_hash, password)

    @classmethod
    def match_by_email(cls, email: str) -> User:
        user_list = cls.match_by_attr(cls.PROPERTY_NAME_EMAIL, email)
        if len(user_list) > 0:
            return user_list[0]
        return None

    @classmethod
    def match_by_username(cls, username: str) -> User:
        user_list = cls.match_by_attr(cls.PROPERTY_NAME_USERNAME, username)
        if len(user_list) > 0:
            return user_list[0]
        return None

    def __repr__(self):
        return f"<User '{self.username}'>"
