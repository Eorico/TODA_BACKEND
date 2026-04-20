from beanie import Document
from datetime import datetime
from typing import Optional

class Announcement(Document):
    type: str = "General" 
    title: str
    body: str
    author: str = "Admin"
    created_at : datetime = datetime.utcnow()

    class Settings: 
        name = "announcements"