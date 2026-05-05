# Routes/auth_driver_routes.py
from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Request
from typing import Optional
from Schemas.auth_schema import SignUpSchema, LoginSchema
from Services.auth_service import AuthService
from Middleware.rate_limiter import limiter

router = APIRouter(prefix="/driver", tags=["Auth - Driver"])

@router.post("/register")
@limiter.limit("3/minute")
async def signup(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    contact_number: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    body_number: Optional[str] = Form(None),
    license_file: Optional[UploadFile] = File(None),
    orcr_file: Optional[UploadFile] = File(None),
):
    try:
        signup_data = SignUpSchema(
            full_name=full_name,
            email=email,
            password=password,
            role="driver",  
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    extra_data = {
        "contact_number": contact_number,
        "address": address,
        "body_number": body_number,
        "license_url": license_file,
        "orcr_url": orcr_file,
    }

    return await AuthService.signup(signup_data, extra_data)


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginSchema):
    data.role = "driver"
    return await AuthService.login(data)