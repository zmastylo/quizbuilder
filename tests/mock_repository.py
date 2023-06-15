# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=R0903

"""Mock repository module providing mock user, quiz, and
quiz solution object repository."""

import json
from typing import Dict

from database.repository import IRepository
from model import Quiz, User
from tests.mock_repository_data import mock_quiz_data, mock_user_data


class MockUserRepository(IRepository):
    """User model mock repository."""

    def __init__(self, user_data: Dict = None):
        self._repo = {} if not user_data else user_data

    def get(self, key):
        return self._repo.get(key, None)

    def filter(self, **kwargs):
        pass

    def persist(self, item: User):
        key = item.email
        self._repo[key] = item
        return item

    def delete(self, item: User):
        key = item.email
        self._repo.pop(key)


class MockQuizRepository(IRepository):
    """Quiz model mock repository."""

    def __init__(self, quiz_data: Dict = None):
        self._repo = {} if not quiz_data else quiz_data

    def get(self, key):
        result = self._repo.get(key, None)
        return result

    def filter(self, **kwargs):
        result = [self.helper(key, value) for key, value in kwargs.items()]
        return result

    def persist(self, item: Quiz):
        key = item.identifier
        self._repo[key] = item
        return item

    def delete(self, item: Quiz):
        key = item.identifier
        self._repo.pop(key)

    def helper(self, key, value):
        key_split = "__"
        key = key.split(key_split)[0] if key_split in key else key
        for quiz in self._repo.values():
            quiz_json = json.loads(quiz.to_json())
            if value in quiz_json[key]:
                yield quiz_json


class MockRepositoryFactory:
    """Mock repository factory."""

    __MockUserRepository = MockUserRepository(mock_user_data)
    __MockQuizRepository = MockQuizRepository(mock_quiz_data)

    def __init__(self):
        """Constructor."""

        self.user = MockRepositoryFactory.__MockUserRepository
        self.quiz = MockRepositoryFactory.__MockQuizRepository


def get_mock_repository():
    """Gets mock repository factory: used for dependency injection."""

    return MockRepositoryFactory()
