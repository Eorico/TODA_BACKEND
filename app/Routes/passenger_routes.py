from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role
from Models.announcement_model import Announcement
from Models.lostfound_model import LostFound
router = APIRouter(
    prefix="/passenger",
    tags=["Passenger"],
    dependencies=[Depends(verify_role("passenger"))]
)

@router.get("/dashboard")
async def passenger_dashboard():
    return {"message": "Welcome Passenger"}

@router.get("/announcements")
async def view_announcements():
    return await Announcement.find_all().to_list()

@router.get("/lost-found")
async def view_lost_found():
    return await LostFound.find_all().to_list()