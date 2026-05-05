# Routes/auth_shared_routes.py
from fastapi import APIRouter, Request
from Schemas.auth_schema import ForgotPasswordSchema, VerifyCodeSchema, ResetPasswordSchema
from Services.auth_service import AuthService
from Middleware.rate_limiter import limiter

router = APIRouter(tags=["Auth - Shared"])

@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password(request: Request, data: ForgotPasswordSchema):
    return await AuthService.forgot_password(data)

@router.post("/verify-code")
@limiter.limit("3/minute")
async def verify_code(request: Request, data: VerifyCodeSchema):
    return await AuthService.verify_code(data)

@router.post("/reset-password")
@limiter.limit("3/minute")
async def reset_password(request: Request, data: ResetPasswordSchema):
    return await AuthService.reset_password(data)