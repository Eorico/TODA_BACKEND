from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role
from backend.src.Schemas.rider_schema import RiderProfileCreateSchema
from Models.lostfound_model import LostFound
from Services.rider_profile_service import (
    create_rider_profile, get_rider_profile, 
    get_rider_funds, is_rider_approved
)
from Models.announcement_model import Announcement

router = APIRouter(
    prefix="/rider",
    tags=["Rider"],
    dependencies=[Depends(verify_role("rider"))]
)

@router.get("/dashboard")
async def rider_dashboard():
    return {"message": "Welcome Rider"}

@router.post("/profile")
async def submit_profile(data: RiderProfileCreateSchema, user=Depends(verify_role("rider"))):
    return await create_rider_profile(user, data)

@router.get("/profile")
async def view_profile(user=Depends()):
    return await get_rider_profile(user)

@router.get("/funds")
async def view_funds(user=Depends()):
    return await get_rider_funds(user)

@router.get("/lost-found")
async def view_lost_found():
    return await LostFound.find_all().to_list()

@router.get("/announcements")
async def view_announcements(user=Depends()):
    if not await is_rider_approved(user):
        return {"message": "Profile not approved yet"}
    
    announcements = await Announcement.find_all().sort("-created_at").to_list()
    return announcements