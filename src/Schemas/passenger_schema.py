from pydantic import BaseModel, Field
from typing import Optional

class PassengerProfileCreateSchema(BaseModel):
    contact_number: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5)