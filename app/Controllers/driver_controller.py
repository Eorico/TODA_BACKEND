from app.Models.lostfound_model import LostFound
from app.Models.announcement_model import Announcement
from app.Models.violation_model import Violation
from app.Services.driver_service import RiderService
from app.Utils.serializer import serialize


class RiderViewController:

    @staticmethod
    async def dashboard() -> dict:
        return {"message": "Welcome Rider"}

    @staticmethod
    async def submit_profile(user, data) -> dict:
        return await RiderService.create(user, data)

    @staticmethod
    async def view_profile(user: dict):
        return await RiderService.get_profile(user)

    @staticmethod
    async def view_funds(user) -> dict:
        return await RiderService.get_funds(user)

    @staticmethod
    async def view_lost_found() -> list:
        items = await LostFound.find_all().to_list()
        return [serialize(i) for i in items]

    @staticmethod
    async def view_announcements(user) -> list:
        items = await Announcement.find_all().sort("-created_at").to_list()
        return [serialize(i) for i in items]

    @staticmethod
    async def view_my_violations(user: dict) -> list:
        """Returns violations that belong to the logged-in driver."""
        profile = await RiderService.get_profile(user)
        driver_id = profile.get("id")
        full_name = f"{profile.get('full_name', '')} {profile.get('last_name', '')}".strip()

        all_violations = await Violation.find_all().to_list()
        mine = [
            v for v in all_violations
            if v.driver_id == driver_id
            or v.driver_name.strip().lower() == full_name.lower()
        ]
        return [serialize(v) for v in mine]