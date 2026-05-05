# passenger_router.py
from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role
from Controllers.passenger_controller import PassengerViewController

router = APIRouter(
    tags=["Passenger"],
    dependencies=[Depends(verify_role("passenger"))]
)

@router.get("/dashboard")
async def passenger_dashboard():
    return await PassengerViewController.dashboard()

@router.get("/announcements")
async def view_announcements():
    return await PassengerViewController.view_announcements()

@router.get("/lost-found")
async def view_lost_found():
    return await PassengerViewController.view_lost_found()