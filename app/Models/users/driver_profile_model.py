from beanie import Document
from datetime import datetime, timezone
from typing import Optional
from pydantic import Field

class DriverProfile(Document):
    full_name: str
    last_name: str = ""
    body_number: str = "---"
    contact: str
    status: str = "Active"
    
    email: Optional[str] = None  
    
    expiration_date_license: Optional [str] = None
    expiration_date_orcr: Optional [str] = None
        
    license_url: Optional[str] = None 
    orcr_url: Optional[str] = None
    
    address: Optional[str] = "Not Specified"
 
    member_status: str = "approved"
    last_contribution: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "driver_profiles"