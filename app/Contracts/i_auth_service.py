# app/Contracts/IAuthService.py
from abc import ABC, abstractmethod

class IAuthService(ABC):

    @abstractmethod
    async def register(self, data, extra: dict) -> dict: ...

    @abstractmethod
    async def login(self, data) -> dict: ...

    @abstractmethod
    async def forgot_password(self, data) -> dict: ...

    @abstractmethod
    async def verify_code(self, data) -> dict: ...

    @abstractmethod
    async def reset_password(self, data) -> dict: ...