from sqlalchemy.orm import Session
from app.models.user import User, UserProfile
from app.models.post import Post, Like, Comment
from app.models.follow import Follow
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    UserProfileUpdate,
)
from app.schemas.post import PostResponse, CommentResponse
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.config import settings


class UserService:
    @staticmethod
    def register_user(db: Session, user_data: UserRegister):
        existing = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        if existing:
            return None
        
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        
        return user

    @staticmethod
    def authenticate_user(db: Session, user_data: UserLogin):
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def update_profile(db: Session, user_id: int, profile_data: UserProfileUpdate):
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)
        
        if profile_data.full_name is not None:
            profile.full_name = profile_data.full_name
        if profile_data.bio is not None:
            profile.bio = profile_data.bio
        if profile_data.website is not None:
            profile.website = profile_data.website
        if profile_data.phone is not None:
            profile.phone = profile_data.phone
        
        db.commit()
        db.refresh(profile)
        return profile.user

    @staticmethod
    def get_user_stats(db: Session, user_id: int):
        posts_count = db.query(Post).filter(Post.author_id == user_id).count()
        followers_count = db.query(Follow).filter(Follow.following_id == user_id).count()
        following_count = db.query(Follow).filter(Follow.follower_id == user_id).count()
        return {
            "posts_count": posts_count,
            "followers_count": followers_count,
            "following_count": following_count,
        }


class AuthService:
    @staticmethod
    def create_tokens(user_id: int, username: str):
        access_token = create_access_token(data={"sub": str(user_id), "username": username})
        refresh_token = create_refresh_token(data={"sub": str(user_id), "username": username})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def build_user_response(user: User) -> dict:
        profile = user.profile
        return {
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
        }

    @staticmethod
    def build_user_detail_response(db: Session, user: User) -> dict:
        base = AuthService.build_user_response(user)
        stats = UserService.get_user_stats(db, user.id)
        base.update(stats)
        return base

    @staticmethod
    def build_post_response(db: Session, post: Post) -> dict:
        author = post.author
        profile = author.profile if author else None
        return {
            "id": post.id,
            "author_id": post.author_id,
            "author_username": author.username if author else "Unknown",
            "author_profile_pic": profile.profile_picture_url if profile else None,
            "caption": post.caption,
            "location": post.location,
            "media": [
                {
                    "id": m.id,
                    "media_url": m.media_url,
                    "thumbnail_url": m.thumbnail_url,
                    "media_type": m.media_type,
                    "order": m.order,
                }
                for m in post.media
            ],
            "likes_count": len(post.likes),
            "comments_count": len(post.comments),
            "is_liked": False,
            "created_at": post.created_at,
        }

    @staticmethod
    def build_comment_response(db: Session, comment: Comment) -> dict:
        author = comment.author
        profile = author.profile if author else None
        return {
            "id": comment.id,
            "post_id": comment.post_id,
            "author_id": comment.author_id,
            "author_username": author.username if author else "Unknown",
            "author_profile_pic": profile.profile_picture_url if profile else None,
            "content": comment.content,
            "created_at": comment.created_at,
        }