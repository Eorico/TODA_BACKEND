# app/Contracts/IRepository.py
from abc import ABC, abstractmethod

class IRepository(ABC):
    """
    Interface Segregation + Dependency Inversion:
    all repositories depend on this abstraction.
    """

    @abstractmethod
    async def find_all(self) -> list: ...

    @abstractmethod
    async def find_by_id(self, id: str): ...

    @abstractmethod
    async def create(self, data: dict): ...

    @abstractmethod
    async def update(self, id: str, data: dict): ...

    @abstractmethod
    async def delete(self, id: str) -> dict: ...