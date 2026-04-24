from beanie import Document
from datetime import datetime, timezone
from typing import Optional
from pydantic import Field

class Officer(Document):

    full_name: Optional[str] = None
    mi: Optional[str] = ""
    last_name: Optional[str] = None
    role: str           # President, Vice President, etc.
    status: str         # on-duty, in-office, off-duty
    phone: str
    email: str
    custom_id: str      # This stores your 'TODA-001' format
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "officers"