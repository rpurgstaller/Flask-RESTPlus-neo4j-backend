import unittest
from unittest.mock import patch

from test.unit.base import BaseUnitTestCase
from app.main.model.user import User
from app.main.model.blacklist_token import ERR_MSG_TOKEN_BLACKLISTED


def create_test_user(identifier=1, username='test', email='test@test.com', password='test'):
    user = User.create(username=username, password=password, email=email)
    user.identifier = identifier
    user.username = username
    user.email = email
    user.password = password
    return user


class TestUserModel(BaseUnitTestCase):

    def test_encode_auth_token(self):
        user = create_test_user()
        auth_token = user.encode_auth_token(user.identifier)
        self.assertTrue(isinstance(auth_token, bytes))

    # @patch('app.main.repository.blacklist_repository.is_token_blacklisted')
    def test_decode_auth_token(self, mock_token_blacklisted):
        # GIVEN
        mock_token_blacklisted.return_value = False
        user = create_test_user()
        # WHEN
        auth_token = user.encode_auth_token(user.identifier)
        # THEN
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token.decode("utf-8")), 1)

    # @patch('app.main.repository.blacklist_repository.is_token_blacklisted')
    def test_decode_auth_token_blacklisted(self, mock_token_blacklisted):
        # GIVEN
        mock_token_blacklisted.return_value = True
        user = create_test_user()
        # WHEN
        auth_token = user.encode_auth_token(user.identifier)
        # THEN
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token.decode("utf-8")), ERR_MSG_TOKEN_BLACKLISTED)


if __name__ == '__main__':
    unittest.main()
