import logging

from app.main.model.blacklist_token import BlacklistToken
from app.main.repository.blacklist_repository import BlacklistRepository as Repo
from app.main.util.response.auth_response import AuthResponse


def save_token(auth_token: str):
    try:
        blacklist_token = BlacklistToken(token=auth_token)
        Repo.get().save(blacklist_token)
        return AuthResponse.successfully_logged_out().get()
    except Exception as e:
        logging.exception(e)
        return AuthResponse.unauthorized("Unable to log out")


def is_token_blacklisted(auth_token):
    token = Repo.get().match(primary_value=auth_token)
    return token is not None
