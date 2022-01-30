import logging
from http.client import OK
from typing import Tuple

from py2neo import NodeMatch
from py2neo.ogm import ModelMatcher

from app.main.model.user import User

from app.main.util.response.user_response import UserResponse

from app.main.repository.user_repository import UserRepository as Repo
from app.main.util.exceptions.user_exceptions import EmailAlreadyTakenError, EmailValidationError, \
    UsernameAlreadyTakenError, UserNotFoundError
from app.main.util.response.response import Response


def _get(public_id: str, active_only=True) -> User:
    if active_only:
        user = Repo.get().match(primary_value=public_id).where(f'_:{User.LABEL_NAME_ACTIVE}').first()
    else:
        user = Repo.get().match(primary_value=public_id).where(f'_.{User.LABEL_NAME_ACTIVE}').first()

    if user is None:
        raise UserNotFoundError()

    return user


def get(public_id: str) -> Tuple[dict, int]:
    try:
        return _get(public_id)
    except UserNotFoundError as user_exception:
        logging.exception("Unable to get user, exception: " + str(user_exception))
        return UserResponse.from_exception(user_exception).get()
    except Exception as e:
        logging.exception("Unable to get user, exception: " + str(e))
        return UserResponse.internal_server_error().get()

    return user


def get_all(active_only=True) -> Response:
    try:
        if active_only:
            val = Repo.get().node_match(User.LABEL_NAME_ACTIVE)
            return val.all()

        return Repo.get().node_match()
    except Exception as e:
        logging.exception(e)
        return UserResponse.internal_server_error().get()


def save(*user: User) -> None:
    Repo.get().save(*user)


def create_user(username: str, email: str, password: str) -> Response:
    try:
        user = User.create(username=username, password=password, email=email)
        save(user)
        response = UserResponse.created()
        response.set(User.PROPERTY_NAME_PUBLIC_ID, user.public_id)
        return response.get()
    except (EmailValidationError, UsernameAlreadyTakenError, EmailAlreadyTakenError) as user_exception:
        return UserResponse.from_exception(user_exception).get()
    except Exception as e:
        logging.exception(e)
        return UserResponse.internal_server_error().get()


def update(public_id: str, username: str, email: str, password: str) -> Response:
    try:
        user = _get(public_id)
        user.username = username
        user.email = email
        user.password = password
        save(user)
    except (EmailValidationError, UsernameAlreadyTakenError, EmailAlreadyTakenError, UserNotFoundError) \
            as user_exception:
        return UserResponse.from_exception(user_exception).get()
    except Exception as e:
        logging.exception(e)
        return UserResponse.internal_server_error().get()


def mark_as_deleted(public_id: str, modifier: str) -> Response:
    try:
        user = _get(public_id)
        user.set_deleted_on(modifier)
        save(user)
    except UserNotFoundError as user_exception:
        return UserResponse.from_exception(user_exception).get()
    except Exception as e:
        logging.exception(e)
        return UserResponse.internal_server_error().get()


def delete_marked() -> None:
    Repo.get().delete_marked()


def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.node_id)
        response = UserResponse()
        response.set_created()
        response.set(key=User.PROPERTY_NAME_PUBLIC_ID, value=user.public_id)
        return response.get()
    except Exception as e:
        logging.exception(e)
        return UserResponse.internal_server_error().get()
