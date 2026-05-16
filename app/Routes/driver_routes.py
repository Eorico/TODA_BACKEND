# app/Routes/driver_routes.py  ← THIS is the file main.py uses
from fastapi import APIRouter, Depends
from app.Middleware.role_base_access import verify_role
from app.Schemas.driver_schema import RiderProfileCreateSchema
from app.Controllers.driver_controller import RiderViewController
from app.Controllers.admin_controller import (
    OfficerController, FareController, CodingController, ViolationController
)

router = APIRouter(
    tags=["Driver"],
    dependencies=[Depends(verify_role("driver"))]
)

@router.get("/dashboard")
async def rider_dashboard():
    return await RiderViewController.dashboard()

@router.post("/profile")
async def submit_profile(data: RiderProfileCreateSchema, user=Depends(verify_role("driver"))):
    return await RiderViewController.submit_profile(user, data)

@router.get("/profile")
async def view_profile(user: dict = Depends(verify_role("driver"))):
    return await RiderViewController.view_profile(user)

@router.get("/funds")
async def view_funds(user=Depends(verify_role("driver"))):
    return await RiderViewController.view_funds(user)

@router.get("/lost-found")
async def view_lost_found():
    return await RiderViewController.view_lost_found()

@router.get("/announcements")
async def view_announcements(user=Depends(verify_role("driver"))):
    return await RiderViewController.view_announcements(user)

@router.get("/officers")
async def get_officers():
    return await OfficerController.get_all()

@router.get("/fare")
async def get_fare():
    return await FareController.get_all()

@router.get("/coding")
async def get_coding():
    return await CodingController.get_all()

@router.get("/violations")
async def get_all_violations():
    return await ViolationController.get_all()

@router.get("/my-violations")
async def get_my_violations(user=Depends(verify_role("driver"))):
    return await RiderViewController.view_my_violations(user)