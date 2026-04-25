from fastapi import APIRouter, WebSocket, Query
from Controllers.chat_controller import chat_manager
from jose import jwt, JWTError
import os

router = APIRouter(
    tags=['Chat']
)

SECRET_KEY = os.getenv("SECRET KEY")
ALGORITHM = "HS256"

@router.websocket('/ws/{room_id}/{user_id}')
async def websocket_chat(
    websocket: WebSocket, 
    room_id: str, 
    user_id: str,
    token: str = Query(...)
    ):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("user_id") != user_id:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return
    
    await chat_manager.handle(room_id, user_id, websocket)