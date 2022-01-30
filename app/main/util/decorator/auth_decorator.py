from functools import wraps
from flask import request

from app.main.service.auth_helper import Auth


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_token = request.get('Authorization')
        data, status = Auth.get_logged_in_user(auth_token)
        token = data._get('data')

        if not token:
            return data, status

        return func(*args, **kwargs)

    return decorated
