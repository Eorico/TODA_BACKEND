from Models.riderprofile_model import RiderProfile
from backend.src.Schemas.admin_schema import RiderProfileCreateSchema
from fastapi import HTTPException

async def  create_rider_profile(user, data: RiderProfileCreateSchema):
    existing = await RiderProfile.find_one(RiderProfile.user.id == user.id)
    if existing:
        raise HTTPException(status_code=400, detail=" Rider profile already exists")

    profile = RiderProfile(
        user=user,
        address=data.address,
        license_pic=data.license_pic,
        tricycle_body_number=data.tricycle_body_number
    )
    
    await profile.insert()
    return {"message": "Rider profile submitted, awaiting admin approval"}

async def get_rider_profile(user):
    profile = await RiderProfile.find_one(RiderProfile.user.id == user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

async def get_rider_funds(user):
    total_fund = 0 
    return {"funds": total_fund}

async def is_rider_approved(user):
    profile = await RiderProfile.find_one(RiderProfile.user.id == user.id)
    return profile.is_approved if profile else False
