from Models.lostfound_model import LostFound
from Models.announcement_model import Announcement
from Services.rider_profile_service import RiderProfileService

class RiderViewController:

    @staticmethod
    async def dashboard() -> dict:
        return {"message": "Welcome Rider"}

    @staticmethod
    async def submit_profile(user, data) -> dict:
        return await RiderProfileService.create(user, data)

    @staticmethod
    async def view_profile(user):
        return await RiderProfileService.get_profile(user)

    @staticmethod
    async def view_funds(user) -> dict:
        return await RiderProfileService.get_funds(user)

    @staticmethod
    async def view_lost_found() -> list:
        return await LostFound.find_all().to_list()

    @staticmethod
    async def view_announcements(user):
        if not await RiderProfileService.is_approved(user):
            return {"message": "Profile not approved yet"}
        return await Announcement.find_all().sort("-created_at").to_list()