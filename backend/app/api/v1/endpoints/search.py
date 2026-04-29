from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.models.post import Post
from app.services.user_service import AuthService
from app.api.v1.endpoints.deps import get_current_user

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search_users(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Search users by username or name."""
    users = db.query(User).filter(
        User.username.ilike(f"%{q}%")
    ).limit(20).all()
    
    return [
        AuthService.build_user_response(u)
        for u in users
    ]


@router.get("/posts")
def search_posts(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Search posts by caption or hashtags."""
    posts = db.query(Post).filter(
        Post.caption.ilike(f"%{q}%")
    ).order_by(Post.created_at.desc()).limit(20).all()
    
    return [AuthService.build_post_response(db, p) for p in posts]


@router.get("/explore")
def explore_posts(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Explore posts from all users."""
    from app.services.user_service import AuthService
    from app.services.post_service import PostService
    
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return [AuthService.build_post_response(db, p) for p in posts]