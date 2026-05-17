from app.Contracts.i_repository import IRepository
from app.Exceptions.app_exception import NotFoundException
from app.Utils.serializer import Serializer

class BaseRepository(IRepository):
    """
    Open/Closed: open for extension (subclass adds methods),
    closed for modification (base logic doesn't change).
    """
    model = None

    async def find_all(self) -> list:
        # fetch_links=False prevents Beanie from making extra DB round trips
        # to resolve linked documents on every record in the list
        docs = await self.model.find_all(fetch_links=False).to_list()
        return Serializer.serialize_many(docs)

    async def find_by_id(self, id: str):
        doc = await self.model.get(id, fetch_links=False)
        if not doc:
            raise NotFoundException(self.model.__name__)
        return doc

    async def find_by_id_serialized(self, id: str) -> dict:
        return Serializer.serialize(await self.find_by_id(id))

    async def create(self, data: dict):
        instance = self.model(**data)
        await instance.insert()
        return instance

    async def update(self, id: str, data: dict):
        instance = await self.find_by_id(id)
        # exclude_unset equivalent — only write fields that are actually provided
        for key, value in data.items():
            if value is not None:
                setattr(instance, key, value)
        await instance.save()
        return instance

    async def delete(self, id: str) -> dict:
        instance = await self.find_by_id(id)
        await instance.delete()
        return {"message": f"{self.model.__name__} deleted successfully."}