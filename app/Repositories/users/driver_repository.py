# app/Repositories/DriverRepository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.users.driver_profile_model import DriverProfile
from app.Models.admin.roster_model import MemberRoster

class DriverRepository(BaseRepository):
    """Single Responsibility: DriverProfile data access only."""
    model = DriverProfile

    async def find_by_email(self, email: str) -> DriverProfile | None:
        return await DriverProfile.find_one(
            DriverProfile.email == email, fetch_links=False
        )

    async def find_all_serialized(self) -> list:
        return await self.find_all()

    async def create_profile(self, data: dict) -> DriverProfile:
        return await self.create(data)

    async def find_roster_by_email(self, email: str) -> MemberRoster | None:
        return await MemberRoster.find_one(
            MemberRoster.email == email, fetch_links=False
        )

    async def create_roster(self, data: dict) -> MemberRoster:
        entry = MemberRoster(**data)
        await entry.insert()
        return entry

    async def delete_roster_by_email(self, email: str) -> None:
        entry = await self.find_roster_by_email(email)
        if entry:
            await entry.delete()