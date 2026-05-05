from .base_controller import BaseController
from Models.announcement_model import Announcement
from Models.officer_model import Officer
from Models.driver_profile_model import RiderProfile
from Models.lostfound_model import LostFound
from Models.fare_matrix_model import Fare
from Models.coding_model import CodingSchedule
from Models.roster_model import MemberRoster
from Models.contribution_or_butaw_model import Contribution_Or_Butaw
from Models.violation_model import Violation
from Models.user_model import User 
from Utils.serializer import serialize
from fastapi import HTTPException
from datetime import datetime

class RiderController(BaseController):
    model = RiderProfile
    
    @classmethod
    async def create(cls, data) -> dict:
        rider = RiderProfile(**data.dict())
        await rider.insert()
        return {
            "message": "Rider Added",
            "_id": str(rider.id) 
        }
    
    @classmethod
    async def update(cls, id: str, data) -> dict:
        rider = await cls.get_or_404(id)
        update_data = data.dict(exclude_unset=True)
        update_data.pop('licens_url', None)  
        for k, v in update_data.items():
            setattr(rider, k, v)
        await rider.save()
        return {"message": "Rider Updated"}

    @classmethod
    async def delete_by_id(cls, id: str) -> dict:         # ← override BaseController
        rider = await cls.get_or_404(id)

        user = None
        if rider.user:
            try:
                rider_fetched = await RiderProfile.get(id, fetch_links=True)
                user = rider_fetched.user
            except Exception:
                pass
            
        if not user:
            user = await User.find_one(User.email == rider.email)
        
        if user:
            await user.delete()
            
        roster_entry = await MemberRoster.find_one(MemberRoster.email == rider.email)
        if roster_entry:
            await roster_entry.delete()

        await rider.delete()
        return {"message": "Driver and user account deleted successfully"}

    @classmethod
    async def approve(cls, id: str) -> dict:
        rider = await RiderProfile.get(id, fetch_links=True)
        if not rider:
            raise HTTPException(404, "Rider not found")
        
        existing_member = await MemberRoster.find_one(
            MemberRoster.email == rider.email
        )
        if not existing_member:
            new_member = MemberRoster(
                full_name=f"{rider.full_name} {rider.last_name}",   
                body_number=rider.body_number,
                status="active",
                contrib="₱0.00",
                date=datetime.now().strftime("%b %d"),
                email=rider.email or "—",
                contact=rider.contact or "—",
                license_url=rider.license_url,  
                orcr_url=rider.orcr_url, 
            )
            try:
                await new_member.insert()
            except Exception as e:
                raise HTTPException(500, f"Roster creation failed: {str(e)}")

        if rider.user:
            user = rider.user
            user.is_active = True
            await user.save()
        else:
            user = await User.find_one(User.email == rider.email)
            if user:
                user.is_active = True
                await user.save()

        rider.member_status = "approved"
        rider.status = "Active"
        await rider.save()

        return {"message": "Rider Approved, Roster synced, and Mobile Login enabled!"}

    @classmethod
    async def reject(cls, id: str) -> dict:
        rider = await cls.get_or_404(id)
        
        user = await User.find_one(User.email == rider.email)
        if user:
            await user.delete()

        await rider.delete()
        return {"message": "Rider application rejected and account cleared."}
    
class RosterController(BaseController):
    model = MemberRoster
    
    @classmethod
    async def get_all(cls) -> list:
        items = await MemberRoster.find_all().to_list()  # ← no fetch_links
        return [serialize(i) for i in items]
    
    @classmethod
    async def create(cls, data) -> dict:
        await MemberRoster(**data.dict()).insert()
        return {"message": "Member added to roster"}
    
    @classmethod
    async def update(cls, id: str, data) -> dict:
        member = await cls.get_or_404(id)
        for k, v, in data.dict(exclude_unset=True).items():
            setattr(member, k, v)
        await member.save()
        return {"message": "Member record updated"}

class ContributionController(BaseController):
    model = Contribution_Or_Butaw
    
    @classmethod
    async def create(cls, data) -> dict:
        await Contribution_Or_Butaw(**data.dict()).insert()  
        return {"message": "Contribution recorded successfully"}
    
    @classmethod
    async def update(cls, id: str, data) -> dict:
        record = await cls.get_or_404(id)
        for k, v, in data.dict(exclude_unset=True).items():
            setattr(record, k, v)
        await record.save()
        return {"message": "Record Update"}
    
class AnnouncementController(BaseController):
    model = Announcement

    @classmethod
    async def create(cls, data) -> dict:
        await Announcement(**data.dict()).insert()
        return {"message": "Announcement posted!"}

    @classmethod
    async def update(cls, id: str, data) -> dict:
        announcement = await cls.get_or_404(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(announcement, k, v)
        await announcement.save()
        return {"message": "Updated"}
    
class LostFoundController(BaseController):
    model = LostFound

    @classmethod
    async def create(cls, data) -> dict:
        await LostFound(**data.dict()).insert()
        return {"message": "Item posted"}

    @classmethod
    async def update(cls, id: str, data) -> dict:
        item = await cls.get_or_404(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(item, k, v)
        await item.save()
        return {"message": "Item updated"}


class FareController(BaseController):
    model = Fare

    @classmethod
    async def create(cls, data) -> dict:
        await Fare(**data.dict()).insert()
        return {"message": "Fare created"}

    @classmethod
    async def update(cls, id: str, data) -> dict:
        fare = await cls.get_or_404(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(fare, k, v)
        await fare.save()
        return {"message": "Fare updated"}


class CodingController(BaseController):
    model = CodingSchedule

    @classmethod
    async def create(cls, data) -> dict:
        await CodingSchedule(**data.dict()).insert()
        return {"message": "Coding added"}

    @classmethod
    async def update(cls, id: str, data) -> dict:
        coding = await cls.get_or_404(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(coding, k, v)
        await coding.save()
        return {"message": "Coding updated"}


class OfficerController(BaseController):
    model = Officer

    @classmethod
    async def create(cls, data) -> dict:
        await Officer(**data.dict()).insert()
        return {"message": "Officer added"}

    @classmethod
    async def update(cls, id: str, data) -> dict:
        officer = await cls.get_or_404(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(officer, k, v)
        await officer.save()
        return {"message": "Officer updated"}


class ViolationController(BaseController):
    model = Violation

    @classmethod
    async def create(cls, data) -> dict:
        await Violation(**data.dict()).insert()
        return {"message": "Violation recorded"}

    @classmethod
    async def update(cls, id: str, data) -> dict:
        item = await cls.get_or_404(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(item, k, v)
        await item.save()
        return {"message": "Violation updated"}