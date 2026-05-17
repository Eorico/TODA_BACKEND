from beanie import Document
from typing import Optional
 
class CodingSchedule(Document):
    day: str
    bodyRange: str
    time: str
    status: str
    route: str
    effectivity: Optional[str] = None

    class Settings:
        name = "coding_schedule"