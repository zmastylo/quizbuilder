"""Test user api module."""

import unittest

from parameterized import parameterized

from api.user.model import BaseUser
from tests.mock_client import get_auth_client, test_client
from tests.mock_repository import get_mock_repository


class TestUsersApi(unittest.TestCase):
    """Test user class."""

    def __init__(self, *args, **kwargs):
        """Constructor."""

        super().__init__(*args, **kwargs)
        self.endpoint = "/user"

    @classmethod
    def del_user(cls, email: str):
        """Helper method to delete a user given its email."""

        mock_repo = get_mock_repository()
        user_del = mock_repo.user.get(email)
        if user_del:
            mock_repo.user.delete(user_del)

    @parameterized.expand(
        [
            [{"username": "john@wick.com", "password": "_Hard_pass1"}, 200],
            [{"username": "al.pacino@gmail.com", "password": "_Hard_pass1"}, 200],
            [{"username": "al.pacino@gmail.com", "password": "invalid"}, 401],
            [{"username": "test", "password": "abcdefghijk"}, 401],
        ]
    )
    def test_login(self, data, status_code):
        """Test login functionality."""

        end_point = "/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = test_client.post(end_point, headers=headers, data=data)
        assert response.status_code == status_code

    @parameterized.expand(
        [
            ["john@wick.com", "_Hard_pass1", 200],
            ["al.pacino@gmail.com", "_Hard_pass1", 200],
            ["john@wick.com", "hdjhsh", 401],
            ["invaliduser@some.com", "pppass", 401],
        ]
    )
    def test_user_me(self, username: str, password: str, status_code: int):
        """Test if user logged in and authorized."""

        auth_client = get_auth_client(username, password)
        response = auth_client.get(f"{self.endpoint}/me")
        assert response.status_code == status_code

        if response.status_code == 200:
            current_user = BaseUser(**response.json())
            assert current_user.email == username

    @parameterized.expand(
        [
            [
                {
                    "email": "leo.messi@gmail.com",
                    "first_name": "Lionel",
                    "last_name": "Messi",
                    "password": "ValidPass_8",
                },
                200,
            ],
            [
                {
                    "email": "john@wick.com",
                    "first_name": "John",
                    "last_name": "Wick",
                    "password": "_Hard_pass1",
                },
                400,
            ],
            [
                {
                    "email": "al.pacino@gmail.com",
                    "first_name": "Irrelevant",
                    "last_name": "Irrelevant",
                    "password": "_Hard_pass1",
                },
                400,
            ],
        ]
    )
    def test_user_signup(self, data: dict, status_code: int):
        """Test user signup functionality."""

        if status_code == 200:
            self.del_user(data["email"])

        response = test_client.post(f"{self.endpoint}/signup", json=data)
        assert response.status_code == status_code
        if status_code == 200:
            current_user = BaseUser(**response.json())
            assert current_user.email == data.get("email")
            assert current_user.first_name == data.get("first_name")
            assert current_user.last_name == data.get("last_name")
