from beanie import Document, Link
from datetime import datetime
from typing import Optional
from Models.user_model import User

class RiderProfile(Document):
    user: Link[User]
    first_name: str
    last_name: str
    address: str 
    contact_number: int
    
    license_pic: Optional[str] = None
    tricycle_body_number: str
    
    member_status: str = "pending" # pending or approve
    account_status: str = "inactive" # inactive or active
    
    last_contribution: float = 0.0
    
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "rider_profiles"