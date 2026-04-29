from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
from app.services.message_service import MessageService
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)


chat_manager = ConnectionManager()


async def websocket_auth(websocket: WebSocket) -> int:
    """Authenticate WebSocket connection."""
    from app.core.security import decode_token, get_current_user_id
    
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001)
        return None
    
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        await websocket.close(code=4001)
        return None
    
    try:
        user_id = get_current_user_id(token)
        return user_id
    except:
        await websocket.close(code=4001)
        return None