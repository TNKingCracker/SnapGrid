from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.message import MessageCreate
from app.services.message_service import MessageService
from app.services.follow_service import FollowService
from app.api.v1.endpoints.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/conversations")
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all conversations."""
    return MessageService.get_conversations(db, current_user.id)


@router.get("/{user_id}")
def get_messages_with_user(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get messages with a specific user."""
    conversation = MessageService.get_or_create_conversation(db, current_user.id, user_id)
    return MessageService.get_messages(db, conversation.id, current_user.id, skip, limit)


@router.post("/{user_id}")
def send_message(
    user_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send message to a user."""
    conversation = MessageService.get_or_create_conversation(db, current_user.id, user_id)
    return MessageService.send_message(
        db,
        conversation.id,
        current_user.id,
        message_data.content,
        message_data.media_url,
    )


@router.get("/conversations/{conversation_id}")
def get_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get messages in a conversation."""
    return MessageService.get_messages(db, conversation_id, current_user.id, skip, limit)