from beanie import Document
from datetime import datetime, timezone
from pydantic import Field

class MemberRoster(Document):
    name: str
    id: str            
    status: str          
    contrib: str      
    date: str         
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "member_roster"