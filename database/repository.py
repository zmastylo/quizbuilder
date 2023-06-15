# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=R0903

"""Database repository module."""

from abc import ABC, abstractmethod

from mongoengine import Document

from model import Quiz, QuizSolution, User


class IRepository(ABC):
    """Base repository class."""

    @abstractmethod
    def get(self, key):
        """Gets an entity by id/primary key.
        :param key: Entity primary key
        :return: Entity object"""

    @abstractmethod
    def filter(self, **kwargs):
        """Filters an entity.
        :param kwargs: Filter operations
        :return: List of entities"""

    @abstractmethod
    def persist(self, item):
        """Saves or updates an entity.
        :param item: Entity to save
        :return: The saved entity"""

    @abstractmethod
    def delete(self, item):
        """Deletes an entity.
        :param item: The entity that should be deleted
        :return: None"""


class MongoRepository(IRepository):
    """Mongo repository class."""

    def __init__(self, model):
        """Constructor
        :param model: model to use in repository"""

        self._model = model

    def get(self, key):
        result = self._model.objects(pk=key).first()
        return result

    def filter(self, **kwargs):
        limit, skip, only = (
            kwargs.pop("limit", 50),
            kwargs.pop("skip", 0),
            kwargs.pop("only", None),
        )
        rows = self._model.objects(**kwargs).skip(skip).limit(limit)
        if only is not None:
            rows.only(*only)
        return rows

    def persist(self, item: Document) -> Document:
        item.save()
        item.reload()
        return item

    def delete(self, item: Document):
        item.delete()


class UserRepository(MongoRepository):
    """User repository providing access to user objects."""

    def __init__(self):
        super().__init__(model=User)


class QuizRepository(MongoRepository):
    """Quiz repository providing access to quiz objects."""

    def __init__(self):
        super().__init__(model=Quiz)


class QuizSolutionRepository(MongoRepository):
    """Quiz solution repository providing access to quiz solution objects."""

    def __init__(self):
        super().__init__(model=QuizSolution)


class RepositoryFactory:
    """Repository factory."""

    __UserRepository = UserRepository()
    __QuizRepository = QuizRepository()
    __QuizSolutionRepository = QuizSolutionRepository()

    def __init__(self):
        """Constructor."""

        self.user = RepositoryFactory.__UserRepository
        self.quiz = RepositoryFactory.__QuizRepository
        self.quiz_solution = RepositoryFactory.__QuizSolutionRepository


def get_repository():
    """Return repository factory. Useful for dependency
    injection."""

    return RepositoryFactory()
