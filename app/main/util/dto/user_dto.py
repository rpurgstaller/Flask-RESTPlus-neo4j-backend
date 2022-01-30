from flask_restplus import Namespace, fields


class UserDto:
    NAMESPACE_NAME = 'users'

    api = Namespace(NAMESPACE_NAME, description='user related operations')

    user = api.model(NAMESPACE_NAME, {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=False, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'created_on': fields.String(required=False, description='User registration date/time')
    })

