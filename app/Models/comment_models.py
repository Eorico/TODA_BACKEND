from beanie import Document, Link
from datetime import datetime
from Models.user_model import User
from Models.announcement_model import Announcement

class Comment(Document):
    user: Link[User]
    announcement: Link[Announcement]
    message: str
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "comments"