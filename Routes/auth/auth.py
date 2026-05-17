# Routes/auth.py
from fastapi import APIRouter, Form, File, UploadFile, Request
from typing import Optional
from app.Providers.app_service_provider import auth_controller
from app.Http.Middleware.rate_limiter import limiter
from app.Http.Requests.auth_request import (
    LoginRequest, ForgotPasswordRequest,
    VerifyCodeRequest, ResetPasswordRequest, RegisterRequest,
)
from fastapi import HTTPException

router = APIRouter(tags=["Auth"])

@router.post("/driver/register")
@limiter.limit("3/minute")
async def driver_register(
    request:                 Request,
    full_name:               str           = Form(...),
    email:                   str           = Form(...),
    password:                str           = Form(...),
    contact_number:          Optional[str] = Form(None),
    address:                 Optional[str] = Form(None),
    body_number:             Optional[str] = Form(None),
    expiration_date_license: Optional[str] = Form(None),
    expiration_date_orcr:    Optional[str] = Form(None),
    license_file:            Optional[UploadFile] = File(None),
    orcr_file:               Optional[UploadFile] = File(None),
):
    try:
        data = RegisterRequest(
            full_name=full_name, email=email,
            password=password,   role="driver",
        )
    except Exception as e:
        raise HTTPException(422, str(e))

    return await auth_controller.register(data, {
        "contact_number":          contact_number,
        "address":                 address,
        "body_number":             body_number,
        "expiration_date_license": expiration_date_license,
        "expiration_date_orcr":    expiration_date_orcr,
        "license_url":             license_file,
        "orcr_url":                orcr_file,
    })

@router.post("/driver/login")
@limiter.limit("5/minute")
async def driver_login(request: Request, data: LoginRequest):
    data.role = "driver"
    return await auth_controller.login(data)

@router.post("/passenger/register")
@limiter.limit("3/minute")
async def passenger_register(
    request:        Request,
    full_name:      str           = Form(...),
    email:          str           = Form(...),
    password:       str           = Form(...),
    contact_number: Optional[str] = Form(None),
    address:        Optional[str] = Form(None),
):
    try:
        data = RegisterRequest(
            full_name=full_name, email=email,
            password=password,   role="passenger",
        )
    except Exception as e:
        raise HTTPException(422, str(e))

    return await auth_controller.register(data, {
        "contact_number": contact_number,
        "address":        address,
    })

@router.post("/passenger/login")
@limiter.limit("5/minute")
async def passenger_login(request: Request, data: LoginRequest):
    data.role = "passenger"
    return await auth_controller.login(data)

@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password(request: Request, data: ForgotPasswordRequest):
    return await auth_controller.forgot_password(data)

@router.post("/verify-code")
@limiter.limit("3/minute")
async def verify_code(request: Request, data: VerifyCodeRequest):
    return await auth_controller.verify_code(data)

@router.post("/reset-password")
@limiter.limit("3/minute")
async def reset_password(request: Request, data: ResetPasswordRequest):
    return await auth_controller.reset_password(data)