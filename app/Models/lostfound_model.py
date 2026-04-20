from beanie import Document
from datetime import datetime, timezone
from typing import Optional
from pydantic import Field

class LostFound(Document):

    name: str
    body: str
    date: str         
    status: str = "Pending"
    image: Optional[str] = None  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "lost_found"