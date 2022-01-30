from app.main.util.exceptions.custom_exception import ExceptionWithResponse


class InvalidValueError(ExceptionWithResponse):
    def __init__(self):
        super().__init__(response_code=BAD_REQUEST)

    def __str__(self):
        return 'Invalid Value '