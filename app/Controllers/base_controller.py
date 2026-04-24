from fastapi import HTTPException

def serialize(doc) -> dict:
    data = {}
    for key, value in doc.model_dump().items():
        if isinstance(value, dict) and '$ref' in str(value):
            # Skip unresolved link references
            continue
        data[key] = value
    
    # Handle the user link separately — just store the ID string
    if hasattr(doc, 'user') and doc.user is not None:
        try:
            if hasattr(doc.user, 'id'):
                data['user_id'] = str(doc.user.id)
            else:
                data['user_id'] = str(doc.user.ref.id)
        except Exception:
            pass
        data.pop('user', None)  # remove the raw link object
    
    data['id'] = str(doc.id)
    return data

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