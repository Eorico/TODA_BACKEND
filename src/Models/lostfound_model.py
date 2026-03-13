from beanie import Document
from datetime import datetime

class LostFound(Document):

    item_name: str
    description: str
    driver_name: str
    tricycle_number: str
    reported_at: datetime = datetime.utcnow()

    class Settings:
        name = "lost_found"