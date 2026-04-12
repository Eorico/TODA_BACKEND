from beanie import Document
from datetime import datetime

class LostFound(Document):

    item_name: str
    image_url: str
    tricycle_body_number: str
    date_found: datetime

    class Settings:
        name = "lost_found"