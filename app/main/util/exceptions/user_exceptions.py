from http.client import CONFLICT, BAD_REQUEST, NOT_FOUND

from app.main.util.exceptions.custom_exception import ExceptionWithResponse


class EmailValidationError(ExceptionWithResponse):
    def __init__(self):
        super().__init__(response_code=BAD_REQUEST)

    def __str__(self):
        return 'Invalid Email.'


class UsernameAlreadyTakenError(ExceptionWithResponse):
    def __init__(self):
        super().__init__(response_code=CONFLICT)

    def __str__(self):
        return 'Username already taken.'


class EmailAlreadyTakenError(ExceptionWithResponse):
    def __init__(self):
        super().__init__(response_code=CONFLICT)

    def __str__(self):
        return 'Email already taken.'


class UserNotFoundError(ExceptionWithResponse):
    def __init__(self):
        super().__init__(response_code=NOT_FOUND)

    def __str__(self):
        return 'User not found'

