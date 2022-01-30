from flask_restplus import Namespace, fields


class AuthDto:
    NAMESPACE_NAME = 'auth'

    api = Namespace(NAMESPACE_NAME, description='authentication related operations')

    user_auth = api.model(NAMESPACE_NAME, {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
