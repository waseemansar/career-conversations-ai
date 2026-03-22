# schemas/error_schema.py
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    message: str
    code: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


class ValidationErrorResponse(ErrorResponse):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": {
                        "message": "Invalid or missing field: 'message'",
                        "code": "VALIDATION_ERROR",
                    }
                }
            ]
        }
    }


class InternalErrorResponse(ErrorResponse):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": {
                        "message": "Internal server error",
                        "code": "INTERNAL_ERROR",
                    }
                }
            ]
        }
    }


class ServiceUnavailableResponse(ErrorResponse):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": {
                        "message": "Service temporarily unavailable",
                        "code": "QDRANT_ERROR",
                    }
                }
            ]
        }
    }
