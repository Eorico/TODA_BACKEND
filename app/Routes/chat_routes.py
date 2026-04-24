from fastapi import APIRouter, WebSocket
from Controllers.chat_controller import chat_manager

router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)

@router.websocket('/ws/{room_id}/{user_id}')
async def websocket_chat(websocket: WebSocket, room_id: str, user_id: str):
    await chat_manager.handle(room_id, user_id, websocket)