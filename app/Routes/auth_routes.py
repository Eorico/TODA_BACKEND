from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from typing import Optional
from Schemas.auth_schema import (
    SignUpSchema, LoginSchema, ForgotPasswordSchema,
    VerifyCodeSchema, ResetPasswordSchema
)
from Services.auth_service import AuthService

router = APIRouter(tags=["Auth"])

@router.post("/register")
async def signup(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    contact_number: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    body_number: Optional[str] = Form(None),
    license_file: Optional[UploadFile] = File(None) 
):
    # 3. Manually trigger Pydantic validation for the core fields
    try:
        signup_data = SignUpSchema(
            full_name=full_name, 
            email=email, 
            password=password, 
            role=role
        )
    except Exception as e:
        # This catches things like short passwords or invalid emails
        raise HTTPException(status_code=422, detail=str(e))

    extra_data = {
        "contact_number": contact_number,
        "address": address,
        "body_number": body_number,
        "license_url": license_file
    }

    return await AuthService.signup(signup_data, extra_data)

@router.post("/login")
async def login(data: LoginSchema):
    return await AuthService.login(data)

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema):
    return await AuthService.forgot_password(data)

@router.post("/verify-code")
async def verify_code(data: VerifyCodeSchema):
    return await AuthService.verify_code(data)

@router.post("/reset-password")
async def reset_password(data: ResetPasswordSchema):
    return await AuthService.reset_password(data)