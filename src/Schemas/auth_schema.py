from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class SignUpSchema(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Literal["admin", "rider", "passenger"]
    
class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class ForgotPasswordSchema(BaseModel):
    email: EmailStr
