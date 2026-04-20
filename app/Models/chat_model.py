from beanie import Document, Link
from datetime import datetime
from Models.user_model import User

class Chatroom(Document):
    
    rider: Link[User]
    passenger: Link[User]
    created_at: datetime = datetime .utcnow()

    class Settings: 
        name = "chat_rooms"
