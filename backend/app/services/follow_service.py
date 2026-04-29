from sqlalchemy.orm import Session
from app.models.follow import Follow
from app.models.user import User
from app.services.notification_service import NotificationService


class FollowService:
    @staticmethod
    def follow_user(db: Session, follower_id: int, following_id: int):
        if follower_id == following_id:
            return None
        
        existing = db.query(Follow).filter(
            Follow.follower_id == follower_id, Follow.following_id == following_id
        ).first()
        
        if existing:
            return None
        
        follow = Follow(follower_id=follower_id, following_id=following_id)
        db.add(follow)
        db.commit()
        
        NotificationService.create_follow_notification(db, following_id, follower_id)
        
        return {"message": "Successfully followed user"}

    @staticmethod
    def unfollow_user(db: Session, follower_id: int, following_id: int):
        follow = db.query(Follow).filter(
            Follow.follower_id == follower_id, Follow.following_id == following_id
        ).first()
        
        if follow:
            db.delete(follow)
            db.commit()
            return {"message": "Successfully unfollowed user"}
        
        return None

    @staticmethod
    def get_followers(db: Session, user_id: int, skip: int = 0, limit: int = 20):
        follows = (
            db.query(Follow)
            .filter(Follow.following_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for f in follows:
            user = db.query(User).filter(User.id == f.follower_id).first()
            if user:
                profile = user.profile
                result.append({
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "is_active": user.is_active,
                    "is_private": user.is_private,
                    "created_at": user.created_at,
                    "profile": {
                        "full_name": profile.full_name if profile else None,
                        "bio": profile.bio if profile else None,
                        "website": profile.website if profile else None,
                        "profile_picture_url": profile.profile_picture_url if profile else None,
                        "phone": profile.phone if profile else None,
                    } if profile else None,
                })
        
        return result

    @staticmethod
    def get_following(db: Session, user_id: int, skip: int = 0, limit: int = 20):
        follows = (
            db.query(Follow)
            .filter(Follow.follower_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for f in follows:
            user = db.query(User).filter(User.id == f.following_id).first()
            if user:
                profile = user.profile
                result.append({
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "is_active": user.is_active,
                    "is_private": user.is_private,
                    "created_at": user.created_at,
                    "profile": {
                        "full_name": profile.full_name if profile else None,
                        "bio": profile.bio if profile else None,
                        "website": profile.website if profile else None,
                        "profile_picture_url": profile.profile_picture_url if profile else None,
                        "phone": profile.phone if profile else None,
                    } if profile else None,
                })
        
        return result

    @staticmethod
    def is_following(db: Session, follower_id: int, following_id: int):
        return (
            db.query(Follow)
            .filter(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
            )
            .first()
            is not None
        )