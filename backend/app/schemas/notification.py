from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    notification_type: str
    actor_id: int
    actor_username: str
    actor_profile_pic: Optional[str] = None
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    message: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    is_read: bool = True