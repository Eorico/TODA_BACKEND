# app/Contracts/IPassengerService.py
from abc import ABC, abstractmethod

class IPassengerService(ABC):

    @abstractmethod
    async def get_profile(self, user: dict) -> dict: ...

    @abstractmethod
    async def update_profile(self, user: dict, data: dict) -> dict: ...