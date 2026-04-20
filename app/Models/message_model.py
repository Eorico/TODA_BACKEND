from beanie import Document, Link 
from datetime import datetime
from Models.user_model import User
from Models.chat_model import Chatroom


class Message(Document):

    room: Link[Chatroom]
    sender: Link[User]
    messange: str 
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "messages"