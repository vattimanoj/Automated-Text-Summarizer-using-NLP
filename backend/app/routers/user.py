from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func
import os
import shutil
import uuid
from app.database import get_db
from app.models import User, Document, Summary, Feedback
from app.schemas import UserResponse, UserUpdate, PasswordUpdate
from app.auth import get_current_active_user, get_password_hash, verify_password
from app.utils import validate_password, get_safe_filename

router = APIRouter()

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get statistics for current user"""
    doc_count = db.query(Document).filter(
        Document.user_id == current_user.user_id
    ).count()
    
    summary_count = db.query(Summary).join(Document).filter(
        Document.user_id == current_user.user_id
    ).count()
    
    feedback_count = db.query(Feedback).filter(
        Feedback.user_id == current_user.user_id
    ).count()
    
    avg_rating = db.query(
        sa_func.avg(Feedback.rating)
    ).filter(Feedback.user_id == current_user.user_id).scalar() or 0
    
    return {
        "user_id": current_user.user_id,
        "documents_count": doc_count,
        "summaries_count": summary_count,
        "feedback_count": feedback_count,
        "average_rating": round(float(avg_rating), 2)
    }

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile information"""
    current_user.name = user_update.name
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/change-password")
async def change_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change current user's password"""
    # Validate new password rules
    validate_password(password_data.new_password)
    
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Incorrect current password"
        )
    
    # Update to new password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.post("/upload-photo", response_model=UserResponse)
async def upload_profile_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload and set profile photo for current user"""
    # Create uploads directory if it doesn't exist
    upload_dir = os.path.join("static", "uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
    
    # Sanitize filename
    safe_name = get_safe_filename(file.filename)
    
    # Check file extension
    file_ext = os.path.splitext(safe_name)[1].lower()
    if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and GIF are allowed.")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update user in database
    photo_url = f"/static/uploads/{unique_filename}"
    current_user.profile_photo = photo_url
    db.commit()
    db.refresh(current_user)
    
    return current_user
