from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.ws.chat import chat_manager, websocket_auth
import json

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    user_id = await websocket_auth(websocket)
    if user_id is None:
        return
    
    await chat_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            await chat_manager.send_personal_message(
                {
                    "type": "message",
                    "content": message_data.get("content"),
                    "sender_id": user_id,
                },
                user_id,
            )
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)