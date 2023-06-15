# pylint: disable=C0115

"""Custom exception module."""

from http import HTTPStatus


class CustomError(Exception):
    def __init__(self, message=None):
        if message:
            self.message = message


class BadRequestError(CustomError):
    code = HTTPStatus.BAD_REQUEST.value
    error_code = HTTPStatus.BAD_REQUEST.name
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundError(CustomError):
    code = HTTPStatus.NOT_FOUND.value
    error_code = HTTPStatus.NOT_FOUND.name
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenError(CustomError):
    code = HTTPStatus.FORBIDDEN.value
    error_code = HTTPStatus.FORBIDDEN.name
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedError(CustomError):
    code = HTTPStatus.UNAUTHORIZED.value
    error_code = HTTPStatus.UNAUTHORIZED.name
    message = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntityError(CustomError):
    code = HTTPStatus.UNPROCESSABLE_ENTITY.value
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY.name
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueError(CustomError):
    code = HTTPStatus.UNPROCESSABLE_ENTITY.value
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY.name
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DecodeTokenError(CustomError):
    code = 400
    error_code = "TOKEN_DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenError(CustomError):
    code = 400
    error_code = "TOKEN_EXPIRE_TOKEN"
    message = "expired token"


class PasswordDoesNotMatchError(CustomError):
    code = 401
    error_code = "USER_PASSWORD_DOES_NOT_MATCH"
    message = "password does not match"


class DuplicateEmailOrNicknameError(CustomError):
    code = 400
    error_code = "USER_DUPLICATE_EMAIL"
    message = "duplicate email"


class UserNotFoundError(CustomError):
    code = 404
    error_code = "USER_NOT_FOUND"
    message = "user not found"
