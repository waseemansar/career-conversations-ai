class AppError(Exception):
    def __init__(self, message: str, code: str = "APP_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ExternalServiceError(AppError):
    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        code: str = "EXTERNAL_SERVICE_ERROR",
        status_code: int = 503,
    ):
        super().__init__(message, code=code, status_code=status_code)


class OpenAIError(ExternalServiceError):
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(message, code="OPENAI_ERROR", status_code=503)


class QdrantError(ExternalServiceError):
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(message, code="QDRANT_ERROR", status_code=503)


class RedisError(ExternalServiceError):
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(message, code="REDIS_ERROR", status_code=503)


class NotificationError(ExternalServiceError):
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(message, code="NOTIFICATION_ERROR", status_code=502)


class ValidationError(AppError):
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, code="VALIDATION_ERROR", status_code=400)
