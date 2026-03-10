from fastapi import APIRouter
from Schemas.user_schema import SignUpSchema, LoginSchema, ForgotPasswordSchema
from Controllers.auth_controller import *

router = APIRouter()

@router.post("/signup")
async def signup_route(data: SignUpSchema):
    return await signup_controller(data)
@router.post("/login")
async def login_controller(data: LoginSchema):
    return await login_controller(data)
@router.post("/forgot-password")
async def forgot_password_controller(data: ForgotPasswordSchema):
    return await forgot_controller(data)