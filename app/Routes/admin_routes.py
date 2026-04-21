from fastapi import APIRouter, Depends, Body, HTTPException
from Middleware.role_base_access import verify_role
from Models.announcement_model import Announcement
from Models.officer_model import Officer
from Models.riderprofile_model import RiderProfile
from Models.lostfound_model import LostFound
from Models.fare_matrix_model import Fare
from Models.coding_model import CodingSchedule
from Models.roster_model import MemberRoster
from Models.contribution_or_butaw_model import Contribution_Or_Butaw
from Models.violation_model import Violation
from Schemas.auth_schema import LoginSchema
from Schemas.rider_schema import RiderProfileCreateSchema
from Schemas.admin_schema import (
    AnnouncementSchema, LostFoundSchema, FareSchema,
    CodingSchema, OfficerSchema, ContributionSchema, MemberRosterSchema,
    ViolationSchema
)
from Services.auth_service import login

public_router = APIRouter(
    tags=["Admin"]
)

@public_router.post("/login")
async def admin_login(data: LoginSchema = Body(...)):
    
    result = await login(data)

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

def serialize(doc):
    return {**doc.model_dump(), "id": str(doc.id)}

@router.get("/dashboard")
async def admin_dashboard():
    return {"message": "Welcome Admin",}
    
@router.post("/riders")
async def create_rider(data: RiderProfileCreateSchema):
    new_rider = RiderProfile(**data.dict())
    await new_rider.insert()
    return {"message": "Rider added"}

@router.get("/riders")
async def get_all_riders():
    riders = await RiderProfile.find_all().to_list()
    return [serialize(r) for r in riders]

@router.put("/riders/approve/{id}")  # ✅ specific route FIRST
async def approve_rider(id: str):
    rider = await RiderProfile.get(id)
    if not rider:
        return {"message": "Rider not found"}
    rider.member_status = "approved"
    rider.status = "active"
    await rider.save()
    return {"message": "Rider approved"}

@router.put("/riders/{id}")          # ✅ dynamic route AFTER
async def update_rider(id: str, data: RiderProfileCreateSchema):
    rider = await RiderProfile.get(id)
    if not rider:
        return {"message": "Rider not found"}
    for key, value in data.dict(exclude_unset=True).items():
        setattr(rider, key, value)
    await rider.save()
    return {"message": "Rider updated"}

@router.delete("/riders/{id}")
async def delete_rider(id: str):
    rider = await RiderProfile.get(id)
    if not rider:
        return {"message": "Rider not found"}
    await rider.delete()
    return {"message": "Rider deleted"}

@router.get("/roster")
async def get_roster():
    members = await MemberRoster.find_all().to_list()
    return [serialize(m) for m in members]

@router.post("/roster")
async def create_member(data: MemberRosterSchema):
    new_member = MemberRoster(**data.dict())
    await new_member.insert()
    return {"message": "Member added to roster"}

@router.put("/roster/{id}")
async def update_member(id: str, data: MemberRosterSchema):
    member = await MemberRoster.get(id)
    if not member:
        return {"message": "Member not found"}

    # Dynamically update based on the schema payload (name, status, contrib, etc.)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(member, key, value)

    await member.save()
    return {"message": "Member record updated"}

@router.delete("/roster/{id}")
async def delete_member(id: str):
    member = await MemberRoster.get(id)
    if not member:
        return {"message": "Member not found"}
    
    await member.delete()
    return {"message": "Member removed from roster"}

@router.post("/contributions")
async def create_contribution(data: ContributionSchema):
    new_record = Contribution_Or_Butaw(**data.dict())
    await new_record.insert()
    return {"message": "Contribution recorded successfully"}

@router.get("/contributions")
async def get_all_contributions():
    records = await Contribution_Or_Butaw.find_all().to_list()
    return [serialize(r) for r in records]

@router.put("/contributions/{id}")
async def update_contribution(id: str, data: ContributionSchema):
    record = await Contribution_Or_Butaw.get(id)
    if not record:
        return {"message": "Contribution or Butaw not found"}
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    
    await record.save()
    return {"message": "Record updated"}

@router.delete("/contributions/{id}")
async def delete_contribution(id: str):
    record = await Contribution_Or_Butaw.get(id)
    if not record:
        return {"message": "Record not found"}
    
    await record.delete()
    return {"message": "Record deleted"}

@router.post("/announcements")
async def create_announcement(data: AnnouncementSchema):
    announcement = Announcement(**data.dict())
    await announcement.insert()
    return {"message": "Announcement posted!"}


@router.get("/announcements")
async def get_announcements():
    announcements = await Announcement.find_all().to_list()
    return [serialize(a) for a in announcements]

