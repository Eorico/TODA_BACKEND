from beanie import Document, Link
from datetime import datetime, timezone
from typing import Optional
from Models.user_model import User
from pydantic import Field

class RiderProfile(Document):
    full_name: str
    last_name: str = ""
    body_number: str = "---"
    contact: str
    status: str = "Active"
    
    email: Optional[str] = None  
        
    license_url: Optional[str] = None 
    orcr_url: Optional[str] = None
    
    address: Optional[str] = "Not Specified"
    user: Optional[Link[User]] = None
    member_status: str = "approved"
    last_contribution: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "driver_profiles"