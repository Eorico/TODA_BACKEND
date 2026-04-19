from pydantic import BaseModel
from typing import Optional 
from pydantic import BaseModel

class RiderProfileCreateSchema(BaseModel):
    fname: str
    lname: str
    body: str
    contact: str
    status: str
    address: Optional[str] = "Not Specified"
    member_status: Optional[str] = "approved"