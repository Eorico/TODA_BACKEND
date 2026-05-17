from app.Contracts.i_admin_service import IAdminService
from app.Services.users.driver_service import DriverService
from app.Repositories.admin.announcement_repository import AnnouncementRepository
from app.Repositories.admin.coding_repository import CodingRepository
from app.Repositories.admin.contribution_repository import ContributionRepository
from app.Repositories.admin.fare_repository import FareRepository
from app.Repositories.admin.lost_and_found_repository import LostFoundRepository
from app.Repositories.admin.officer_repository import OfficerRepository
from app.Repositories.admin.roster_repository import RosterRepository
from app.Repositories.admin.violation_repository import ViolationRepository
from app.Repositories.users.driver_repository import DriverRepository
from app.Repositories.users.user_repository import UserRepository
from app.Exceptions.app_exception import NotFoundException
import base64
import asyncio
from fastapi import UploadFile

class AdminService(IAdminService):

    def __init__(
        self,
        driver_service:    DriverService,
        driver_repo:       DriverRepository,
        user_repo:         UserRepository,
        announcement_repo: AnnouncementRepository,
        coding_repo:       CodingRepository,
        contribution_repo: ContributionRepository,
        fare_repo:         FareRepository,
        lost_found_repo:   LostFoundRepository,
        officer_repo:      OfficerRepository,
        roster_repo:       RosterRepository,
        violation_repo:    ViolationRepository,
    ):
        self._driver_service  = driver_service
        self._drivers         = driver_repo
        self._users           = user_repo
        self._announcements   = announcement_repo
        self._coding          = coding_repo
        self._contributions   = contribution_repo
        self._fares           = fare_repo
        self._lost_found      = lost_found_repo
        self._officers        = officer_repo
        self._roster          = roster_repo
        self._violations      = violation_repo

    # ── Drivers ─────────────────────────────────────────────────
    async def get_all_drivers(self):
        return await self._drivers.find_all()

    async def approve_driver(self, id):
        return await self._driver_service.approve(id)

    async def reject_driver(self, id):
        return await self._driver_service.reject(id)

    async def delete_driver(self, id):
        return await self._driver_service.delete(id)

    async def delete_driver_cascade(self, id: str) -> dict:
        # 1. Fetch the driver profile to get email + body_number for related lookups
        profile = await self._drivers.find_by_id(id)
        if not profile:
            raise NotFoundException("Driver")

        driver_id   = str(profile.id)
        email       = profile.email
        body_number = profile.body_number

        # 2. Delete all related records in parallel — roster, violations, contributions
        #    and user account all run simultaneously instead of sequentially
        await asyncio.gather(
            self._roster.delete_by_email(email),
            self._violations.delete_by_driver(driver_id, body_number),
            self._contributions.delete_by_driver(driver_id, body_number),
            self._users.delete_by_email(email),
            return_exceptions=True,  # don't abort if one fails (e.g. roster didn't exist)
        )

        # 3. Delete the driver profile itself last
        await profile.delete()

        return {
            "message": (
                f"Driver {profile.full_name} {profile.last_name} "
                f"and all related records deleted successfully."
            )
        }

    async def delete_roster_by_email(self, email: str):
        return await self._roster.delete_by_email(email)

    async def update_driver(self, id, data: dict):
        return await self._drivers.update(id, data)

    async def upload_document(self, id: str, file: UploadFile, field: str) -> dict:
        content = await file.read()
        encoded = base64.b64encode(content).decode("utf-8")
        url     = f"data:{file.content_type};base64,{encoded}"
        profile = await self._drivers.find_by_id(id)
        setattr(profile, field, url)
        await profile.save()
        return {"message": f"{field} uploaded successfully.", "type": "base64"}

    # ── Roster ──────────────────────────────────────────────────
    async def get_roster(self):              return await self._roster.find_all()
    async def create_roster(self, data):     return await self._roster.create(data)
    async def update_roster(self, id, data): return await self._roster.update(id, data)
    async def delete_roster(self, id):       return await self._roster.delete(id)

    # ── Contributions ────────────────────────────────────────────
    async def get_contributions(self):           return await self._contributions.find_all()
    async def create_contribution(self, data):   return await self._contributions.create(data)
    async def update_contribution(self, id, d):  return await self._contributions.update(id, d)
    async def delete_contribution(self, id):     return await self._contributions.delete(id)

    # ── Announcements ────────────────────────────────────────────
    async def get_announcements(self):           return await self._announcements.find_all_sorted()
    async def create_announcement(self, data):   return await self._announcements.create(data)
    async def update_announcement(self, id, d):  return await self._announcements.update(id, d)
    async def delete_announcement(self, id):     return await self._announcements.delete(id)

    # ── Lost & Found ─────────────────────────────────────────────
    async def get_lost_found(self):           return await self._lost_found.find_all()
    async def create_lost_found(self, data):  return await self._lost_found.create(data)
    async def update_lost_found(self, id, d): return await self._lost_found.update(id, d)
    async def delete_lost_found(self, id):    return await self._lost_found.delete(id)

    # ── Fare ─────────────────────────────────────────────────────
    async def get_fare(self):          return await self._fares.find_all()
    async def create_fare(self, data): return await self._fares.create(data)
    async def update_fare(self, id, d): return await self._fares.update(id, d)
    async def delete_fare(self, id):   return await self._fares.delete(id)

    # ── Coding ───────────────────────────────────────────────────
    async def get_coding(self):          return await self._coding.find_all()
    async def create_coding(self, data): return await self._coding.create(data)
    async def update_coding(self, id, d): return await self._coding.update(id, d)
    async def delete_coding(self, id):   return await self._coding.delete(id)

    # ── Officers ─────────────────────────────────────────────────
    async def get_officers(self):          return await self._officers.find_all()
    async def create_officer(self, data):  return await self._officers.create(data)
    async def update_officer(self, id, d): return await self._officers.update(id, d)
    async def delete_officer(self, id):    return await self._officers.delete(id)

    # ── Violations ───────────────────────────────────────────────
    async def get_violations(self):          return await self._violations.find_all()
    async def create_violation(self, data):  return await self._violations.create(data)
    async def update_violation(self, id, d): return await self._violations.update(id, d)
    async def delete_violation(self, id):    return await self._violations.delete(id)