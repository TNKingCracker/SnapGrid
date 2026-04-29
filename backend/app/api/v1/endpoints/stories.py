from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.media import StoryCreate
from app.services.story_service import StoryService
from app.services.user_service import AuthService
from app.api.v1.endpoints.deps import get_current_user
from app.models.user import User
from app.utils import save_upload_file

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("/following")
def get_stories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get stories from followed users."""
    return StoryService.get_stories(db, current_user.id)


@router.post("", response_model=dict)
async def create_story(
    media_type: str = "photo",
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new story."""
    file_path = await save_upload_file(file, "stories")
    story = StoryService.create_story(db, current_user.id, file_path, media_type)
    
    author = story.author
    profile = author.profile if author else None
    return {
        "id": story.id,
        "author_id": story.author_id,
        "author_username": author.username if author else "Unknown",
        "author_profile_pic": profile.profile_picture_url if profile else None,
        "media_url": story.media_url,
        "media_type": story.media_type,
        "created_at": story.created_at,
    }


@router.post("/{story_id}/view")
def view_story(
    story_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a story as viewed."""
    return StoryService.mark_viewed(db, story_id, current_user.id)