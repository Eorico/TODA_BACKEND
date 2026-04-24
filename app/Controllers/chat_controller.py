from fastapi import WebSocket, WebSocketDisconnect
from Services.chat_service import ChatService

class ChatManager:

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

    async def broadcast(self, room_id: str, message: str):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_text(message)

    async def handle(self, room_id: str, user_id: str, websocket: WebSocket):
        await self.connect(room_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await ChatService.save_message(room_id, user_id, data)
                await self.broadcast(room_id, data)
        except WebSocketDisconnect:
            self.disconnect(room_id, websocket)

chat_manager = ChatManager()