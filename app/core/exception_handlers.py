from typing import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.exceptions import (
    AppError,
    ExternalServiceError,
    NotificationError,
    OpenAIError,
    QdrantError,
    RedisError,
    ValidationError,
)


def create_exception_handler() -> Callable[[Request, AppError], JSONResponse]:

    async def exception_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "code": exc.code,
                }
            },
        )

    return exception_handler


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"{request.method} {request.url} : {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}
        },
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    first_error = errors[0] if errors else {}
    field = first_error.get("loc", ["unknown"])[-1]

    logger.warning(f"{request.method} {request.url} : {str(exc)}")

    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "message": f"Invalid or missing field: '{field}'",
                "code": "VALIDATION_ERROR",
            }
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(ExternalServiceError, create_exception_handler())
    app.add_exception_handler(OpenAIError, create_exception_handler())
    app.add_exception_handler(QdrantError, create_exception_handler())
    app.add_exception_handler(RedisError, create_exception_handler())
    app.add_exception_handler(NotificationError, create_exception_handler())
    app.add_exception_handler(ValidationError, create_exception_handler())
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)
