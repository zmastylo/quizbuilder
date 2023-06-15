"""Server module."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api import router
from core.exception import CustomError


def init(the_app: FastAPI) -> None:
    """Initialize resources."""

    the_app.include_router(router=router)

    @the_app.exception_handler(CustomError)
    async def custom_exception_handler(request: Request, exc: CustomError):
        """Custom exception handler."""

        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomError):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def create_app() -> FastAPI:
    """Create application."""

    the_app = FastAPI(
        description="Quiz builder API",
        version="1.0.0",
    )

    init(the_app)
    return the_app


app = create_app()
