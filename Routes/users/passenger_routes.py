# Routes/passenger.py
from fastapi import APIRouter, Depends, Body
from app.Providers.app_service_provider import passenger_controller
from app.Http.Middleware.auth_middleware import verify_role

public_router = APIRouter(tags=["Passenger"])
router        = APIRouter(tags=["Passenger"], dependencies=[Depends(verify_role("passenger"))])

# Public
@public_router.get("/announcements")
async def announcements(): return await passenger_controller.announcements()

@public_router.get("/lost-found")
async def lost_found():    return await passenger_controller.lost_found()

@public_router.get("/officers")
async def officers():      return await passenger_controller.officers()

@public_router.get("/fare")
async def fare():          return await passenger_controller.fare()

@public_router.get("/coding")
async def coding():        return await passenger_controller.coding()

# Protected
@router.get("/profile")
async def profile(user=Depends(verify_role("passenger"))):
    return await passenger_controller.profile(user)

@router.put("/profile")
async def update_profile(
    user=Depends(verify_role("passenger")),
    data: dict = Body(...),
):
    return await passenger_controller.update_profile(user, data)