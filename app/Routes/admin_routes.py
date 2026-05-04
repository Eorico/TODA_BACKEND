from fastapi import APIRouter, Depends, Body, HTTPException, File, UploadFile, Request
from slowapi import Limiter
from Middleware.rate_limiter import limiter
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

public_router = APIRouter(tags=["Admin"])

# ── Login (strictest limit — prevents brute force) ──────────────
@public_router.post("/login")
@limiter.limit("5/minute")
async def admin_login(request: Request, data: LoginSchema = Body(...)):
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
@limiter.limit("30/minute")
async def admin_dashboard(request: Request):
    return {"message": "Welcome Admin"}

# ── Riders ──────────────────────────────────────────────────────
@router.post("/riders")
@limiter.limit("20/minute")
async def create_rider(request: Request, data: RiderProfileCreateSchema):
    return await RiderController.create(data)

@router.post("/riders/{id}/license")
@limiter.limit("10/minute")        # file uploads — keep low
async def upload_rider_license(request: Request, id: str, license: UploadFile = File(...)):
    content = await license.read()
    base64_encoded = base64.b64encode(content).decode("utf-8")
    mime_type = license.content_type
    license_url = f"data:{mime_type};base64,{base64_encoded}"

    rider = await RiderProfile.get(PydanticObjectId(id))
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    await rider.set({"license_url": license_url})
    return {
        "message": "License processed and stored in database successfully",
        "type": "base64"
    }
    
@router.post("/riders/{id}/orcr")
@limiter.limit("10/minute")
async def upload_rider_orcr(request: Request, id: str, orcr: UploadFile = File(...)):
    content = await orcr.read()
    base64_encoded = base64.b64encode(content).decode("utf-8")
    orcr_url = f"data:{orcr.content_type};base64,{base64_encoded}"

    rider = await RiderProfile.get(PydanticObjectId(id))
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    await rider.set({"orcr_url": orcr_url})
    return {"message": "OR/CR stored successfully", "type": "base64"}

@router.get("/riders")
@limiter.limit("30/minute")
async def get_riders(request: Request):
    return await RiderController.get_all()

@router.put("/riders/{id}/accept")
@limiter.limit("20/minute")
async def approve_rider(request: Request, id: str):
    return await RiderController.approve(id)

@router.put("/riders/{id}/reject")
@limiter.limit("20/minute")
async def reject_rider(request: Request, id: str):
    return await RiderController.reject(id)

@router.put("/riders/{id}")
@limiter.limit("20/minute")
async def update_rider(request: Request, id: str, data: RiderProfileCreateSchema):
    return await RiderController.update(id, data)

@router.delete("/riders/{id}")
@limiter.limit("10/minute")        # deletes — extra caution
async def delete_rider(request: Request, id: str):
    return await RiderController.delete_by_id(id)

# ── Roster ───────────────────────────────────────────────────────
@router.get("/roster")
@limiter.limit("30/minute")
async def get_roster(request: Request):
    return await RosterController.get_all()

@router.post("/roster")
@limiter.limit("20/minute")
async def create_member(request: Request, data: MemberRosterSchema):
    return await RosterController.create(data)

@router.put("/roster/{id}")
@limiter.limit("20/minute")
async def update_member(request: Request, id: str, data: MemberRosterSchema):
    return await RosterController.update(id, data)

@router.delete("/roster/{id}")
@limiter.limit("10/minute")
async def delete_member(request: Request, id: str):
    return await RosterController.delete_by_id(id)

# ── Contributions ────────────────────────────────────────────────
@router.post("/contributions")
@limiter.limit("20/minute")
async def create_contribution(request: Request, data: ContributionSchema):
    return await ContributionController.create(data)

@router.get("/contributions")
@limiter.limit("30/minute")
async def get_contributions(request: Request):
    return await ContributionController.get_all()

@router.put("/contributions/{id}")
@limiter.limit("20/minute")
async def update_contribution(request: Request, id: str, data: ContributionSchema):
    return await ContributionController.update(id, data)

@router.delete("/contributions/{id}")
@limiter.limit("10/minute")
async def delete_contribution(request: Request, id: str):
    return await ContributionController.delete_by_id(id)

