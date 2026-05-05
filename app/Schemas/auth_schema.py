from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional

class SignUpSchema(BaseModel):
    full_name: str = Field(..., min_length=6, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Literal["admin", "driver", "passenger"]
    
class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    role: Optional[Literal["driver", "passenger"]] = None
    
class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class VerifyCodeSchema(BaseModel):
    email: EmailStr
    code: str
    
class ResetPasswordSchema(BaseModel):
    email: EmailStr
    code: str
    new_password: str