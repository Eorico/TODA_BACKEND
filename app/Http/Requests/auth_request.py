# app/Http/Requests/AuthRequest.py
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional

class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=6, max_length=50)
    email:     EmailStr
    password:  str = Field(..., min_length=6)
    role:      Literal["admin", "driver", "passenger"]

class LoginRequest(BaseModel):
    email:       EmailStr
    password:    str
    role:        Optional[Literal["driver", "passenger"]] = None
    body_number: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code:  str

class ResetPasswordRequest(BaseModel):
    email:        EmailStr
    code:         str
    new_password: str