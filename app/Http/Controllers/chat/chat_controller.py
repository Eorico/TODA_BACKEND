# app/Http/Controllers/ChatController.py
from fastapi import WebSocket, WebSocketDisconnect
from app.Services.chat.chat_service import ChatService
from app.Utils.jwt_handler import JwtHandler

class ChatConnectionManager:
    """Single Responsibility: WebSocket connection tracking only."""

    def __init__(self):
        self._rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self._rooms.setdefault(room_id, []).append(ws)

    def disconnect(self, room_id: str, ws: WebSocket) -> None:
        if room_id in self._rooms:
            self._rooms[room_id].remove(ws)

    async def broadcast(self, room_id: str, message: str) -> None:
        for ws in self._rooms.get(room_id, []):
            await ws.send_text(message)


class ChatController:
    def __init__(self, service: ChatService):
        self._service = service
        self._manager = ChatConnectionManager()

    async def handle(
        self,
        websocket: WebSocket,
        room_id:   str,
        user_id:   str,
        token:     str,
    ) -> None:
        payload = JwtHandler.decode(token)
        if payload.get("user_id") != user_id:
            await websocket.close(code=1008)
            return

        await self._manager.connect(room_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await self._service.save_message(room_id, user_id, data)
                await self._manager.broadcast(room_id, data)
        except WebSocketDisconnect:
            self._manager.disconnect(room_id, websocket)