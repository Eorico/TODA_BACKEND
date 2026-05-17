from app.Services.admin.admin_service import AdminService
from app.Services.auth.auth_service import AuthService
from app.Exceptions.app_exception import ForbiddenException
from fastapi import UploadFile

class AdminController:
    def __init__(self, service: AdminService, auth_service: AuthService):
        self._service      = service
        self._auth_service = auth_service

    async def login(self, data) -> dict:
        result = await self._auth_service.login(data)
        if result.get("role") != "admin":
            raise ForbiddenException("Admin access only.")
        return {"access_token": result["access_token"]}

    # ── Drivers ───────────────────────────────────────────────────
    async def get_drivers(self):
        return await self._service.get_all_drivers()

    async def update_driver(self, id, data):
        return await self._service.update_driver(id, data.dict(exclude_unset=True))

    async def delete_driver(self, id):
        return await self._service.delete_driver(id)

    async def delete_driver_cascade(self, id: str):
        return await self._service.delete_driver_cascade(id)

    async def approve_driver(self, id):
        return await self._service.approve_driver(id)

    async def reject_driver(self, id):
        return await self._service.reject_driver(id)

    async def upload_license(self, id, file: UploadFile):
        return await self._service.upload_document(id, file, "license_url")

    async def upload_orcr(self, id, file: UploadFile):
        return await self._service.upload_document(id, file, "orcr_url")

    # ── Roster ────────────────────────────────────────────────────
    async def get_roster(self):
        return await self._service.get_roster()

    async def create_roster(self, data):
        return await self._service.create_roster(data.dict())

    async def update_roster(self, id, data):
        return await self._service.update_roster(id, data.dict(exclude_unset=True))

    async def delete_roster(self, id):
        return await self._service.delete_roster(id)

    async def delete_roster_by_email(self, email: str):
        return await self._service.delete_roster_by_email(email)

    # ── Contributions ─────────────────────────────────────────────
    async def get_contributions(self):
        return await self._service.get_contributions()

    async def create_contribution(self, data):
        return await self._service.create_contribution(data.dict())

    async def update_contribution(self, id, d):
        return await self._service.update_contribution(id, d.dict(exclude_unset=True))

    async def delete_contribution(self, id):
        return await self._service.delete_contribution(id)

    # ── Announcements ─────────────────────────────────────────────
    async def get_announcements(self):
        return await self._service.get_announcements()

    async def create_announcement(self, data):
        return await self._service.create_announcement(data.dict())

    async def update_announcement(self, id, d):
        return await self._service.update_announcement(id, d.dict(exclude_unset=True))

    async def delete_announcement(self, id):
        return await self._service.delete_announcement(id)

    # ── Lost & Found ──────────────────────────────────────────────
    async def get_lost_found(self):
        return await self._service.get_lost_found()

    async def create_lost_found(self, data):
        return await self._service.create_lost_found(data.dict())

    async def update_lost_found(self, id, d):
        return await self._service.update_lost_found(id, d.dict(exclude_unset=True))

    async def delete_lost_found(self, id):
        return await self._service.delete_lost_found(id)

    # ── Fare ──────────────────────────────────────────────────────
    async def get_fare(self):
        return await self._service.get_fare()

    async def create_fare(self, data):
        return await self._service.create_fare(data.dict())

    async def update_fare(self, id, d):
        return await self._service.update_fare(id, d.dict(exclude_unset=True))

    async def delete_fare(self, id):
        return await self._service.delete_fare(id)

    # ── Coding ────────────────────────────────────────────────────
    async def get_coding(self):
        return await self._service.get_coding()

    async def create_coding(self, data):
        return await self._service.create_coding(data.dict())

    async def update_coding(self, id, d):
        return await self._service.update_coding(id, d.dict(exclude_unset=True))

    async def delete_coding(self, id):
        return await self._service.delete_coding(id)

    # ── Officers ──────────────────────────────────────────────────
    async def get_officers(self):
        return await self._service.get_officers()

    async def create_officer(self, data):
        return await self._service.create_officer(data.dict())

    async def update_officer(self, id, d):
        return await self._service.update_officer(id, d.dict(exclude_unset=True))

    async def delete_officer(self, id):
        return await self._service.delete_officer(id)

    # ── Violations ────────────────────────────────────────────────
    async def get_violations(self):
        return await self._service.get_violations()

    async def create_violation(self, data):
        return await self._service.create_violation(data.dict())

    async def update_violation(self, id, d):
        return await self._service.update_violation(id, d.dict(exclude_unset=True))

    async def delete_violation(self, id):
        return await self._service.delete_violation(id)