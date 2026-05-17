# app/Services/DriverService.py
from datetime import datetime
from app.Contracts.i_driver_service import IDriverService
from app.Repositories.users.driver_repository import DriverRepository
from app.Repositories.users.user_repository import UserRepository
from app.Repositories.admin.contribution_repository import ContributionRepository
from app.Repositories.admin.violation_repository import ViolationRepository
from app.Repositories.admin.announcement_repository import AnnouncementRepository
from app.Repositories.admin.lost_and_found_repository import LostFoundRepository
from app.Repositories.admin.officer_repository import OfficerRepository
from app.Repositories.admin.fare_repository import FareRepository
from app.Repositories.admin.coding_repository import CodingRepository
from app.Exceptions.app_exception import NotFoundException, UnauthorizedException

class DriverService(IDriverService):

    def __init__(
        self,
        driver_repo:       DriverRepository,
        user_repo:         UserRepository,
        contribution_repo: ContributionRepository,
        violation_repo:    ViolationRepository,
        announcement_repo: AnnouncementRepository,
        lost_found_repo:   LostFoundRepository,
        officer_repo:      OfficerRepository,
        fare_repo:         FareRepository,
        coding_repo:       CodingRepository,
    ):
        self._drivers       = driver_repo
        self._users         = user_repo
        self._contributions = contribution_repo
        self._violations    = violation_repo
        self._announcements = announcement_repo
        self._lost_found    = lost_found_repo
        self._officers      = officer_repo
        self._fares         = fare_repo
        self._coding        = coding_repo

    async def get_profile(self, user: dict) -> dict:
        email = user.get("email")
        if not email:
            raise UnauthorizedException("Token missing email.")
        profile = await self._drivers.find_by_email(email)
        if not profile:
            raise NotFoundException("Driver profile")
        return {
            "id":                      str(profile.id),
            "full_name":               profile.full_name,
            "last_name":               profile.last_name,
            "body_number":             profile.body_number,
            "contact":                 profile.contact,
            "email":                   profile.email,
            "address":                 profile.address,
            "status":                  profile.status,
            "member_status":           profile.member_status,
            "license_url":             profile.license_url,
            "orcr_url":                profile.orcr_url,
            "expiration_date_license": profile.expiration_date_license,
            "expiration_date_orcr":    profile.expiration_date_orcr,
            "last_contribution":       profile.last_contribution,
            "created_at":              profile.created_at.isoformat(),
        }

    async def get_funds(self, user: dict) -> dict:
        profile = await self._drivers.find_by_email(user.get("email"))
        if not profile:
            raise NotFoundException("Driver profile")

        profile_id    = str(profile.id)
        contributions = await self._contributions.find_by_driver_id(profile_id)

        if not contributions and profile.body_number and profile.body_number != "---":
            contributions = await self._contributions.find_by_body_number(
                profile.body_number
            )

        total = sum(c.get("amount", 0) for c in contributions)
        return {"total_amount": total, "contributions": contributions}

    async def get_my_violations(self, user: dict) -> list:
        profile   = await self.get_profile(user)
        driver_id = profile["id"]
        full_name = f"{profile['full_name']} {profile['last_name']}".strip()
        return await self._violations.find_by_driver_id_or_name(
            driver_id, full_name
        )

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

    async def get_violations(self) -> list:
        return await self._violations.find_all()
    
    async def get_my_violations(self, user: dict) -> list:
        email = user.get("email")
        if not email:
            raise UnauthorizedException("Token missing email.")

        profile = await self._drivers.find_by_email(email)
        if not profile:
            raise NotFoundException("Driver profile")

        driver_id = str(profile.id)

        return await self._violations.find_by_driver_id(driver_id)

    async def approve(self, id: str) -> dict:
        profile  = await self._drivers.find_by_id(id)
        existing = await self._drivers.find_roster_by_email(profile.email)

        if not existing:
            await self._drivers.create_roster({
                "full_name":               f"{profile.full_name} {profile.last_name}",
                "body_number":             profile.body_number,
                "status":                  "active",
                "contrib":                 "₱0.00",
                "date":                    datetime.now().strftime("%b %d"),
                "email":                   profile.email or "—",
                "contact":                 profile.contact or "—",
                "license_url":             profile.license_url,
                "orcr_url":                profile.orcr_url,
                "expiration_date_license": profile.expiration_date_license,
                "expiration_date_orcr":    profile.expiration_date_orcr,
            })

        await self._users.activate(profile.email)
        profile.member_status = "approved"
        profile.status        = "Active"
        await profile.save()
        return {"message": "Driver approved and roster synced."}

    async def reject(self, id: str) -> dict:
        profile = await self._drivers.find_by_id(id)
        await self._users.delete_by_email(profile.email)
        await profile.delete()
        return {"message": "Driver rejected and account cleared."}

    async def delete(self, id: str) -> dict:
        profile = await self._drivers.find_by_id(id)
        await self._users.delete_by_email(profile.email)
        await self._drivers.delete_roster_by_email(profile.email)
        await profile.delete()
        return {"message": "Driver deleted successfully."}