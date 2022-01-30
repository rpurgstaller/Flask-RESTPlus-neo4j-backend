from __future__ import annotations

from app.main.util.response.response import Response


class UserResponse(Response):

    @classmethod
    def created(cls) -> UserResponse:
        response = super().created()
        response.set_msg('Successfully registered')
        return response

    @classmethod
    def not_found(cls) -> UserResponse:
        response = super().not_found()
        response.set_msg('User not found')
        return response

    def set_conflict(self, msg: str) -> None:
        super().set_conflict()
        super().set_msg(msg)

    def set_unauthorized(self) -> None:
        super().set_unauthorized()
        super().set_msg('Authorization failed')

