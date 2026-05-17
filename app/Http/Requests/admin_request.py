# app/Http/Requests/AdminRequest.py
from pydantic import BaseModel
from typing import Optional

class DriverUpdateRequest(BaseModel):
    full_name:               str
    last_name:               str = ""
    body_number:             str = "---"
    contact:                 str
    email:                   Optional[str] = None
    address:                 Optional[str] = "Not Specified"
    status:                  Optional[str] = "Active"
    expiration_date_license: Optional[str] = None
    expiration_date_orcr:    Optional[str] = None

class AnnouncementRequest(BaseModel):
    type:   str = "General"
    title:  str
    body:   str
    author: str = "Admin"

class OfficerRequest(BaseModel):
    full_name: str
    mi:        Optional[str] = ""
    last_name: str
    role:      str
    status:    str
    phone:     str
    email:     str
    custom_id: str

class ContributionRequest(BaseModel):
    full_name:   str
    last_name:   str
    body_number: str
    driverid:    str
    amount:      float
    date:        str
    status:      str
    notes:       Optional[str] = None

class LostFoundRequest(BaseModel):
    name:   str
    body:   str
    date:   str
    status: str = "Pending"
    image:  Optional[str] = None

class FareRequest(BaseModel):
    base:        float
    highway:     float
    special:     float
    discStudent: float
    discSenior:  float

class CodingRequest(BaseModel):
    day:         str
    bodyRange:   str
    time:        str
    status:      str
    route:       str
    effectivity: Optional[str] = None

class ViolationRequest(BaseModel):
    driver_id:      str
    driver_name:    str
    body:           str
    date:           str
    violation:      str
    penalty:        str
    penalty_amount: Optional[str] = None

class RosterRequest(BaseModel):
    full_name:               str
    body_number:             Optional[str] = "—"
    status:                  str
    contrib:                 str
    date:                    str
    email:                   Optional[str] = "—"
    contact:                 Optional[str] = "—"
    license_url:             Optional[str] = None
    orcr_url:                Optional[str] = None
    expiration_date_license: Optional[str] = None
    expiration_date_orcr:    Optional[str] = None