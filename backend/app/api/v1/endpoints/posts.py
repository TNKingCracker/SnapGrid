from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.post import PostCreate, CommentCreate, LikeResponse
from app.services.post_service import PostService
from app.services.user_service import AuthService
from app.api.v1.endpoints.deps import get_current_user
from app.models.user import User
from app.utils import save_upload_file, MediaUtils

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/feed")
def get_feed(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get home feed of followed users posts."""
    return PostService.get_feed(db, current_user.id, skip, limit)


@router.get("/user/{user_id}")
def get_user_posts(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get posts by user."""
    return PostService.get_user_posts(db, user_id, skip, limit)


@router.post("", response_model=dict)
async def create_post(
    caption: str = None,
    location: str = None,
    media_type: str = "photo",
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new post."""
    file_path = await save_upload_file(file, "posts")
    
    post_data = PostCreate(caption=caption, location=location) if caption or location else None
    post = PostService.create_post(
        db,
        author_id=current_user.id,
        media_url=file_path,
        media_type=media_type,
        post_data=post_data,
    )
    
    return AuthService.build_post_response(db, post)


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a single post."""
    post = PostService.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return AuthService.build_post_response(db, post)


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a post."""
    result = PostService.delete_post(db, post_id, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or unauthorized",
        )
    return {"message": "Post deleted successfully"}


@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Like or unlike a post."""
    return PostService.like_post(db, post_id, current_user.id)


@router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Unlike a post (alternative endpoint)."""
    return PostService.like_post(db, post_id, current_user.id)


@router.get("/{post_id}/comments")
def get_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Get comments for a post."""
    return PostService.get_comments(db, post_id, skip, limit)


@router.post("/{post_id}/comments")
def add_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add comment to a post."""
    return PostService.add_comment(db, post_id, current_user.id, comment_data.content)


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a comment."""
    result = PostService.delete_comment(db, comment_id, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or unauthorized",
        )
    return {"message": "Comment deleted successfully"}