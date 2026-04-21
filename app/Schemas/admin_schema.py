from pydantic import BaseModel, EmailStr 
from typing import Optional 
from pydantic import BaseModel


class CommentCreateSchema(BaseModel):
    announcement_id: str
    message: str
    
class AnnouncementSchema(BaseModel):
    type: str = "General" 
    title: str
    body: str
    author: str = "Admin"
    
class OfficerSchema(BaseModel):
    fname: str
    mi: Optional[str] = ""
    lname: str
    role: str
    status: str
    phone: str
    email: str
    custom_id: str
    
class ContributionSchema(BaseModel):
    fname: str
    lname: str
    body: str
    driverid: str
    amount: float
    period: str
    date: str
    status: str
    notes: Optional[str] = None
    
class LostFoundSchema(BaseModel):
    name: str
    body: str
    date: str         
    status: str = "Pending"
    image: Optional[str] = None 
    
class FareSchema(BaseModel):
    base: float
    highway: float  
    special: float
    discStudent: float
    discSenior: float
    
class CodingSchema(BaseModel):
    day: str
    bodyRange: str
    time: str
    status: str
    route: str
    effectivity: Optional[str] = None
    
class ViolationSchema(BaseModel):
    driver_id: str       
    driver_name: str       
    body: str               
    date: str             
    violation: str           
    penalty: str            
    penalty_amount: Optional[str] = None  
    
class MemberRosterSchema(BaseModel):
    name: str
    id: str
    status: str
    contrib: str
    date: str