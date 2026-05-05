from pydantic import BaseModel
from typing import Optional 
from pydantic import BaseModel

class RiderProfileCreateSchema(BaseModel):
    full_name: str
    last_name: str = ""
    body_number: str = "---"
    contact: str
    email: Optional[str] = None    
    license_url: Optional[str] = None
    orcr_url: Optional[str] = None
    address: Optional[str] = "Not Specified"
    status: Optional[str] = "Active"