@router.put("/announcements/{id}")
async def update_announcement(id: str, data: AnnouncementSchema):
    announcement = await Announcement.get(id)

    if not announcement:
        return {"message": "Announcement not found"}

    for k, v in data.dict(exclude_unset=True).items():
        setattr(announcement, k, v)

    await announcement.save()
    return {"message": "Updated"}

@router.delete("/announcements/{id}")
async def delete_announcement(id: str):
    announcement = await Announcement.get(id)

    if not announcement:
        return {"message": "Announcement not found"}

    await announcement.delete()
    return {"message": "Announcement deleted"}

@router.post("/lost-found")
async def create_lost_found(data: LostFoundSchema):
    item = LostFound(**data.dict())
    await item.insert()
    return {"message": "Item posted"}

@router.get("/lost-found")
async def get_lost_found():
    items = await LostFound.find_all().to_list()
    return [serialize(i) for i in items]

@router.put("/lost-found/{id}")
async def update_lost_found(id: str, data: LostFoundSchema):
    item = await LostFound.get(id)

    if not item:
        return {"message": "Item not found"}

    for k, v in data.dict(exclude_unset=True).items():
        setattr(item, k, v)

    await item.save()
    return {"message": "Item updated"}

@router.delete("/lost-found/{id}")
async def delete_lost_found(id: str):
    item = await LostFound.get(id)

    if not item:
        return {"message": "Item not found"}

    await item.delete()
    return {"message": "Item deleted"}

@router.post("/fare")
async def create_fare(data: FareSchema):
    fare = Fare(**data.dict())
    await fare.insert()
    return {"message": "Fare created"}

@router.get("/fare")
async def get_fare():
    return await Fare.find_all().to_list()

@router.put("/fare/{id}")
async def update_fare(id: str, data: FareSchema):
    fare = await Fare.get(id)

    if not fare:
        return {"message": "Fare not found"}

    for k, v in data.dict(exclude_unset=True).items():
        setattr(fare, k, v)

    await fare.save()
    return {"message": "Fare updated"}

@router.delete("/fare/{id}")
async def delete_fare(id: str):
    fare = await Fare.get(id)

    if not fare:
        return {"message": "Fare not found"}

    await fare.delete()
    return {"message": "Fare deleted"}

@router.post("/coding")
async def add_coding(data: CodingSchema):
    coding = CodingSchedule(**data.dict())
    await coding.insert()
    return {"message": "Coding added"}

@router.get("/coding")
async def get_coding():
    items = await CodingSchedule.find_all().to_list()
    return [serialize(c) for c in items]

@router.put("/coding/{id}")
async def update_coding(id: str, data: CodingSchema):
    coding = await CodingSchedule.get(id)

    if not coding:
        return {"message": "Coding not found"}

    for k, v in data.dict(exclude_unset=True).items():
        setattr(coding, k, v)

    await coding.save()
    return {"message": "Coding updated"}

@router.delete("/coding/{id}")
async def delete_coding(id: str):
    coding = await CodingSchedule.get(id)

    if not coding:
        return {"message": "Coding not found"}

    await coding.delete()
    return {"message": "Coding deleted"}

@router.post("/officers")
async def create_officer(data: OfficerSchema):
    officer = Officer(**data.dict())
    await officer.insert()
    return {"message": "Officer added"}

@router.get("/officers")
async def get_officers():
    officers = await Officer.find_all().to_list()
    return [serialize(o) for o in officers]

@router.put("/officers/{id}")
async def update_officer(id: str, data: OfficerSchema):
    officer = await Officer.get(id)

    if not officer:
        return {"message": "Officer not found"}

    for k, v in data.dict(exclude_unset=True).items():
        setattr(officer, k, v)

    await officer.save()
    return {"message": "Officer updated"}

@router.delete("/officers/{id}")
async def delete_officer(id: str):
    officer = await Officer.get(id)

    if not officer:
        return {"message": "Officer not found"}

    await officer.delete()
    return {"message": "Officer removed"}

@router.post("/violations")
async def create_violation(data: ViolationSchema):
    violation = Violation(**data.dict())
    await violation.insert()
    return {"message": "Violation recorded"}

@router.get("/violations")
async def get_violations():
    items = await Violation.find_all().to_list()
    return [serialize(v) for v in items]

@router.get("/violations/{id}")
async def get_violation(id: str):
    item = await Violation.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Violation not found")
    return serialize(item)

@router.put("/violations/{id}")
async def update_violation(id: str, data: ViolationSchema):
    item = await Violation.get(id)
    if not item:
        return {"message": "Violation not found"}
    for k, v in data.dict(exclude_unset=True).items():
        setattr(item, k, v)
    await item.save()
    return {"message": "Violation updated"}

@router.delete("/violations/{id}")
async def delete_violation(id: str):
    item = await Violation.get(id)
    if not item:
        return {"message": "Violation not found"}
    await item.delete()
    return {"message": "Violation deleted"}