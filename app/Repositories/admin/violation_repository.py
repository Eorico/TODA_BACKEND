from app.Repositories.base_repository import BaseRepository
from app.Models.admin.violation_model import Violation
from app.Utils.serializer import Serializer

class ViolationRepository(BaseRepository):
    model = Violation

    async def find_by_driver_id(self, driver_id: str) -> list:
        """Fetch only violations belonging to this specific driver ID.
        No name matching — names can collide between drivers."""
        docs = await Violation.find(
            Violation.driver_id == driver_id,
            fetch_links=False
        ).sort(-Violation.created_at).to_list()
        return Serializer.serialize_many(docs)

    # Kept for admin use only — finds by either ID or name
    async def find_by_driver_id_or_name(
        self, driver_id: str, full_name: str
    ) -> list:
        by_id = await Violation.find(
            Violation.driver_id == driver_id,
            fetch_links=False
        ).to_list()

        by_name = await Violation.find(
            Violation.driver_name == full_name,
            fetch_links=False
        ).to_list()

        seen   = set()
        merged = []
        for v in by_id + by_name:
            vid = str(v.id)
            if vid not in seen:
                seen.add(vid)
                merged.append(v)

        return Serializer.serialize_many(merged)

    async def delete_by_driver(self, driver_id: str, body_number: str) -> None:
        await Violation.find(Violation.driver_id == driver_id).delete()
        if body_number and body_number not in ("---", "—", ""):
            await Violation.find(Violation.body == body_number).delete()