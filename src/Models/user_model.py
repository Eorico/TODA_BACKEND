from beanie import Document
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

"""
    Roles Allowed: 
    admin
    rider
    passenger
"""

class User(Document):
    name: str
    email: EmailStr
    password: str
    role: str
    is_active: bool = True
    reset_token: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "users"