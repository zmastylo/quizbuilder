"""Quiz testing module."""

import unittest

import pytest
from parameterized import parameterized
from pydantic import ValidationError

from api.quiz.model import NewQuiz
from tests.helper import get_entity, get_quiz_json_data
from tests.mock_client import get_auth_client, test_client


class TestQuiz(unittest.TestCase):
    """Quiz testing class."""

    def __init__(self, *args, **kwargs):
        """Constructor."""

        super().__init__(*args, **kwargs)
        self.endpoint = "/quiz"

    @parameterized.expand([[2, 200], [3, 200], [200, 404]])
    def test_get_quiz(self, quiz_id: int, status_code: int):
        """Test get quiz endpoint."""

        response = test_client.get(f"{self.endpoint}/{quiz_id}")
        assert response.status_code == status_code

    @parameterized.expand(
        [
            ["john@wick.com", "_Hard_pass1", 200],
            ["al.pacino@gmail.com", "_Hard_pass1", 200],
            ["john@wick.com", "hdjhsh", 401],
            ["invaliduser@some.com", "pppass", 401],
        ]
    )
    def test_create_quiz(self, username: str, password: str, status_code: int):
        """Test quiz create endpoint/functionality."""

        auth_client = get_auth_client(username, password)
        new_quiz = get_entity("quiz_countries.json", NewQuiz)
        response = auth_client.post(f"{self.endpoint}", json=new_quiz.dict())
        assert response.status_code == status_code

    @parameterized.expand(
        [
            ["quiz_countries_invalid_too_many_answers.json"],
            ["quiz_countries_invalid_too_many_questions.json"],
        ]
    )
    def test_create_quiz_validation(self, file_name: str):
        """Test quiz validation."""

        with pytest.raises(ValidationError):
            get_entity(file_name, NewQuiz)

    @parameterized.expand(
        [
            ["al.pacino@gmail.com", "_Hard_pass1", 3, 200],
            ["al.pacino@gmail.com", "_Hard_pass1", 4, 400],
            # ["john@wick.com", "_Hard_pass1", 100, 404],
            ["invaliduser@some.com", "pppass", 3, 401],
        ]
    )
    def test_update_quiz(
        self, username: str, password: str, quiz_id: int, status_code: int
    ):
        """Test quiz update endpoint/functionality."""

        auth_client = get_auth_client(username, password)
        response = auth_client.put(
            f"{self.endpoint}/{quiz_id}", json=get_quiz_json_data(quiz_id)
        )
        assert response.status_code == status_code

    @parameterized.expand(
        [
            ["john@wick.com", "_Hard_pass1", 1, 200],
            ["invaliduser@some.com", "pppass", 2, 401],
        ]
    )
    def test_delete_quiz(
        self, username: str, password: str, quiz_id: int, status_code: int
    ):
        """Test quiz delete endpoint/functionality."""

        auth_client = get_auth_client(username, password)
        response = auth_client.delete(f"{self.endpoint}/{quiz_id}")
        assert response.status_code == status_code
