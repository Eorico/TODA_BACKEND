# Routes/chat.py
from fastapi import APIRouter, WebSocket, Query
from app.Providers.app_service_provider import chat_controller

router = APIRouter(tags=["Chat"])

@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id:   str,
    user_id:   str,
    token:     str = Query(...),
):
    await chat_controller.handle(websocket, room_id, user_id, token)