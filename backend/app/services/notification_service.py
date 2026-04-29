from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.user import User
from datetime import datetime


class NotificationService:
    @staticmethod
    def create_like_notification(db: Session, post_id: int, owner_id: int, actor_id: int):
        if owner_id == actor_id:
            return None
        
        notification = Notification(
            user_id=owner_id,
            notification_type="like",
            actor_id=actor_id,
            post_id=post_id,
            message="liked your post",
        )
        db.add(notification)
        db.commit()
        return notification

    @staticmethod
    def create_comment_notification(
        db: Session, post_id: int, comment_id: int, owner_id: int, actor_id: int
    ):
        if owner_id == actor_id:
            return None
        
        notification = Notification(
            user_id=owner_id,
            notification_type="comment",
            actor_id=actor_id,
            post_id=post_id,
            comment_id=comment_id,
            message="commented on your post",
        )
        db.add(notification)
        db.commit()
        return notification

    @staticmethod
    def create_follow_notification(db: Session, owner_id: int, actor_id: int):
        if owner_id == actor_id:
            return None
        
        notification = Notification(
            user_id=owner_id,
            notification_type="follow",
            actor_id=actor_id,
            message="started following you",
        )
        db.add(notification)
        db.commit()
        return notification

    @staticmethod
    def get_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 20):
        notifications = (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for n in notifications:
            actor = db.query(User).filter(User.id == n.actor_id).first()
            actor_profile = actor.profile if actor else None
            result.append({
                "id": n.id,
                "user_id": n.user_id,
                "notification_type": n.notification_type,
                "actor_id": n.actor_id,
                "actor_username": actor.username if actor else "Unknown",
                "actor_profile_pic": actor_profile.profile_picture_url if actor_profile else None,
                "post_id": n.post_id,
                "comment_id": n.comment_id,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at,
            })
        return result

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int):
        notification = (
            db.query(Notification)
            .filter(Notification.id == notification_id, Notification.user_id == user_id)
            .first()
        )
        if notification:
            notification.is_read = True
            db.commit()
            return True
        return False

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int):
        db.query(Notification).filter(
            Notification.user_id == user_id, Notification.is_read == False
        ).update({"is_read": True})
        db.commit()