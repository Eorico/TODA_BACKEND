# app/Models/passenger_profile_model.py
from beanie import Document
from typing import Optional
from datetime import datetime, timezone
from pydantic import Field

class PassengerProfile(Document):
    full_name: str
    contact: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = "Not Specified"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "passenger_profiles"