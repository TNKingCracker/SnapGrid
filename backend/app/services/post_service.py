from sqlalchemy.orm import Session
from app.models.post import Post, PostMedia, Like, Comment
from app.models.user import User
from app.models.follow import Follow
from app.schemas.post import PostCreate, CommentCreate
from app.services.user_service import AuthService
from app.services.notification_service import NotificationService
import os
import shutil
from datetime import datetime


class PostService:
    @staticmethod
    def create_post(
        db: Session,
        author_id: int,
        media_url: str,
        media_type: str = "photo",
        post_data: PostCreate = None,
    ):
        post = Post(author_id=author_id)
        if post_data:
            post.caption = post_data.caption
            post.location = post_data.location
            
            import re
            hashtags = re.findall(r"#\w+", post.caption or "")
            post.hashtags = hashtags
        
        db.add(post)
        db.commit()
        db.refresh(post)
        
        media = PostMedia(
            post_id=post.id,
            media_url=media_url,
            media_type=media_type,
            order=0,
        )
        db.add(media)
        db.commit()
        
        return post

    @staticmethod
    def get_post(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: int):
        post = PostService.get_post(db, post_id)
        if not post or post.author_id != user_id:
            return False
        
        for media in post.media:
            if media.media_url:
                try:
                    if os.path.exists(media.media_url):
                        os.remove(media.media_url)
                except:
                    pass
        
        db.delete(post)
        db.commit()
        return True

    @staticmethod
    def get_feed(db: Session, user_id: int, skip: int = 0, limit: int = 20):
        following_ids = [
            f.following_id
            for f in db.query(Follow).filter(Follow.follower_id == user_id).all()
        ]
        following_ids.append(user_id)
        
        posts = (
            db.query(Post)
            .filter(Post.author_id.in_(following_ids))
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return [AuthService.build_post_response(db, p) for p in posts]

    @staticmethod
    def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 20):
        posts = (
            db.query(Post)
            .filter(Post.author_id == user_id)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [AuthService.build_post_response(db, p) for p in posts]

    @staticmethod
    def like_post(db: Session, post_id: int, user_id: int):
        post = PostService.get_post(db, post_id)
        if not post:
            return None
        
        existing = db.query(Like).filter(
            Like.post_id == post_id, Like.user_id == user_id
        ).first()
        
        if existing:
            db.delete(existing)
            db.commit()
            is_liked = False
        else:
            like = Like(post_id=post_id, user_id=user_id)
            db.add(like)
            db.commit()
            is_liked = True
            
            if post.author_id != user_id:
                NotificationService.create_like_notification(
                    db, post_id, post.author_id, user_id
                )
        
        likes_count = db.query(Like).filter(Like.post_id == post_id).count()
        return {"post_id": post_id, "likes_count": likes_count, "is_liked": is_liked}

    @staticmethod
    def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 20):
        comments = (
            db.query(Comment)
            .filter(Comment.post_id == post_id)
            .order_by(Comment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": c.id,
                "post_id": c.post_id,
                "author_id": c.author_id,
                "author_username": c.author.username if c.author else "Unknown",
                "author_profile_pic": c.author.profile.profile_picture_url if c.author and c.author.profile else None,
                "content": c.content,
                "created_at": c.created_at,
            }
            for c in comments
        ]

    @staticmethod
    def add_comment(db: Session, post_id: int, author_id: int, content: str):
        post = PostService.get_post(db, post_id)
        if not post:
            return None
        
        comment = Comment(post_id=post_id, author_id=author_id, content=content)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        if post.author_id != author_id:
            NotificationService.create_comment_notification(
                db, post_id, comment.id, post.author_id, author_id
            )
        
        author = comment.author
        return {
            "id": comment.id,
            "post_id": comment.post_id,
            "author_id": comment.author_id,
            "author_username": author.username if author else "Unknown",
            "author_profile_pic": author.profile.profile_picture_url if author and author.profile else None,
            "content": comment.content,
            "created_at": comment.created_at,
        }

    @staticmethod
    def delete_comment(db: Session, comment_id: int, user_id: int):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment or comment.author_id != user_id:
            return False
        
        db.delete(comment)
        db.commit()
        return True