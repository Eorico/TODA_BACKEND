# app/Repositories/Admin/FareRepository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.admin.fare_matrix_model import Fare

class FareRepository(BaseRepository):
    model = Fare