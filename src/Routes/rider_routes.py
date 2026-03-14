from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role
from Schemas.user_schema import RiderProfileCreateSchema
from Services.rider_profile_service import (
    create_rider_profile, get_rider_profile, 
    get_rider_funds, is_rider_approved
)
from Models.announcement_model import Announcement

router = APIRouter(
    prefix="/rider",
    tags=["Rider"],
    dependencies=[Depends(verify_role["rider"])]
)

@router.get("/rider-dashboard")
async def rider_dashboard(user=Depends(verify_role("rider"))):
    return {"message": "Welcome Rider"}

@router.post("/rider-profile")
async def submit_profile(data: RiderProfileCreateSchema, user=Depends()):
    return await create_rider_profile(user, data)

@router.get("/rider-profile")
async def view_profile(user=Depends()):
    return await get_rider_profile(user)

@router.get("/funds")
async def view_funds(user=Depends()):
    return await get_rider_funds(user)

@router.get("/announcements")
async def view_announcements(user=Depends()):
    if not await is_rider_approved(user):
        return {"message": "Profile not approved yet"}
    
    announcements = await Announcement.find_all().sort("-created_at").to_list()
    return announcements