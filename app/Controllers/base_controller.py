from fastapi import HTTPException
from Utils.serializer import serialize

class BaseController:
    model = None
    
    @classmethod
    async def get_or_404(cls, id: str):
        item = await cls.model.get(id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{cls.model.__name__} not found")
        return item
    
    @classmethod
    async def get_all(cls) -> list:
        items = await cls.model.find_all(fetch_links=True).to_list()
        return [serialize(i) for i in items]
    
    @classmethod
    async def delete_by_id(cls, id: str) -> dict:
        item = await cls.get_or_404(id)
        await item.delete()
        return {"message": f"{cls.model.__name__} deleted"}