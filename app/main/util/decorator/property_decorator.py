import re
from functools import wraps


def not_null_property(func):
    @wraps(func)
    def decorated(instance, value):
        if not value:
            return

        return func(instance, value)

    return decorated


def regexp_property(regexp):
    def inner_function(func):
        @wraps(func)
        def decorated(instance, value):
            if not re.search(regexp, value):
                return #raise EmailValidationError()

            return func(instance, value)

        return decorated
    return inner_function
