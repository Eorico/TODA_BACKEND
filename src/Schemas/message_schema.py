from pydantic import BaseModel, Field

class MessageSchema(BaseModel):
    room_id: str
    message: str = Field(..., min_length=1)