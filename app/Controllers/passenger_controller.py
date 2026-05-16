# app/Controllers/passenger_controller.py
from app.Models.announcement_model import Announcement
from app.Models.lostfound_model import LostFound
from app.Models.passenger_profile_model import PassengerProfile
from app.Models.officer_model import Officer
from app.Models.fare_matrix_model import Fare
from app.Models.coding_model import CodingSchedule
from app.Models.user_model import User
from app.Utils.serializer import serialize
from fastapi import HTTPException

class PassengerViewController:

    @staticmethod
    async def dashboard() -> dict:
        return {"message": "Welcome Passenger"}

    @staticmethod
    async def view_announcements() -> list:
        items = await Announcement.find_all().sort("-created_at").to_list()
        return [serialize(i) for i in items]

    @staticmethod
    async def view_lost_found() -> list:
        items = await LostFound.find_all().to_list()
        return [serialize(i) for i in items]

    @staticmethod
    async def view_officers() -> list:
        items = await Officer.find_all().to_list()
        return [serialize(i) for i in items]

    @staticmethod
    async def view_fare() -> list:
        items = await Fare.find_all().to_list()
        return [serialize(i) for i in items]

    @staticmethod
    async def view_coding() -> list:
        items = await CodingSchedule.find_all().to_list()
        return [serialize(i) for i in items]

    @staticmethod
    async def get_profile(user: dict) -> dict:
        email = user.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Token missing email.")

        profile = await PassengerProfile.find_one(
            PassengerProfile.email == email,
            fetch_links=False
        )
        if not profile:
            db_user = await User.find_one(User.email == email, fetch_links=False)
            profile = PassengerProfile(
                full_name=db_user.full_name if db_user else email.split('@')[0],
                contact=db_user.contact_number if db_user else None,
                email=email,
                address=db_user.address if db_user else None,   
            )
            await profile.insert()

        return {
            "id":         str(profile.id),
            "full_name":  profile.full_name,
            "contact":    profile.contact,
            "email":      profile.email,
            "address":    profile.address,
            "created_at": profile.created_at.isoformat(),
        }
        
    @staticmethod
    async def update_profile(user: dict, data: dict) -> dict:
        email = user.get("email")
        profile = await PassengerProfile.find_one(
            PassengerProfile.email == email,
            fetch_links=False
        )
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        for k, v in data.items():
            if v is not None:
                setattr(profile, k, v)
        await profile.save()
        return {"message": "Profile updated"}