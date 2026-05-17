# app/Exceptions/AppException.py
from fastapi import HTTPException

class AppException(HTTPException):
    """Base application exception — all custom exceptions extend this."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(404, f"{resource} not found.")

class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized."):
        super().__init__(401, detail)

class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden."):
        super().__init__(403, detail)

class ValidationException(AppException):
    def __init__(self, detail: str):
        super().__init__(422, detail)

class ConflictException(AppException):
    def __init__(self, detail: str):
        super().__init__(409, detail)