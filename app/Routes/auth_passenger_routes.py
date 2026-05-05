# Routes/auth_passenger_routes.py
from fastapi import APIRouter, Form, HTTPException, Request
from Schemas.auth_schema import SignUpSchema, LoginSchema
from Services.auth_service import AuthService
from Middleware.rate_limiter import limiter
from typing import Optional

router = APIRouter(prefix="/passenger", tags=["Auth - Passenger"])

@router.post("/register")
@limiter.limit("3/minute")
async def signup(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    contact_number: Optional[str] = Form(None)
):
    try:
        signup_data = SignUpSchema(
            full_name=full_name,
            email=email,
            password=password,
            role="passenger",
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    return await AuthService.signup(signup_data, extra_data={
        "contact_number": contact_number
    })


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginSchema):
    data.role = "passenger"
    return await AuthService.login(data)