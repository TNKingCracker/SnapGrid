from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Reel(Base):
    __tablename__ = "reels"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    video_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    author = relationship("User", back_populates="reels")
    likes = relationship("ReelLike", back_populates="reel", cascade="all, delete-orphan")
    comments = relationship("ReelComment", back_populates="reel", cascade="all, delete-orphan")


class ReelLike(Base):
    __tablename__ = "reel_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reel_id = Column(Integer, ForeignKey("reels.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    reel = relationship("Reel", back_populates="likes")


class ReelComment(Base):
    __tablename__ = "reel_comments"

    id = Column(Integer, primary_key=True, index=True)
    reel_id = Column(Integer, ForeignKey("reels.id"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    reel = relationship("Reel", back_populates="comments")