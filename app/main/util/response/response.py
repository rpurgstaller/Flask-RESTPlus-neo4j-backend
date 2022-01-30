from __future__ import annotations
from http.client import CONFLICT, CREATED, UNAUTHORIZED, INTERNAL_SERVER_ERROR, NOT_FOUND, OK
from typing import Tuple

from app.main.util.exceptions.custom_exception import ExceptionWithResponse


class Response(object):

    _KEY_STATUS = 'status'
    _KEY_MSG = 'message'

    _STATUS_FAIL = 'fail'
    _STATUS_SUCCESS = 'success'

    def __init__(self):
        self._attribs = {}
        self.response_code = None

    @classmethod
    def from_exception(cls, e: Exception) -> Response:
        response = cls()
        if isinstance(e, ExceptionWithResponse):
            response.response_code = e.response_code
            response.set_msg(str(e))
        else:
            response.set_internal_error()

        return response

    @classmethod
    def created(cls) -> Response:
        response = cls()
        response.set_status(cls._STATUS_SUCCESS)
        response.response_code = CREATED
        return response

    @classmethod
    def not_found(cls) -> Response:
        response = cls()
        response.set_status(cls._STATUS_FAIL)
        response.response_code = NOT_FOUND
        return response

    @classmethod
    def internal_server_error(cls) -> Response:
        response = cls()
        response.set_internal_error()
        return response

    @classmethod
    def ok(cls) -> Response:
        response = cls()
        response.set_status(cls._STATUS_SUCCESS)
        response.response_code = OK
        return response

    def set_conflict(self) -> None:
        self.set_status(self._STATUS_FAIL)
        self.response_code = CONFLICT

    def set_internal_error(self) -> None:
        self.set_status(self._STATUS_FAIL)
        self.response_code = INTERNAL_SERVER_ERROR

    @property
    def response_code(self):
        return self._response_code

    @response_code.setter
    def response_code(self, response_code: int) -> None:
        self._response_code = response_code

    def set_msg(self, msg: str) -> None:
        self._attribs[self._KEY_MSG] = msg

    def set_status(self, key: str) -> None:
        self._attribs[self._KEY_STATUS] = key

    def set(self, key: str, value: str) -> None:
        self._attribs[key] = value

    def get(self) -> Tuple[dict, int]:
        return self._attribs, self.response_code

