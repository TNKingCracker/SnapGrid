from sqlalchemy.orm import Session
from app.models.reel import Reel, ReelLike, ReelComment
from app.models.user import User
from datetime import datetime
from app.services.notification_service import NotificationService


class ReelService:
    @staticmethod
    def create_reel(
        db: Session,
        author_id: int,
        video_url: str,
        caption: str = None,
        thumbnail_url: str = None,
    ):
        reel = Reel(
            author_id=author_id,
            video_url=video_url,
            caption=caption,
            thumbnail_url=thumbnail_url,
        )
        db.add(reel)
        db.commit()
        db.refresh(reel)
        return reel

    @staticmethod
    def get_reels(db: Session, user_id: int = None, skip: int = 0, limit: int = 20):
        reels = (
            db.query(Reel)
            .order_by(Reel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for reel in reels:
            author = db.query(User).filter(User.id == reel.author_id).first()
            profile = author.profile if author else None
            
            is_liked = False
            if user_id:
                is_liked = (
                    db.query(ReelLike)
                    .filter(ReelLike.reel_id == reel.id, ReelLike.user_id == user_id)
                    .first()
                    is not None
                )
            
            result.append({
                "id": reel.id,
                "author_id": reel.author_id,
                "author_username": author.username if author else "Unknown",
                "author_profile_pic": profile.profile_picture_url if profile else None,
                "video_url": reel.video_url,
                "thumbnail_url": reel.thumbnail_url,
                "caption": reel.caption,
                "likes_count": len(reel.likes),
                "comments_count": len(reel.comments),
                "is_liked": is_liked,
                "created_at": reel.created_at,
            })
        
        return result

    @staticmethod
    def like_reel(db: Session, reel_id: int, user_id: int):
        reel = db.query(Reel).filter(Reel.id == reel_id).first()
        if not reel:
            return None
        
        existing = db.query(ReelLike).filter(
            ReelLike.reel_id == reel_id, ReelLike.user_id == user_id
        ).first()
        
        if existing:
            db.delete(existing)
            db.commit()
            is_liked = False
        else:
            like = ReelLike(reel_id=reel_id, user_id=user_id)
            db.add(like)
            db.commit()
            is_liked = True
            
            if reel.author_id != user_id:
                NotificationService.create_like_notification(
                    db, reel_id, reel.author_id, user_id
                )
        
        likes_count = db.query(ReelLike).filter(ReelLike.reel_id == reel_id).count()
        return {"reel_id": reel_id, "likes_count": likes_count, "is_liked": is_liked}

    @staticmethod
    def get_reel_comments(db: Session, reel_id: int, skip: int = 0, limit: int = 20):
        comments = (
            db.query(ReelComment)
            .filter(ReelComment.reel_id == reel_id)
            .order_by(ReelComment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": c.id,
                "reel_id": c.reel_id,
                "author_id": c.author_id,
                "author_username": c.author.username if c.author else "Unknown",
                "author_profile_pic": c.author.profile.profile_picture_url if c.author and c.author.profile else None,
                "content": c.content,
                "created_at": c.created_at,
            }
            for c in comments
        ]

    @staticmethod
    def add_reel_comment(db: Session, reel_id: int, author_id: int, content: str):
        reel = db.query(Reel).filter(Reel.id == reel_id).first()
        if not reel:
            return None
        
        comment = ReelComment(reel_id=reel_id, author_id=author_id, content=content)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        return {
            "id": comment.id,
            "reel_id": comment.reel_id,
            "author_id": comment.author_id,
            "author_username": comment.author.username if comment.author else "Unknown",
            "author_profile_pic": comment.author.profile.profile_picture_url if comment.author and comment.author.profile else None,
            "content": comment.content,
            "created_at": comment.created_at,
        }