# ── Announcements ────────────────────────────────────────────────
@router.post("/announcements")
@limiter.limit("20/minute")
async def create_announcement(request: Request, data: AnnouncementSchema):
    return await AnnouncementController.create(data)

@router.get("/announcements")
@limiter.limit("30/minute")
async def get_announcements(request: Request):
    return await AnnouncementController.get_all()

@router.put("/announcements/{id}")
@limiter.limit("20/minute")
async def update_announcement(request: Request, id: str, data: AnnouncementSchema):
    return await AnnouncementController.update(id, data)

@router.delete("/announcements/{id}")
@limiter.limit("10/minute")
async def delete_announcement(request: Request, id: str):
    return await AnnouncementController.delete_by_id(id)

# ── Lost & Found ─────────────────────────────────────────────────
@router.post("/lost-found")
@limiter.limit("20/minute")
async def create_lost_found(request: Request, data: LostFoundSchema):
    return await LostFoundController.create(data)

@router.get("/lost-found")
@limiter.limit("30/minute")
async def get_lost_found(request: Request):
    return await LostFoundController.get_all()

@router.put("/lost-found/{id}")
@limiter.limit("20/minute")
async def update_lost_found(request: Request, id: str, data: LostFoundSchema):
    return await LostFoundController.update(id, data)

@router.delete("/lost-found/{id}")
@limiter.limit("10/minute")
async def delete_lost_found(request: Request, id: str):
    return await LostFoundController.delete_by_id(id)

# ── Fare ─────────────────────────────────────────────────────────
@router.post("/fare")
@limiter.limit("20/minute")
async def create_fare(request: Request, data: FareSchema):
    return await FareController.create(data)

@router.get("/fare")
@limiter.limit("30/minute")
async def get_fare(request: Request):
    return await FareController.get_all()

@router.put("/fare/{id}")
@limiter.limit("20/minute")
async def update_fare(request: Request, id: str, data: FareSchema):
    return await FareController.update(id, data)

@router.delete("/fare/{id}")
@limiter.limit("10/minute")
async def delete_fare(request: Request, id: str):
    return await FareController.delete_by_id(id)

# ── Coding ───────────────────────────────────────────────────────
@router.post("/coding")
@limiter.limit("20/minute")
async def add_coding(request: Request, data: CodingSchema):
    return await CodingController.create(data)

@router.get("/coding")
@limiter.limit("30/minute")
async def get_coding(request: Request):
    return await CodingController.get_all()

@router.put("/coding/{id}")
@limiter.limit("20/minute")
async def update_coding(request: Request, id: str, data: CodingSchema):
    return await CodingController.update(id, data)

@router.delete("/coding/{id}")
@limiter.limit("10/minute")
async def delete_coding(request: Request, id: str):
    return await CodingController.delete_by_id(id)

# ── Officers ─────────────────────────────────────────────────────
@router.post("/officers")
@limiter.limit("20/minute")
async def create_officer(request: Request, data: OfficerSchema):
    return await OfficerController.create(data)

@router.get("/officers")
@limiter.limit("30/minute")
async def get_officers(request: Request):
    return await OfficerController.get_all()

@router.put("/officers/{id}")
@limiter.limit("20/minute")
async def update_officer(request: Request, id: str, data: OfficerSchema):
    return await OfficerController.update(id, data)

@router.delete("/officers/{id}")
@limiter.limit("10/minute")
async def delete_officer(request: Request, id: str):
    return await OfficerController.delete_by_id(id)

# ── Violations ───────────────────────────────────────────────────
@router.post("/violations")
@limiter.limit("20/minute")
async def create_violation(request: Request, data: ViolationSchema):
    return await ViolationController.create(data)

@router.get("/violations")
@limiter.limit("30/minute")
async def get_violations(request: Request):
    return await ViolationController.get_all()

@router.get("/violations/{id}")
@limiter.limit("30/minute")
async def get_violation(request: Request, id: str):
    item = await ViolationController.get_or_404(id)
    from Controllers.base_controller import serialize
    return serialize(item)

@router.put("/violations/{id}")
@limiter.limit("20/minute")
async def update_violation(request: Request, id: str, data: ViolationSchema):
    return await ViolationController.update(id, data)

@router.delete("/violations/{id}")
@limiter.limit("10/minute")
async def delete_violation(request: Request, id: str):
    return await ViolationController.delete_by_id(id)