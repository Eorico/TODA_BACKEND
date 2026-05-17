# app/Repositories/PassengerRepository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.users.passenger_profile_model import PassengerProfile

class PassengerRepository(BaseRepository):
    """Single Responsibility: PassengerProfile data access only."""
    model = PassengerProfile

    async def find_by_email(self, email: str) -> PassengerProfile | None:
        return await PassengerProfile.find_one(
            PassengerProfile.email == email, fetch_links=False
        )

    async def create_profile(self, data: dict) -> PassengerProfile:
        return await self.create(data)