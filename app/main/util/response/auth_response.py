from http.client import UNAUTHORIZED, FORBIDDEN

from app.main.util.response.response import Response


class AuthResponse(Response):

    @classmethod
    def successfully_logged_out(cls):
        response = cls.ok()
        response.set_msg("Successfully logged out")
        return response

    @classmethod
    def successfully_logged_in(cls, token: str):
        response = cls.ok()
        response.set_msg("Successfully logged in")
        response.set('Authorization', token)
        return response

    @classmethod
    def unauthorized(cls, msg: str):
        response = cls()
        response.set_status(response._STATUS_FAIL)
        response.response_code = UNAUTHORIZED
        response.set_msg(msg)
        return response

    @classmethod
    def forbidden(cls, msg: str):
        response = cls()
        response.set_status(response._STATUS_FAIL)
        response.response_code = FORBIDDEN
        response.set_msg(msg)
        return response
