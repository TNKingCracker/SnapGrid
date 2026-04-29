from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.message import Conversation, Message
from app.models.user import User
from app.models.follow import Follow
from datetime import datetime


class MessageService:
    @staticmethod
    def get_or_create_conversation(db: Session, user1_id: int, user2_id: int):
        conversation = (
            db.query(Conversation)
            .filter(
                or_(
                    (Conversation.user1_id == user1_id) & (Conversation.user2_id == user2_id),
                    (Conversation.user1_id == user2_id) & (Conversation.user2_id == user1_id),
                )
            )
            .first()
        )
        
        if not conversation:
            conversation = Conversation(user1_id=user1_id, user2_id=user2_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        return conversation

    @staticmethod
    def get_conversations(db: Session, user_id: int):
        conversations = (
            db.query(Conversation)
            .filter((Conversation.user1_id == user_id) | (Conversation.user2_id == user_id))
            .order_by(Conversation.updated_at.desc())
            .all()
        )
        
        result = []
        for c in conversations:
            other_id = c.user2_id if c.user1_id == user_id else c.user1_id
            other_user = db.query(User).filter(User.id == other_id).first()
            
            if not other_user:
                continue
            
            profile = other_user.profile
            
            unread_count = (
                db.query(Message)
                .filter(
                    Message.conversation_id == c.id,
                    Message.sender_id != user_id,
                    Message.is_read == False,
                )
                .count()
            )
            
            result.append({
                "id": c.id,
                "other_user_id": other_id,
                "other_user_username": other_user.username,
                "other_user_profile_pic": profile.profile_picture_url if profile else None,
                "last_message": c.last_message,
                "last_message_at": c.last_message_at,
                "unread_count": unread_count,
            })
        
        return result

    @staticmethod
    def get_messages(db: Session, conversation_id: int, user_id: int, skip: int = 0, limit: int = 50):
        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .filter(
                (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
            )
            .first()
        )
        
        if not conversation:
            return []
        
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for m in messages:
            sender = db.query(User).filter(User.id == m.sender_id).first()
            result.append({
                "id": m.id,
                "conversation_id": m.conversation_id,
                "sender_id": m.sender_id,
                "sender_username": sender.username if sender else "Unknown",
                "content": m.content,
                "media_url": m.media_url,
                "is_read": m.is_read,
                "created_at": m.created_at,
            })
        
        db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.is_read == False,
        ).update({"is_read": True})
        db.commit()
        
        return result

    @staticmethod
    def send_message(
        db: Session,
        conversation_id: int,
        sender_id: int,
        content: str = None,
        media_url: str = None,
    ):
        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .filter(
                (Conversation.user1_id == sender_id) | (Conversation.user2_id == sender_id)
            )
            .first()
        )
        
        if not conversation:
            return None
        
        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
            media_url=media_url,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        
        conversation.last_message = content or "Sent a photo"
        conversation.last_message_at = datetime.utcnow()
        db.commit()
        
        sender = db.query(User).filter(User.id == sender_id).first()
        return {
            "id": message.id,
            "conversation_id": message.conversation_id,
            "sender_id": message.sender_id,
            "sender_username": sender.username if sender else "Unknown",
            "content": message.content,
            "media_url": message.media_url,
            "is_read": message.is_read,
            "created_at": message.created_at,
        }