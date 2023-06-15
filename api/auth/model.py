# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=R0903

"""Authorization specific models."""


from typing import Optional

from pydantic.main import BaseModel


class Token(BaseModel):
    """Token model representing the actual token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model that contains username."""

    username: Optional[str] = None
