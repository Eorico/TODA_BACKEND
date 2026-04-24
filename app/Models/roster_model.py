from beanie import Document
from datetime import datetime, timezone
from pydantic import Field
from typing import Optional

class MemberRoster(Document):
    full_name: str
    body_number: str = "—"            
    status: str          
    contrib: str      
    date: str 
    email: str = "—"
    contact: str = "—"
    license_url: Optional[str] = None
    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "member_roster"