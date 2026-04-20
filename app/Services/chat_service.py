from Models.chat_model import Chatroom
from Models.message_model import Message
from Models.user_model import User

async def create_chat_room(rider_id: str, passenger_id: str):
    rider, passenger = await User.get(rider_id), await User.get(passenger_id) 
    
    room = Chatroom(
        rider=rider,
        passenger=passenger
    )
    
    await room.insert()
    
    return room

async def save_message(room_id: str, sender_id: str, message: str):
    room, sender = await Chatroom.get(room_id), await User.get(sender_id) 
    
    msg = Message(
        room=room,
        sender=sender,
        message=message
    )
    
    await msg.insert()
    
    return msg

