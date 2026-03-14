from beanie import Document, Link
from datetime import datetime
from typing import Optional
from Models.user_model import User

class RiderProfile(Document):
    user: Link[User]
    address: str 
    license_pic: Optional[str] = None
    tricycle_body_number: str
    is_approved: bool = False 
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "rider_profile"