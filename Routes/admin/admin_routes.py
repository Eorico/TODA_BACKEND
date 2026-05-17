from fastapi import APIRouter, Depends, Request, File, UploadFile, Body
from app.Providers.app_service_provider import admin_controller
from app.Http.Middleware.auth_middleware import verify_role
from app.Http.Middleware.rate_limiter import limiter
from app.Http.Requests.auth_request import LoginRequest
from app.Http.Requests.admin_request import (
    DriverUpdateRequest, AnnouncementRequest, OfficerRequest,
    ContributionRequest, LostFoundRequest, FareRequest,
    CodingRequest, ViolationRequest, RosterRequest,
)

public_router = APIRouter(tags=["Admin"])
router        = APIRouter(tags=["Admin"], dependencies=[Depends(verify_role("admin"))])

@public_router.post("/login")
@limiter.limit("5/minute")
async def admin_login(request: Request, data: LoginRequest = Body(...)):
    return await admin_controller.login(data)

# ── Drivers ───────────────────────────────────────────────────────────────
@router.get("/riders")
async def get_riders(r: Request):
    return await admin_controller.get_drivers()

@router.put("/riders/{id}/accept")
async def approve_rider(r: Request, id: str):
    return await admin_controller.approve_driver(id)

@router.put("/riders/{id}/reject")
async def reject_rider(r: Request, id: str):
    return await admin_controller.reject_driver(id)

@router.post("/riders/{id}/license")
async def upload_license(r: Request, id: str, license: UploadFile = File(...)):
    return await admin_controller.upload_license(id, license)

@router.post("/riders/{id}/orcr")
async def upload_orcr(r: Request, id: str, orcr: UploadFile = File(...)):
    return await admin_controller.upload_orcr(id, orcr)

# ← IMPORTANT: cascade must be before generic /{id} routes
# FastAPI matches top-to-bottom — /riders/{id}/cascade would be caught
# by /riders/{id} if that was registered first
@router.delete("/riders/{id}/cascade")
async def delete_rider_cascade(r: Request, id: str):
    return await admin_controller.delete_driver_cascade(id)

@router.put("/riders/{id}")
async def update_rider(r: Request, id: str, d: DriverUpdateRequest):
    return await admin_controller.update_driver(id, d)

@router.delete("/riders/{id}")
async def delete_rider(r: Request, id: str):
    return await admin_controller.delete_driver(id)

# ── Roster ────────────────────────────────────────────────────────────────
# ← by-email must be before /{id} for same reason
@router.delete("/roster/by-email/{email}")
async def delete_roster_by_email(r: Request, email: str):
    return await admin_controller.delete_roster_by_email(email)

@router.get("/roster")
async def get_roster(r: Request):
    return await admin_controller.get_roster()

@router.post("/roster")
async def create_roster(r: Request, d: RosterRequest):
    return await admin_controller.create_roster(d)

@router.put("/roster/{id}")
async def update_roster(r: Request, id: str, d: RosterRequest):
    return await admin_controller.update_roster(id, d)

@router.delete("/roster/{id}")
async def delete_roster(r: Request, id: str):
    return await admin_controller.delete_roster(id)

# ── Contributions ─────────────────────────────────────────────────────────
@router.get("/contributions")
async def get_contributions(r: Request):
    return await admin_controller.get_contributions()

@router.post("/contributions")
async def create_contribution(r: Request, d: ContributionRequest):
    return await admin_controller.create_contribution(d)

@router.put("/contributions/{id}")
async def update_contribution(r: Request, id: str, d: ContributionRequest):
    return await admin_controller.update_contribution(id, d)

@router.delete("/contributions/{id}")
async def delete_contribution(r: Request, id: str):
    return await admin_controller.delete_contribution(id)

# ── Announcements ─────────────────────────────────────────────────────────
@router.get("/announcements")
async def get_announcements(r: Request):
    return await admin_controller.get_announcements()

@router.post("/announcements")
async def create_announcement(r: Request, d: AnnouncementRequest):
    return await admin_controller.create_announcement(d)

@router.put("/announcements/{id}")
async def update_announcement(r: Request, id: str, d: AnnouncementRequest):
    return await admin_controller.update_announcement(id, d)

@router.delete("/announcements/{id}")
async def delete_announcement(r: Request, id: str):
    return await admin_controller.delete_announcement(id)

# ── Lost & Found ──────────────────────────────────────────────────────────
@router.get("/lost-found")
async def get_lf(r: Request):
    return await admin_controller.get_lost_found()

@router.post("/lost-found")
async def create_lf(r: Request, d: LostFoundRequest):
    return await admin_controller.create_lost_found(d)

@router.put("/lost-found/{id}")
async def update_lf(r: Request, id: str, d: LostFoundRequest):
    return await admin_controller.update_lost_found(id, d)

@router.delete("/lost-found/{id}")
async def delete_lf(r: Request, id: str):
    return await admin_controller.delete_lost_found(id)

# ── Fare ──────────────────────────────────────────────────────────────────
@router.get("/fare")
async def get_fare(r: Request):
    return await admin_controller.get_fare()

@router.post("/fare")
async def create_fare(r: Request, d: FareRequest):
    return await admin_controller.create_fare(d)

@router.put("/fare/{id}")
async def update_fare(r: Request, id: str, d: FareRequest):
    return await admin_controller.update_fare(id, d)

@router.delete("/fare/{id}")
async def delete_fare(r: Request, id: str):
    return await admin_controller.delete_fare(id)

# ── Coding ────────────────────────────────────────────────────────────────
@router.get("/coding")
async def get_coding(r: Request):
    return await admin_controller.get_coding()

@router.post("/coding")
async def create_coding(r: Request, d: CodingRequest):
    return await admin_controller.create_coding(d)

@router.put("/coding/{id}")
async def update_coding(r: Request, id: str, d: CodingRequest):
    return await admin_controller.update_coding(id, d)

@router.delete("/coding/{id}")
async def delete_coding(r: Request, id: str):
    return await admin_controller.delete_coding(id)

# ── Officers ──────────────────────────────────────────────────────────────
@router.get("/officers")
async def get_officers(r: Request):
    return await admin_controller.get_officers()

@router.post("/officers")
async def create_officer(r: Request, d: OfficerRequest):
    return await admin_controller.create_officer(d)

@router.put("/officers/{id}")
async def update_officer(r: Request, id: str, d: OfficerRequest):
    return await admin_controller.update_officer(id, d)

@router.delete("/officers/{id}")
async def delete_officer(r: Request, id: str):
    return await admin_controller.delete_officer(id)

# ── Violations ────────────────────────────────────────────────────────────
@router.get("/violations")
async def get_violations(r: Request):
    return await admin_controller.get_violations()

@router.post("/violations")
async def create_violation(r: Request, d: ViolationRequest):
    return await admin_controller.create_violation(d)

@router.put("/violations/{id}")
async def update_violation(r: Request, id: str, d: ViolationRequest):
    return await admin_controller.update_violation(id, d)

@router.delete("/violations/{id}")
async def delete_violation(r: Request, id: str):
    return await admin_controller.delete_violation(id)