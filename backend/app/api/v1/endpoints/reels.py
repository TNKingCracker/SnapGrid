from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.media import ReelCreate
from app.services.reel_service import ReelService
from app.services.user_service import AuthService
from app.api.v1.endpoints.deps import get_current_user
from app.models.user import User
from app.utils import save_upload_file

router = APIRouter(prefix="/reels", tags=["reels"])


@router.get("")
def get_reels(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get reels feed."""
    return ReelService.get_reels(db, current_user.id, skip, limit)


@router.post("", response_model=dict)
async def create_reel(
    caption: str = None,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a new reel."""
    file_path = await save_upload_file(file, "reels")
    reel = ReelService.create_reel(db, current_user.id, file_path, caption)
    
    author = reel.author
    profile = author.profile if author else None
    return {
        "id": reel.id,
        "author_id": reel.author_id,
        "author_username": author.username if author else "Unknown",
        "author_profile_pic": profile.profile_picture_url if profile else None,
        "video_url": reel.video_url,
        "caption": reel.caption,
        "likes_count": 0,
        "comments_count": 0,
        "is_liked": False,
        "created_at": reel.created_at,
    }


@router.post("/{reel_id}/like")
def like_reel(
    reel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Like or unlike a reel."""
    return ReelService.like_reel(db, reel_id, current_user.id)


@router.get("/{reel_id}/comments")
def get_reel_comments(
    reel_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Get comments for a reel."""
    return ReelService.get_reel_comments(db, reel_id, skip, limit)


@router.post("/{reel_id}/comments")
def add_reel_comment(
    reel_id: int,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add comment to a reel."""
    return ReelService.add_reel_comment(db, reel_id, current_user.id, content)