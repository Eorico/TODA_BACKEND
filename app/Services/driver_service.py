from app.Models.driver_profile_model import RiderProfile
from app.Schemas.driver_schema import RiderProfileCreateSchema
from app.Models.contribution_or_butaw_model import Contribution_Or_Butaw
from fastapi import HTTPException
 


class RiderService:

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
            "expiration_date_license": profile.expiration_date_license,
            "expiration_date_orcr": profile.expiration_date_orcr,
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

        profile_id = str(profile.id)

        # Primary match: by driverid (admin sets this from the rider dropdown)
        # Fallback: by body_number in case driverid was stored differently
        contributions = await Contribution_Or_Butaw.find(
            Contribution_Or_Butaw.driverid == profile_id
        ).sort("-date").to_list()

        # Fallback: match by body_number if driverid query returned nothing
        if not contributions and profile.body_number and profile.body_number != "---":
            contributions = await Contribution_Or_Butaw.find(
                Contribution_Or_Butaw.body_number == profile.body_number
            ).sort("-date").to_list()

        total = sum(c.amount for c in contributions)

        return {
            "total_amount": total,
            "contributions": [
                {
                    "id":          str(c.id),
                    "full_name":   c.full_name,
                    "last_name":   c.last_name,
                    "body_number": c.body_number,
                    "amount":      c.amount,
                    "date":        c.date,
                    "status":      c.status,
                    "notes":       c.notes,
                }
                for c in contributions
            ],
        }