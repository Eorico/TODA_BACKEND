from fastapi import APIRouter, Depends, Body, HTTPException, File, UploadFile
from Middleware.role_base_access import verify_role
from Schemas.auth_schema import LoginSchema
from Schemas.rider_schema import RiderProfileCreateSchema
from Schemas.admin_schema import (
    AnnouncementSchema, LostFoundSchema, FareSchema,
    CodingSchema, OfficerSchema, ContributionSchema, MemberRosterSchema,
    ViolationSchema
)
from Services.auth_service import AuthService

from Controllers.admin_controller import (
    RiderController, RosterController, ContributionController,
    AnnouncementController, LostFoundController, FareController,
    CodingController, OfficerController, ViolationController
)
from beanie import PydanticObjectId
from Models.riderprofile_model import RiderProfile
import base64

public_router = APIRouter(
    tags=["Admin"]
)

@public_router.post("/login")
async def admin_login(data: LoginSchema = Body(...)):
    result = await AuthService.login(data)   

    if result["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied: not admin")

    return {
        "message": "Admin logged in successfully",
        "access_token": result["access_token"]
    }

router = APIRouter(
    tags=["Admin"],
    dependencies=[Depends(verify_role("admin"))]
)

@router.get("/dashboard")
async def admin_dashboard():
    return {"message": "Welcome Admin"}

# ── Riders ──────────────────────────────────────────────────────
@router.post("/riders")
async def create_rider(data: RiderProfileCreateSchema):
    return await RiderController.create(data)

@router.post("/riders/{id}/license")
async def upload_rider_license(id: str, license: UploadFile = File(...)):
    content = await license.read()
    
    base64_encoded = base64.b64encode(content).decode("utf-8")
    mime_type = license.content_type
    license_url = f"data:{mime_type};base64,{base64_encoded}"
    
    rider = await RiderProfile.get(PydanticObjectId(id))
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    await rider.set({"license_url": license_url})
    return {
        "message": "License processed and store in database successfully",
        "type": "base64"
    }

@router.get("/riders")
async def get_riders():
    return await RiderController.get_all()

@router.put("/riders/{id}/accept")
async def approve_rider(id: str):
    return await RiderController.approve(id)

@router.put("/riders/{id}/reject")
async def reject_rider(id: str):
    """
    Handles the rejection of a rider application.
    """
    return await RiderController.reject(id)

@router.put("/riders/{id}")
async def update_rider(id: str, data: RiderProfileCreateSchema):
    return await RiderController.update(id, data)

@router.delete("/riders/{id}")
async def delete_rider(id: str):
    return await RiderController.delete_by_id(id)


# ── Roster ───────────────────────────────────────────────────────
@router.get("/roster")
async def get_roster():
    return await RosterController.get_all()

@router.post("/roster")
async def create_member(data: MemberRosterSchema):
    return await RosterController.create(data)

@router.put("/roster/{id}")
async def update_member(id: str, data: MemberRosterSchema):
    return await RosterController.update(id, data)

@router.delete("/roster/{id}")
async def delete_member(id: str):
    return await RosterController.delete_by_id(id)

# ── Contributions ────────────────────────────────────────────────
@router.post("/contributions")
async def create_contribution(data: ContributionSchema):
    return await ContributionController.create(data)

@router.get("/contributions")
async def get_contributions():
    return await ContributionController.get_all()

@router.put("/contributions/{id}")
async def update_contribution(id: str, data: ContributionSchema):
    return await ContributionController.update(id, data)

@router.delete("/contributions/{id}")
async def delete_contribution(id: str):
    return await ContributionController.delete_by_id(id)

# ── Announcements ────────────────────────────────────────────────
@router.post("/announcements")
async def create_announcement(data: AnnouncementSchema):
    return await AnnouncementController.create(data)

@router.get("/announcements")
async def get_announcements():
    return await AnnouncementController.get_all()

@router.put("/announcements/{id}")
async def update_announcement(id: str, data: AnnouncementSchema):
    return await AnnouncementController.update(id, data)

@router.delete("/announcements/{id}")
async def delete_announcement(id: str):
    return await AnnouncementController.delete_by_id(id)

# ── Lost & Found ─────────────────────────────────────────────────
@router.post("/lost-found")
async def create_lost_found(data: LostFoundSchema):
    return await LostFoundController.create(data)

@router.get("/lost-found")
async def get_lost_found():
    return await LostFoundController.get_all()

@router.put("/lost-found/{id}")
async def update_lost_found(id: str, data: LostFoundSchema):
    return await LostFoundController.update(id, data)

@router.delete("/lost-found/{id}")
async def delete_lost_found(id: str):
    return await LostFoundController.delete_by_id(id)

# ── Fare ─────────────────────────────────────────────────────────
@router.post("/fare")
async def create_fare(data: FareSchema):
    return await FareController.create(data)

@router.get("/fare")
async def get_fare():
    return await FareController.get_all()

@router.put("/fare/{id}")
async def update_fare(id: str, data: FareSchema):
    return await FareController.update(id, data)

@router.delete("/fare/{id}")
async def delete_fare(id: str):
    return await FareController.delete_by_id(id)

# ── Coding ───────────────────────────────────────────────────────
@router.post("/coding")
async def add_coding(data: CodingSchema):
    return await CodingController.create(data)

@router.get("/coding")
async def get_coding():
    return await CodingController.get_all()

@router.put("/coding/{id}")
async def update_coding(id: str, data: CodingSchema):
    return await CodingController.update(id, data)

@router.delete("/coding/{id}")
async def delete_coding(id: str):
    return await CodingController.delete_by_id(id)

# ── Officers ─────────────────────────────────────────────────────
@router.post("/officers")
async def create_officer(data: OfficerSchema):
    return await OfficerController.create(data)

@router.get("/officers")
async def get_officers():
    return await OfficerController.get_all()

@router.put("/officers/{id}")
async def update_officer(id: str, data: OfficerSchema):
    return await OfficerController.update(id, data)

@router.delete("/officers/{id}")
async def delete_officer(id: str):
    return await OfficerController.delete_by_id(id)

# ── Violations ───────────────────────────────────────────────────
@router.post("/violations")
async def create_violation(data: ViolationSchema):
    return await ViolationController.create(data)

@router.get("/violations")
async def get_violations():
    return await ViolationController.get_all()

@router.get("/violations/{id}")
async def get_violation(id: str):
    item = await ViolationController.get_or_404(id)
    from Controllers.base_controller import serialize
    return serialize(item)

@router.put("/violations/{id}")
async def update_violation(id: str, data: ViolationSchema):
    return await ViolationController.update(id, data)

@router.delete("/violations/{id}")
async def delete_violation(id: str):
    return await ViolationController.delete_by_id(id)