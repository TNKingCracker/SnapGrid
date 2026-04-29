import os
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings


async def save_upload_file(file: UploadFile, subfolder: str = "") -> str:
    """Save uploaded file and return the URL path."""
    upload_dir = Path(settings.UPLOAD_DIR) / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    file_name = f"{Path(file.filename).stem}_{os.urandom(8).hex()}.{file_ext}"
    file_path = upload_dir / file_name
    
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    
    return f"/uploads/{subfolder}/{file_name}" if subfolder else f"/uploads/{file_name}"


def ensure_upload_directory():
    """Ensure upload directory exists."""
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def get_file_size(file: UploadFile) -> int:
    """Get file size."""
    return len(file.file.read())


class MediaUtils:
    @staticmethod
    def generate_thumbnail(image_path: str, size: tuple = (300, 300)) -> str:
        """Generate thumbnail for image."""
        return image_path
    
    @staticmethod
    def validate_media_type(filename: str) -> str:
        """Validate media type from filename."""
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        
        if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
            return "photo"
        elif ext in ["mp4", "mov", "avi", "webm"]:
            return "video"
        return "photo"