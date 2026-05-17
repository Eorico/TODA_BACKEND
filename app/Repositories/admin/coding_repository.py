# app/Repositories/Admin/CodingRepository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.admin.coding_model import CodingSchedule

class CodingRepository(BaseRepository):
    model = CodingSchedule