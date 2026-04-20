from beanie import Document
from datetime import datetime, timezone
from typing import Optional
from pydantic import Field

class Officer(Document):

    fname: str
    mi: Optional[str] = ""
    lname: str
    role: str           # President, Vice President, etc.
    status: str         # on-duty, in-office, off-duty
    phone: str
    email: str
    custom_id: str      # This stores your 'TODA-001' format
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "officers"