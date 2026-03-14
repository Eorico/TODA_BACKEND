from pydantic import BaseModel, EmailStr
from typing import Optional

"""
    SCHEMA CONNECTION TO DATABASE
"""

class SignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    
class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class RiderProfileCreateSchema(BaseModel):
    address: str
    license_pic: Optional[str] = None 
    tricycle_body_number: str