# app/Http/Middleware/AuthMiddleware.py
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.Utils.jwt_handler import JwtHandler
from app.Exceptions.app_exception import ForbiddenException

_bearer = HTTPBearer()

def verify_role(required_role: str):
    """
    Dependency Inversion: routes depend on this abstraction,
    not on raw JWT logic.
    """
    async def _guard(
        credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    ) -> dict:
        payload = JwtHandler.decode(credentials.credentials)
        if payload.get("role") != required_role:
            raise ForbiddenException(
                f"This endpoint requires role: {required_role}."
            )
        return payload
    return _guard