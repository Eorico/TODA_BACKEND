from beanie import Document
from datetime import datetime, timezone
from pydantic import Field

class Fare(Document):
    
    base: float
    highway: float
    special: float
    discStudent: float
    discSenior: float
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "fare_list"