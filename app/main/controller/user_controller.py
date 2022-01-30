import logging
from http.client import NOT_FOUND, CREATED, OK

from flask import request
from flask_restplus import Resource

from app.main.util.dto.user_dto import UserDto
from ..model.user import User
from ..service.user_service import create_user, get, update, mark_as_deleted, get_all
from ..util.exceptions.user_exceptions import UserNotFoundError
from ..util.response.user_response import UserResponse

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        return get_all()

    @api.response(CREATED, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.json
        return create_user(username=data[User.PROPERTY_NAME_USERNAME],
                           email=data[User.PROPERTY_NAME_EMAIL],
                           password=data[User.PROPERTY_NAME_PASSWORD])


@api.route('/<string:public_id>')
@api.param('public_id', 'The User identifier')
@api.response(NOT_FOUND, 'User not found.')
class Users(Resource):
    @api.doc('get a user by public id')
    @api.marshal_with(_user)
    def get(self, public_id):
        return get(public_id=public_id)

    @api.doc('delete a user by public id')
    @api.marshal_with(_user)
    def delete(self, public_id):
        modifier = "System" # TODO check authentication token
        return mark_as_deleted(public_id, modifier)

    @api.doc('update a user')
    @api.marshal_with(_user)
    def put(self, public_id):
        data = request.json
        username = data.get(User.PROPERTY_NAME_USERNAME)
        email = data.get(User.PROPERTY_NAME_EMAIL)
        password = data.get(User.PROPERTY_NAME_PASSWORD)
        return update(public_id=public_id, username=username, email=email, password=password)





