from sqlalchemy.orm import Session
from app.models.story import Story, StoryView
from app.models.user import User
from app.schemas.media import StoryCreate
from app.services.notification_service import NotificationService
from datetime import datetime, timedelta


class StoryService:
    @staticmethod
    def create_story(
        db: Session,
        author_id: int,
        media_url: str,
        media_type: str = "photo",
    ):
        story = Story(
            author_id=author_id,
            media_url=media_url,
            media_type=media_type,
        )
        db.add(story)
        db.commit()
        db.refresh(story)
        return story

    @staticmethod
    def get_stories(db: Session, user_id: int):
        from app.models.follow import Follow
        
        following_ids = [
            f.following_id
            for f in db.query(Follow).filter(Follow.follower_id == user_id).all()
        ]
        following_ids.append(user_id)
        
        stories = (
            db.query(Story)
            .filter(Story.author_id.in_(following_ids))
            .filter(Story.created_at > datetime.utcnow() - timedelta(hours=24))
            .order_by(Story.created_at.desc())
            .all()
        )
        
        result = []
        for story in stories:
            author = db.query(User).filter(User.id == story.author_id).first()
            profile = author.profile if author else None
            
            viewed = (
                db.query(StoryView)
                .filter(StoryView.story_id == story.id, StoryView.viewer_id == user_id)
                .first()
                is not None
            )
            
            result.append({
                "id": story.id,
                "author_id": story.author_id,
                "author_username": author.username if author else "Unknown",
                "author_profile_pic": profile.profile_picture_url if profile else None,
                "media_url": story.media_url,
                "thumbnail_url": story.thumbnail_url,
                "media_type": story.media_type,
                "created_at": story.created_at,
                "is_viewed": viewed,
            })
        
        return result

    @staticmethod
    def mark_viewed(db: Session, story_id: int, user_id: int):
        story = db.query(Story).filter(Story.id == story_id).first()
        if not story:
            return None
        
        existing = (
            db.query(StoryView)
            .filter(StoryView.story_id == story_id, StoryView.viewer_id == user_id)
            .first()
        )
        
        if not existing:
            view = StoryView(story_id=story_id, viewer_id=user_id)
            db.add(view)
            db.commit()
        
        views_count = db.query(StoryView).filter(StoryView.story_id == story_id).count()
        return {"story_id": story_id, "views_count": views_count}

    @staticmethod
    def delete_old_stories(db: Session):
        cutoff = datetime.utcnow() - timedelta(hours=24)
        db.query(Story).filter(Story.created_at < cutoff).delete()
        db.commit()