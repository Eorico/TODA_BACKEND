from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from Services.chat_service import save_message

router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)

active_connections = []

@router.websocket('/ws/{room_id}/{user_id}')
async def websocket_chat(websocket: WebSocket, room_id: str, user_id: str):
    await websocket.accept()
    
    if room_id not in active_connections:
        active_connections[room_id] = []
        
    active_connections[room_id].append(websocket)
    
    socketRun = True
    
    try:
        while socketRun:
            data = await websocket.receive_text()
            await save_message(room_id, user_id, data)
            for connection in active_connections[room_id]:
                await connection.send_text(data)
                
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)