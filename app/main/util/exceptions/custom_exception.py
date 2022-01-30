import logging as log


class ExceptionWithResponse(Exception):
    def __init__(self, response_code: str):
        self.response_code = response_code

    @property
    def response_code(self):
        return self._response_code

    @response_code.setter
    def response_code(self, response_code: str):
        self._response_code = response_code


