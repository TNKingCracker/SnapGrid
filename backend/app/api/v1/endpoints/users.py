from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import (
    UserResponse,
    UserDetailResponse,
    UserProfileUpdate,
    UserProfileResponse,
)
from app.services.user_service import UserService, AuthService
from app.services.follow_service import FollowService
from app.api.v1.endpoints.deps import get_current_user
from app.models.user import User, UserProfile
from app.utils import save_upload_file
import os

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return AuthService.build_user_response(current_user)


@router.put("/me", response_model=UserResponse)
def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile."""
    user = UserService.update_profile(db, current_user.id, profile_data)
    return AuthService.build_user_response(user)


@router.post("/me/profile-pic", response_model=UserResponse)
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload profile picture."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    file_path = await save_upload_file(file, "profiles")
    profile.profile_picture_url = file_path
    db.commit()
    db.refresh(profile)
    
    return AuthService.build_user_response(current_user)


@router.get("/{user_id}", response_model=UserDetailResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID."""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return AuthService.build_user_detail_response(db, user)


@router.get("/username/{username}", response_model=UserDetailResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Get user by username."""
    user = UserService.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return AuthService.build_user_detail_response(db, user)


@router.get("/{user_id}/followers", response_model=list)
def get_user_followers(user_id: int, db: Session = Depends(get_db)):
    """Get user followers."""
    return FollowService.get_followers(db, user_id)


@router.get("/{user_id}/following", response_model=list)
def get_user_following(user_id: int, db: Session = Depends(get_db)):
    """Get user following."""
    return FollowService.get_following(db, user_id)


@router.post("/{user_id}/follow")
def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Follow a user."""
    result = FollowService.follow_user(db, current_user.id, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not follow user",
        )
    return result


@router.delete("/{user_id}/follow")
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Unfollow a user."""
    result = FollowService.unfollow_user(db, current_user.id, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not unfollow user",
        )
    return result