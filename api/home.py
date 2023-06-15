"""Home module, with no real functionality
but informational only."""

from fastapi import APIRouter

home_router = APIRouter(tags=["Home"])


@home_router.get("/")
async def get_introduction():
    """Basic info endpoint."""

    return {"Info": "Quiz builder app!"}
