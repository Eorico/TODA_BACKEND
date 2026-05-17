# Routes/driver.py
from fastapi import APIRouter, Depends
from app.Providers.app_service_provider import driver_controller
from app.Http.Middleware.auth_middleware import verify_role

router = APIRouter(tags=["Driver"], dependencies=[Depends(verify_role("driver"))])

@router.get("/profile")
async def profile(user=Depends(verify_role("driver"))):
    return await driver_controller.profile(user)

@router.get("/funds")
async def funds(user=Depends(verify_role("driver"))):
    return await driver_controller.funds(user)

@router.get("/my-violations")
async def my_violations(user=Depends(verify_role("driver"))):
    return await driver_controller.my_violations(user)

@router.get("/announcements")
async def announcements(): return await driver_controller.announcements()

@router.get("/lost-found")
async def lost_found():    return await driver_controller.lost_found()

@router.get("/officers")
async def officers():      return await driver_controller.officers()

@router.get("/fare")
async def fare():          return await driver_controller.fare()

@router.get("/coding")
async def coding():        return await driver_controller.coding()

@router.get("/violations")
async def violations():    return await driver_controller.violations()