from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PostMediaResponse(BaseModel):
    id: int
    media_url: str
    thumbnail_url: Optional[str] = None
    media_type: str
    order: int

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    author_id: int
    author_username: str
    author_profile_pic: Optional[str] = None
    caption: Optional[str] = None
    location: Optional[str] = None
    media: List[PostMediaResponse] = []
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    caption: Optional[str] = None
    location: Optional[str] = None


class CommentResponse(BaseModel):
    id: int
    post_id: int
    author_id: int
    author_username: str
    author_profile_pic: Optional[str] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str


class LikeResponse(BaseModel):
    post_id: int
    likes_count: int
    is_liked: bool