"""Authorization routing and logic."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import credentials_exception
from api.auth.main import create_access_token, verify_password
from api.auth.model import Token
from core.config import get_config
from database.repository import RepositoryFactory, get_repository
from model import User

auth_router = APIRouter(tags=["Auth"])

OathForm = OAuth2PasswordRequestForm


@auth_router.post("/token", response_model=Token)
def token(
    form_data: OathForm = Depends(OathForm),
    repo: RepositoryFactory = Depends(get_repository),
):
    """Oauth2 token endpoint.
    :param form_data: OAUTH2 form data (contains username & password)
    :param repo: repository factory
    :return: JWT token"""

    user = verify_user(form_data, repo)
    if not user:
        raise credentials_exception

    token_info = get_config().TOKEN_INFO
    access_token = create_access_token(
        data={"sub": user.email},
        secret_key=token_info.jwt_signature,
        algorithm=token_info.jwt_algorithm,
    )
    return Token(access_token=access_token, token_type="bearer")


def verify_user(form_data, repo):
    """User verification logic: given username and password
    it verifies user is valid.
    :param form_data: username and password
    :param repo: database repository
    :return: user is valid user else None"""

    user: User = repo.user.get(form_data.username)

    if user is None:
        return None

    result: bool = verify_password(form_data.password, user.password_hash)

    if not result:
        return None

    return user
