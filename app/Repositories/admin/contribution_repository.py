# app/Repositories/Admin/ContributionRepository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.admin.contribution_or_butaw_model import Contribution_Or_Butaw as Contribution
from app.Utils.serializer import Serializer

class ContributionRepository(BaseRepository):
    model = Contribution

    async def find_by_driver_id(self, driver_id: str) -> list:
        docs = await Contribution.find(
            Contribution.driverid == driver_id
        ).sort("-date").to_list()
        return Serializer.serialize_many(docs)

    async def find_by_body_number(self, body_number: str) -> list:
        docs = await Contribution.find(
            Contribution.body_number == body_number
        ).sort("-date").to_list()
        return Serializer.serialize_many(docs)
    
    async def delete_by_driver(self, driver_id: str, body_number: str) -> None:
        await Contribution.find(Contribution.driverid == driver_id).delete()
        if body_number and body_number not in ("---", "—", ""):
            await Contribution.find(Contribution.body_number == body_number).delete()
