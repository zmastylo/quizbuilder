# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=R0903

"""Auth module models."""


from pydantic.main import BaseModel


class BaseUser(BaseModel):
    """Base user model."""

    email: str
    first_name: str
    last_name: str


class NewUser(BaseUser):
    """New user model: used for user signup."""

    password: str
