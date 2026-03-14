from beanie import Document
from datetime import datetime
from typing import optional
from Models.user_model import User

class RiderProfile(Document):
    user: Link[user]
    address: str 
    license_pic: optional[str] = None
    tricycle_body_number: str
    is_approved: bool = False 
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "rider_profile"