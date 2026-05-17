# app/Services/ChatService.py
from app.Models.chat.chat_model import Chatroom
from app.Models.chat.message_model import Message

class ChatService:
    """Single Responsibility: chat persistence only."""

    @staticmethod
    async def save_message(room_id: str, sender_id: str, message: str) -> Message:
        msg = Message(room_id=room_id, sender_id=sender_id, message=message)
        await msg.insert()
        return msg