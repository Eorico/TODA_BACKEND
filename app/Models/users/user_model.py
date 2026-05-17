from beanie import Document
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

"""
    Roles Allowed: 
    admin
    driver
    passenger
"""

class User(Document):
    full_name: str
    email: EmailStr
    password: str
    role: str
    
    contact_number: Optional[str] = None
    address: Optional[str] = None
    body_number: Optional[str] = None
    
    license_url: Optional[str] = None
    orcr_url: Optional[str] = None  
    
    is_active: bool = True
    reset_token: Optional[str] = None
    
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "users"
        use_revision = False
        
    def model_dump(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)