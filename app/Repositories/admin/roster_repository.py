from app.Models.admin.roster_model import MemberRoster
from app.Repositories.base_repository import BaseRepository

class RosterRepository(BaseRepository):
    model = MemberRoster

    async def delete_by_email(self, email: str) -> dict:
        entry = await MemberRoster.find_one(
            MemberRoster.email == email, fetch_links=False
        )
        if entry:
            await entry.delete()
        return {"message": "Roster entry removed."}
    
    async def delete_by_email(self, email: str) -> None:
        entry = await MemberRoster.find_one(MemberRoster.email == email, fetch_links=False)
        if entry:
            await entry.delete()