import unittest
import json
from app.main.model.user import User
from test.unit.base import BaseUnitTestCase
from unittest.mock import patch


DEFAULT_PASSWORD = '123456'


def get_test_user():
    user = User.create(username='username', password=DEFAULT_PASSWORD, email='test@test.com')
    user.identifier = 1
    user.username = 'username'
    user.password = DEFAULT_PASSWORD
    user.email = 'test@test.com'
    return user


def register_user(self, user, password):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email=user.email,
            username=user.username,
            password=password
        )),
        content_type='application/json'
    )


def login_user(self, user, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=user.email,
            password=password
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseUnitTestCase):

    # @patch('app.main.repository.user_repository.create_user')
    # @patch('app.main.repository.user_repository.is_in_use')
    # @patch('app.main.repository.blacklist_repository.is_token_blacklisted')
    def test_user_registration(self, mock_token_blacklisted, mock_user_in_use, mock_save_user):
        # GIVEN
        user = get_test_user()
        mock_token_blacklisted.return_value = False
        mock_user_in_use.return_value = False
        mock_save_user.return_value = user.identifier
        with self.client:
            # WHEN
            user_response = register_user(self, user, DEFAULT_PASSWORD)
            response_data = json.loads(user_response.data.decode())
            # THEN
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(user_response.status_code, 201)

    # @patch('app.main.repository.user_repository.get_user')
    def test_user_login(self, mock_get_user):
        # GIVEN
        user = get_test_user()
        mock_get_user.return_value = user
        # WHEN
        login_response = login_user(self, user, DEFAULT_PASSWORD)
        data = json.loads(login_response.data.decode())
        # THEN
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)

    # @patch('app.main.repository.user_repository.get_user')
    def test_user_login_no_user_found(self, mock_get_user):
        # GIVEN
        user = get_test_user()
        mock_get_user.return_value = None
        # WHEN
        login_response = login_user(self, user, DEFAULT_PASSWORD)
        data = json.loads(login_response.data.decode())
        # THEN
        self.assertTrue(data['status'] == 'fail')
        self.assertEqual(login_response.status_code, 401)

    # @patch('app.main.repository.user_repository.get_user')
    def test_user_login_wrong_password(self, mock_get_user):
        # GIVEN
        user = get_test_user()
        mock_get_user.return_value = user
        # WHEN
        login_response = login_user(self, user, 'wrong password')
        data = json.loads(login_response.data.decode())
        # THEN
        self.assertTrue(data['status'] == 'fail')
        self.assertEqual(login_response.status_code, 401)

    # @patch('app.main.repository.blacklist_repository.save_token')
    # @patch('app.main.repository.blacklist_repository.is_token_blacklisted')
    # @patch('app.main.repository.user_repository.get_user')
    def test_user_logout(self, mock_get_user, mock_token_blacklisted, mock_save_blacklisted_token):
        # GIVEN
        user = get_test_user()
        mock_get_user.return_value = user
        mock_token_blacklisted.return_value = False
        mock_save_blacklisted_token.return_value = 1
        # WHEN
        # login
        login_response = login_user(self, user, DEFAULT_PASSWORD)
        data = json.loads(login_response.data.decode())
        # logout
        response = self.client.post(
            '/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_response.data.decode()
                )['Authorization']
            )
        )
        data = json.loads(response.data.decode())
        # THEN
        self.assertTrue(data['status'] == 'success')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
