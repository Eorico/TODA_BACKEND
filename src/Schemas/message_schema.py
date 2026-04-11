from pydantic import BaseModel

class MessageSchema(BaseModel):
    room_id: str
    message: str 