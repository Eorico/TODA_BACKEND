from beanie import Document, Link
from datetime import datetime, timezone
from typing import Optional
from Models.user_model import User
from pydantic import Field

class RiderProfile(Document):
    # Field names now match your JS payload keys
    fname: str
    lname: str
    body: str
    contact: str
    status: str = "Active"
    
    # Keeping your original logic but making it compatible
    address: Optional[str] = "Not Specified"
    user: Optional[Link[User]] = None
    member_status: str = "approved"
    last_contribution: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "rider_profiles"