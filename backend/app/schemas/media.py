from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StoryResponse(BaseModel):
    id: int
    author_id: int
    author_username: str
    author_profile_pic: Optional[str] = None
    media_url: str
    thumbnail_url: Optional[str] = None
    media_type: str
    created_at: datetime
    is_viewed: bool = False

    class Config:
        from_attributes = True


class StoryCreate(BaseModel):
    media_type: str = "photo"


class StoryViewResponse(BaseModel):
    story_id: int
    views_count: int


class ReelResponse(BaseModel):
    id: int
    author_id: int
    author_username: str
    author_profile_pic: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class ReelCreate(BaseModel):
    caption: Optional[str] = None


class ReelCommentResponse(BaseModel):
    id: int
    reel_id: int
    author_id: int
    author_username: str
    author_profile_pic: Optional[str] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReelLikeResponse(BaseModel):
    reel_id: int
    likes_count: int
    is_liked: bool