# pylint: disable=R0903

"""Config module providing application configuration."""

import os
from functools import lru_cache

from pydantic import BaseSettings


class TokenSettings(BaseSettings):
    """JWT Token settings."""

    jwt_local_signature = (
        "b05c64ea3955e0c318a2f963c8e3221234e2ab70481f2fd69cdac1606af6bdae"
    )
    jwt_signature: str = os.getenv("JWT_SIGNATURE", jwt_local_signature)
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = os.environ["JWT_EXPIRE_MINUTES"]


class ApiSettings(BaseSettings):
    """Api settings."""

    api_version: str = os.getenv("API_VERSION", default="/api/v1")


class AppSettings(BaseSettings):
    """Application settings."""

    app_host: str = os.getenv("APP_HOST", default="0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", default="8888"))
    max_questions: int = int(os.getenv("MAX_QUESTIONS", default="10"))
    max_answers_per_question: int = int(
        os.getenv("MAX_ANSWERS_PER_QUESTION", default="5")
    )


class Config(BaseSettings):
    """Config base."""

    ENV: str = "local"
    DEBUG: bool = True
    APP_HOST: str = AppSettings().app_host
    APP_PORT: int = AppSettings().app_port
    MAX_QUESTIONS: int = AppSettings().max_questions
    MAX_ANSWERS_PER_QUESTION: int = AppSettings().max_answers_per_question
    TOKEN_INFO = TokenSettings()
    API_INFO = ApiSettings()

    # Local mongo db
    MONGODB_CONN_STR = os.getenv(
        "MONGO_CONN_STR",
        default="mongodb://myUserAdmin:abc123@127.0.0.1:27017/"
        "quizdb?authSource=admin",
    )

    # Cloud mongo db
    # MONGODB_CONN_STR = os.getenv(
    #     'MONGO_CONN_STR',
    #     default="mongodb+srv://user:key@cluster0.z338glp.mongodb.net
    #     /?retryWrites=true&w=majority")


class LocalConfig(Config):
    """Local config."""


class DevelopmentConfig(Config):
    """Development config."""


class StageConfig(Config):
    """Stage config."""


class QualityControlConfig(Config):
    """QA config."""


class ProductionConfig(Config):
    """Production config."""

    DEBUG: str = False


config_factory = {
    "local": LocalConfig(),
    "dev": DevelopmentConfig(),
    "stage": StageConfig(),
    "qa": QualityControlConfig(),
    "prod": ProductionConfig(),
}


@lru_cache
def get_config() -> Config:
    """Gets config and caches it."""

    env = os.getenv("ENV", "local")
    return config_factory[env]
