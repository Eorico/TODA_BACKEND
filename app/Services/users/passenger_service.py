# app/Services/PassengerService.py
from app.Contracts.i_passenger_service import IPassengerService
from app.Repositories.users.passenger_repository import PassengerRepository
from app.Repositories.users.user_repository import UserRepository
from app.Repositories.admin.announcement_repository import AnnouncementRepository
from app.Repositories.admin.lost_and_found_repository import LostFoundRepository
from app.Repositories.admin.officer_repository import OfficerRepository
from app.Repositories.admin.fare_repository import FareRepository
from app.Repositories.admin.coding_repository import CodingRepository
from app.Exceptions.app_exception import UnauthorizedException, NotFoundException

class PassengerService(IPassengerService):

    def __init__(
        self,
        passenger_repo:    PassengerRepository,
        user_repo:         UserRepository,
        announcement_repo: AnnouncementRepository,
        lost_found_repo:   LostFoundRepository,
        officer_repo:      OfficerRepository,
        fare_repo:         FareRepository,
        coding_repo:       CodingRepository,
    ):
        self._passengers    = passenger_repo
        self._users         = user_repo
        self._announcements = announcement_repo
        self._lost_found    = lost_found_repo
        self._officers      = officer_repo
        self._fares         = fare_repo
        self._coding        = coding_repo

    async def get_profile(self, user: dict) -> dict:
        email = user.get("email")
        if not email:
            raise UnauthorizedException("Token missing email.")

        profile = await self._passengers.find_by_email(email)
        if not profile:
            db_user = await self._users.find_by_email(email)
            profile = await self._passengers.create_profile({
                "full_name": db_user.full_name if db_user else email.split("@")[0],
                "contact":   db_user.contact_number if db_user else None,
                "address":   db_user.address if db_user else None,
                "email":     email,
            })

        return {
            "id":         str(profile.id),
            "full_name":  profile.full_name,
            "contact":    profile.contact,
            "email":      profile.email,
            "address":    profile.address,
            "created_at": profile.created_at.isoformat(),
        }

    async def update_profile(self, user: dict, data: dict) -> dict:
        email   = user.get("email")
        profile = await self._passengers.find_by_email(email)
        if not profile:
            raise NotFoundException("Passenger profile")
        for key, value in data.items():
            if value is not None:
                setattr(profile, key, value)
        await profile.save()
        return {"message": "Profile updated."}

    async def get_announcements(self) -> list:
        return await self._announcements.find_all_sorted()

    async def get_lost_found(self) -> list:
        return await self._lost_found.find_all()

    async def get_officers(self) -> list:
        return await self._officers.find_all()

    async def get_fare(self) -> list:
        return await self._fares.find_all()

    async def get_coding(self) -> list:
        return await self._coding.find_all()