from pydantic import BaseModel, EmailStr

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