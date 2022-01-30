import json
import unittest
from http.client import CREATED

from app.main.util.dto.user_dto import UserDto
from main.service.user_service import delete_marked
from test.integration.base import BaseIntegrationTestCase

from app.main.model.user import User

DEFAULT_PASSWORD = '123456'

test_users = []

CONTENT_TYPE = 'application/json'


def get_ns():
    return UserDto.NAMESPACE_NAME + '/'


def _get_test_user():
    user = User.create(username='username' + str(len(test_users) + 1), password=DEFAULT_PASSWORD, email='test@test.com')
    test_users.append(user)
    return user


def register_user(self, user, password):
    return self.client.post(
        get_ns(),
        data=json.dumps(dict(
            email=user.email,
            username=user.username,
            password=password
        )),
        content_type=CONTENT_TYPE
    )


def delete_user(self, public_id):
    return self.client.delete(
        get_ns() + public_id,
        content_type=CONTENT_TYPE
    )


def get_user(self, public_id):
    return self.client._get(
        get_ns() + public_id,
        content_type=CONTENT_TYPE
    )


class TestUser(BaseIntegrationTestCase):

    def test_user(self):
        user = _get_test_user()
        with self.client:
            # REGISTRATION
            user_response = register_user(self, user, DEFAULT_PASSWORD)
            response_data = json.loads(user_response.data.decode())

            #self.assertTrue(response_data['Authorization'])
            self.assertTrue(response_data[User.PROPERTY_NAME_PUBLIC_ID])
            self.assertEqual(user_response.status_code, CREATED)
            user.public_id = response_data[User.PROPERTY_NAME_PUBLIC_ID]

            # GET USER
            response_get_user = get_user(self, user.public_id)
            response_data_get_user = json.loads(response_get_user.data.decode())
            self.assertEqual(response_data_get_user.status_code, )
            self.assertEqual(user.public_id, response_data_get_user[User.PROPERTY_NAME_PUBLIC_ID])
            self.assertEqual(user.username, response_data_get_user[User.PROPERTY_NAME_USERNAME])
            self.assertEqual(user.email, response_data_get_user[User.PROPERTY_NAME_EMAIL])
            self.assertEqual(user.public_id, response_data_get_user[User.PROPERTY_NAME_PUBLIC_ID])
            self.assertIsNone(response_data_get_user[User.PROPERTY_NAME_PASSWORD])

            # MARK AS DELETED
            response_del_user = delete_user(self, user.public_id)
            response_get_user = get_user(self, user.public_id)
            response_data_get_user = json.loads(response_get_user.data.decode())

    def tearDown(self):
        for user in test_users:
            delete_user(user.public_id)
        delete_marked()


if __name__ == '__main__':
    unittest.main()
