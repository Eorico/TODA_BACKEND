# app/Repositories/Admin/OfficerRepository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.admin.officer_model import Officer

class OfficerRepository(BaseRepository):
    model = Officer