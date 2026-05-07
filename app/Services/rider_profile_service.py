from app.Models.driver_profile_model import RiderProfile
from app.Schemas.driver_schema import RiderProfileCreateSchema
from fastapi import HTTPException

class RiderProfileService:

    @staticmethod
    async def get_profile(user: dict):
        email = user.get("email")
        if not email:
            raise HTTPException(
                status_code=401,
                detail="Token missing email. Please log out and log in again."
            )

        profile = await RiderProfile.find_one(
            RiderProfile.email == email,
            fetch_links=False
        )

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        return {
            "id": str(profile.id),
            "full_name": profile.full_name,
            "last_name": profile.last_name,
            "body_number": profile.body_number,
            "contact": profile.contact,
            "email": profile.email,
            "address": profile.address,
            "status": profile.status,
            "member_status": profile.member_status,
            "license_url": profile.license_url,
            "orcr_url": profile.orcr_url,
            "last_contribution": profile.last_contribution,
            "created_at": profile.created_at.isoformat(),
        }

    @staticmethod
    async def create(user: dict, data: RiderProfileCreateSchema) -> dict:
        existing = await RiderProfile.find_one(
            RiderProfile.email == user.get("email"),
            fetch_links=False
        )
        if existing:
            raise HTTPException(status_code=400, detail="Rider profile already exists")

        profile = RiderProfile(
            full_name=data.full_name,
            last_name=data.last_name,
            body_number=data.body_number,
            contact=data.contact,
            email=data.email or user.get("email"),
            address=data.address,
            license_url=data.license_url,
            orcr_url=data.orcr_url,
        )
        await profile.insert()
        return {"message": "Rider profile submitted, awaiting admin approval"}

    @staticmethod
    async def is_approved(user: dict) -> bool:
        profile = await RiderProfile.find_one(
            RiderProfile.email == user.get("email"),
            fetch_links=False
        )
        return profile.member_status if profile else False

    @staticmethod
    async def get_funds(user: dict) -> dict:
        profile = await RiderProfile.find_one(
            RiderProfile.email == user.get("email"),
            fetch_links=False
        )
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {
            "last_contribution": profile.last_contribution,
        }