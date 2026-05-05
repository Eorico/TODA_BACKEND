from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role
from Schemas.driver_schema import RiderProfileCreateSchema
from Controllers.driver_controller import RiderViewController

router = APIRouter(
    tags=["Rider"],
    dependencies=[Depends(verify_role("driver"))]
)

@router.get("/dashboard")
async def rider_dashboard():
    return await RiderViewController.dashboard()

@router.post("/profile")
async def submit_profile(data: RiderProfileCreateSchema, user=Depends(verify_role("rider"))):
    return await RiderViewController.submit_profile(user, data)

@router.get("/profile")
async def view_profile(user=Depends(verify_role("rider"))):
    return await RiderViewController.view_profile(user)

@router.get("/funds")
async def view_funds(user=Depends(verify_role("rider"))):
    return await RiderViewController.view_funds(user)

@router.get("/lost-found")
async def view_lost_found():
    return await RiderViewController.view_lost_found()

@router.get("/announcements")
async def view_announcements(user=Depends(verify_role("rider"))):
    return await RiderViewController.view_announcements(user)