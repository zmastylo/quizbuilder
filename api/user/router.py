"""User routing and endpoint handling logic."""

from fastapi import APIRouter, Depends, HTTPException

from api.auth import pwd_context
from api.auth.main import get_current_active_user
from api.user.model import BaseUser, NewUser
from database.repository import RepositoryFactory, get_repository
from model import User

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/signup", response_model=BaseUser)
def signup(new_user: NewUser, repo: RepositoryFactory = Depends(get_repository)):
    """User signup endpoint
    :param new_user: New user data
    :param repo: repository factory
    :return: user model"""
    if repo.user.get(new_user.email) is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        password_hash=pwd_context.hash(new_user.password),
        active=True,
    )

    user: User = repo.user.persist(user)
    return BaseUser(
        email=user.email, first_name=user.first_name, last_name=user.last_name
    )


@user_router.get("/me", response_model=BaseUser)
def get_current_user(current_user: User = Depends(get_current_active_user)):
    """Gets the user information of the current logged-in user
    :param current_user: Current user
    :return: Information about the current user"""

    return BaseUser(
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
    )
