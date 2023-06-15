"""Api module init file."""


from fastapi import APIRouter

from api.auth.router import auth_router
from api.home import home_router
from api.quiz.router import quiz_router
from api.user.router import user_router

router = APIRouter()

router.include_router(home_router)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(quiz_router)

__all__ = ["router"]
