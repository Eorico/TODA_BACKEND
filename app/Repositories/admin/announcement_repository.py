# app/Repositories/admin/announcement_repository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.admin.announcement_model import Announcement
from app.Utils.serializer import Serializer

class AnnouncementRepository(BaseRepository):
    model = Announcement

    async def find_all_sorted(self) -> list:
        # Use field reference instead of string — works across all Beanie versions
        docs = await Announcement.find_all(
            fetch_links=False
        ).sort(-Announcement.created_at).to_list()
        return Serializer.serialize_many(docs)