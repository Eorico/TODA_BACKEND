from beanie import Document
from datetime import datetime

class Announcement(Document):
    title: str 
    description: str
    created_at : datetime = datetime.utcnow()

    class Settings: 
        name = "announcements"