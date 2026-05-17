# app/Http/Controllers/DriverController.py
from app.Services.users.driver_service import DriverService

class DriverController:
    def __init__(self, service: DriverService):
        self._service = service

    async def profile(self, user):        return await self._service.get_profile(user)
    async def funds(self, user):          return await self._service.get_funds(user)
    async def my_violations(self, user):  return await self._service.get_my_violations(user)
    async def announcements(self):        return await self._service.get_announcements()
    async def lost_found(self):           return await self._service.get_lost_found()
    async def officers(self):             return await self._service.get_officers()
    async def fare(self):                 return await self._service.get_fare()
    async def coding(self):               return await self._service.get_coding()
    async def violations(self):           return await self._service.get_violations()