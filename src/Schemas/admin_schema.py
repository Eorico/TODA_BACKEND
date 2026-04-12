from pydantic import BaseModel, EmailStr 
from typing import Optional 
from pydantic import BaseModel


class CommentCreateSchema(BaseModel):
    announcement_id: str
    message: str
    
class AnnouncementSchema(BaseModel):
    title: str
    description: str
    
class OfficerSchema(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    officer_id: str
    role: str
    duty_status: str
    phone: str
    email: EmailStr
    
class ContributionSchema(BaseModel):
    first_name: str
    last_name: str
    body_number: str
    driver_id: str
    amount: float
    period_date: str
    date_paid: str
    payment_status: str
    notes: Optional[str] = None
    
class LostFoundSchema(BaseModel):
    item_name: str
    image_url: str
    body_number: str
    date_found: str
    
class FareSchema(BaseModel):
    base_fare: float
    town_proper: float
    special_trip: float
    
class CodingSchema(BaseModel):
    date: str
    day: str
    last_digit: int