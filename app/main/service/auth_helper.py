import datetime
import logging

import jwt

from app.main.model.user import User
from ..config import key
from ..service.blacklist_service import save_token, is_token_blacklisted
from ..service.user_service import _get
from ..util.exceptions.auth_exceptions import TokenAlreadyBlacklistedError, InvalidUsernameError, InvalidPasswordError
from app.main.util.response.auth_response import AuthResponse


class Auth:

    @staticmethod
    def login_user(username: str, password: str):
        try:
            token = User.authenticate(username, password)
            return AuthResponse.successfully_logged_in(token.decode()).get()
        except InvalidUsernameError as e:
            return AuthResponse.unauthorized("Invalid Username")
        except InvalidPasswordError as e:
            return AuthResponse.unauthorized("Invalid Password")
        except Exception as e:
            logging.exception(e)
            return AuthResponse.internal_server_error().get()

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            return AuthResponse.forbidden('Invalid token. Please log in again.').get()
        if auth_token:
            try:
                User.decode_auth_token(auth_token)
                return save_token(auth_token=auth_token)
            except TokenAlreadyBlacklistedError:
                return AuthResponse.unauthorized('Token already blacklisted').get()
            except jwt.ExpiredSignatureError:
                return AuthResponse.unauthorized('Signature expired. Please log in again.').get()
            except jwt.InvalidTokenError:
                return AuthResponse.unauthorized('Invalid token. Please log in again.').get()

    @staticmethod
    def get_logged_in_user(auth_token):
        if auth_token:
            user = User.get_user_from_token(auth_token)
            if user is None:
                return AuthResponse.unauthorized('Invalid token. Please log in again.').get()
            else:
                return AuthResponse.ok().get()
        else:
            return AuthResponse.unauthorized('Provide a valid auth token.').get()

