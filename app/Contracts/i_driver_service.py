# app/Contracts/IDriverService.py
from abc import ABC, abstractmethod

class IDriverService(ABC):

    @abstractmethod
    async def get_profile(self, user: dict) -> dict: ...

    @abstractmethod
    async def get_funds(self, user: dict) -> dict: ...

    @abstractmethod
    async def get_my_violations(self, user: dict) -> list: ...