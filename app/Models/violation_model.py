from beanie import Document
from typing import Optional
from datetime import datetime, timezone
from pydantic import Field

class Violation(Document):
    driver_id: str          
    driver_name: str       
    body: str              
    date: str           
    violation: str       
    penalty: str             
    penalty_amount: Optional[str] = None   
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "violations"