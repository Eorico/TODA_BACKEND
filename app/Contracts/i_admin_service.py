# app/Contracts/IAdminService.py
from abc import ABC, abstractmethod

class IAdminService(ABC):

    @abstractmethod
    async def approve_driver(self, id: str) -> dict: ...

    @abstractmethod
    async def reject_driver(self, id: str) -> dict: ...

    @abstractmethod
    async def delete_driver(self, id: str) -> dict: ...