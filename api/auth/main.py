"""Authorization module functionality providing all
needed methods for token based authorization."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWTClaimsError

from api.auth import credentials_exception, oauth2_scheme, pwd_context
from core.config import get_config
from database.repository import RepositoryFactory, get_repository
from model import User


def verify_password(plain_password, hashed_password):
    """Validates plain and hashed password.
    :param plain_password: Plain text user password
    :param hashed_password: Hashed user password (from DB)
    :return: True or False"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Password hashing
    :param password: Plain text password
    :return: hashed password"""
    return pwd_context.hash(password)


def create_access_token(
    *, data: dict, secret_key: str, algorithm: str, delta: Optional[timedelta] = None
):
    """Creates access token.
    :param data: Data that should be included in the access token
    :param secret_key: Secret key for token encoding
    :param algorithm: hashing algo
    :param delta: Token expiry time (default is 90 min)
    :return: JWT access token"""

    expire_data = timedelta(minutes=90) if not delta else delta
    expire = datetime.utcnow() + expire_data

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_username_from_access_token(
    token: str, secret_key: str, algorithm: str
) -> Optional[str]:
    """Decodes a token and returns the "sub" (= username) of the decoded token.
    :param token: JWT access token
    :param secret_key: Secret key used for decoding
    :param algorithm: Token decoding algorithm
    :return: username"""

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        return username
    except (JWTError, ExpiredSignatureError, JWTClaimsError) as exc:
        raise exc


def get_user_from_token(
    *,
    token: str = Depends(oauth2_scheme),
    repo: RepositoryFactory = Depends(get_repository)
) -> Optional[User]:
    """Extracts the current user from the JWT Token
    :param token: JWT access token
    :param repo: repository factory
    :return: Current user"""

    token_info = get_config().TOKEN_INFO
    username = get_username_from_access_token(
        token=token,
        secret_key=token_info.jwt_signature,
        algorithm=token_info.jwt_algorithm,
    )
    user: Optional[User] = repo.user.get(username)
    return user


def get_current_active_user(
    current_user: User = Depends(get_user_from_token),
) -> Optional[User]:
    """Extracts current and active user.
    :param current_user: current and active user
    :return: Current active user"""

    if not current_user or not current_user.active:
        raise credentials_exception
    return current_user
