from Models.riderprofile_model import RiderProfile
from Schemas.rider_schema import RiderProfileCreateSchema
from fastapi import HTTPException

class RiderProfileService:

    @staticmethod
    async def create(user, data: RiderProfileCreateSchema) -> dict:
        existing = await RiderProfile.find_one(RiderProfile.user.id == user.id)
        if existing:
            raise HTTPException(status_code=400, detail="Rider profile already exists")

        profile = RiderProfile(
            user=user,
            address=data.address,
            license_url=data.license_url,
            tricycle_body_number=data.body_number
        )
        await profile.insert()
        return {"message": "Rider profile submitted, awaiting admin approval"}

    @staticmethod
    async def get_profile(user):
        profile = await RiderProfile.find_one(RiderProfile.user.id == user.id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    @staticmethod
    async def get_funds(user) -> dict:
        return {"funds": 0}

    @staticmethod
    async def is_approved(user) -> bool:
        profile = await RiderProfile.find_one(RiderProfile.user.id == user.id)
        return profile.member_status if profile else False