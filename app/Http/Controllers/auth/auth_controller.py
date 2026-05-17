# app/Http/Controllers/AuthController.py
from app.Services.auth.auth_service import AuthService

class AuthController:
    """Single Responsibility: delegate HTTP requests to AuthService."""

    def __init__(self, service: AuthService):
        self._service = service

    async def register(self, data, extra: dict) -> dict:
        return await self._service.register(data, extra)

    async def login(self, data) -> dict:
        return await self._service.login(data)

    async def forgot_password(self, data) -> dict:
        return await self._service.forgot_password(data)

    async def verify_code(self, data) -> dict:
        return await self._service.verify_code(data)

    async def reset_password(self, data) -> dict:
        return await self._service.reset_password(data)