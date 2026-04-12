from pydantic import BaseModel, Field
from typing import Optional 
from pydantic import BaseModel

class RiderProfileCreateSchema(BaseModel):
    address: str = Field(..., min_length=5)
    license_pic: Optional[str] = None 
    tricycle_body_number: str = Field(..., min_length=1)