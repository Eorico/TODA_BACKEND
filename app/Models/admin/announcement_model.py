# app/Models/admin/announcement_model.py
from beanie import Document
from datetime import datetime
from pydantic import Field

class Announcement(Document):
    type:       str      = "General"
    title:      str
    body:       str
    author:     str      = "Admin"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    #                             ↑ called fresh on every new document

    class Settings:
        name = "announcements"