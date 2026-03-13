from src.Models.user_model import User
from src.Utils.password import hash_password, verify_password
from src.Utils.jwt_handler import create_token
from fastapi import HTTPException
import secrets

async def signup(data):
    
    existing_user =  await User.find_one(User.email == data.email)

    if  existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role
    )

    await user.insert()

    return {"messange": "User created successfully"}


async def login(data):
    user = await User.find_one(User.email == data.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")
    
    token = create_token({
        "user_id": str(user.id),
        "role": user.role

    })

    return {
        "access_token": token,
        "role": user.role
    }
    
async def forgot_password(data):
    
    user = await User.find_one(User.email == data.email)
    
    if not user: 
        raise HTTPException(status_code=404, detail="Email not found")
    
    token = secrets.token_hex(16)
    
    user.reset_token = token
    
    await user.save()
    
    return {
        "message": "Password reset token generated",
        "reset_token": token
    }