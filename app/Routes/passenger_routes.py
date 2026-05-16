# app/Routes/passenger_routes.py
from fastapi import APIRouter, Depends, Body
from app.Middleware.role_base_access import verify_role
from app.Controllers.passenger_controller import PassengerViewController

# ── Public routes — no auth required ─────────────────────────────
public_router = APIRouter(tags=["Passenger"])

@public_router.get("/announcements")
async def view_announcements():
    return await PassengerViewController.view_announcements()

@public_router.get("/lost-found")
async def view_lost_found():
    return await PassengerViewController.view_lost_found()

@public_router.get("/officers")
async def view_officers():
    return await PassengerViewController.view_officers()

@public_router.get("/fare")
async def view_fare():
    return await PassengerViewController.view_fare()

@public_router.get("/coding")
async def view_coding():
    return await PassengerViewController.view_coding()

# ── Protected routes — passenger token required ───────────────────
router = APIRouter(
    tags=["Passenger"],
    dependencies=[Depends(verify_role("passenger"))]
)

@router.get("/dashboard")
async def passenger_dashboard():
    return await PassengerViewController.dashboard()

@router.get("/profile")
async def get_profile(user: dict = Depends(verify_role("passenger"))):
    return await PassengerViewController.get_profile(user)

@router.put("/profile")
async def update_profile(
    user: dict = Depends(verify_role("passenger")),
    data: dict = Body(...)
):
    return await PassengerViewController.update_profile(user, data)