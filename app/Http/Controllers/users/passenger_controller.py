# app/Http/Controllers/PassengerController.py
from app.Services.users.passenger_service import PassengerService

class PassengerController:
    def __init__(self, service: PassengerService):
        self._service = service

    async def profile(self, user):             return await self._service.get_profile(user)
    async def update_profile(self, user, data): return await self._service.update_profile(user, data)
    async def announcements(self):             return await self._service.get_announcements()
    async def lost_found(self):                return await self._service.get_lost_found()
    async def officers(self):                  return await self._service.get_officers()
    async def fare(self):                      return await self._service.get_fare()
    async def coding(self):                    return await self._service.get_coding()