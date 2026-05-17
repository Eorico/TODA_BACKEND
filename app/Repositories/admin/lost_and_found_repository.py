# app/Repositories/Admin/LostFoundRepository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.admin.lostfound_model import LostFound

class LostFoundRepository(BaseRepository):
    model = LostFound