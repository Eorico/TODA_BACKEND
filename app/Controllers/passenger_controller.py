# Controllers/passenger_controller.py
from Models.announcement_model import Announcement
from Models.lostfound_model import LostFound

class PassengerViewController:

    @staticmethod
    async def dashboard() -> dict:
        return {"message": "Welcome Passenger"}

    @staticmethod
    async def view_announcements() -> list:
        return await Announcement.find_all().to_list()

    @staticmethod
    async def view_lost_found() -> list:
        return await LostFound.find_all().to_list()