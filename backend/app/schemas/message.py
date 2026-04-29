from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConversationResponse(BaseModel):
    id: int
    other_user_id: int
    other_user_username: str
    other_user_profile_pic: Optional[str] = None
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int = 0

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    sender_username: str
    content: Optional[str] = None
    media_url: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None


class ChatMessage(BaseModel):
    message: str


class WSMessage(BaseModel):
    type: str
    conversation_id: Optional[int] = None
    sender_id: Optional[int] = None
    content: Optional[str] = None
    media_url: Optional[str] = None
    created_at: Optional[datetime] = None