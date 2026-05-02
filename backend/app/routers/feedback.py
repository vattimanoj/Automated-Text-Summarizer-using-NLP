from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Summary, Feedback
from app.schemas import FeedbackCreate, FeedbackResponse
from app.auth import get_current_active_user
from app.config import settings
import logging
from app.ml_model.auto_training import trigger_auto_training_if_needed

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create feedback for a summary"""
    # Validate rating
    if feedback_data.rating < 1 or feedback_data.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    # Verify summary exists
    summary = db.query(Summary).filter(
        Summary.summary_id == feedback_data.summary_id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    # Create feedback
    feedback = Feedback(
        summary_id=feedback_data.summary_id,
        user_id=current_user.user_id,
        rating=feedback_data.rating,
        corrected_summary=feedback_data.corrected_summary,
        comments=feedback_data.comments,
        used_for_training=False
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    # Check if we should trigger auto-training
    if settings.AUTO_TRAINING_ENABLED and feedback_data.rating >= settings.MIN_FEEDBACK_RATING:
        try:
            # This will run in background
            trigger_auto_training_if_needed(db, feedback)
        except Exception as e:
            logger.error(f"Error in auto-training trigger: {e}")
            # Don't fail the request if training fails
    
    return feedback

@router.get("/summary/{summary_id}", response_model=list[FeedbackResponse])
async def get_feedback_for_summary(
    summary_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all feedback for a summary"""
    feedbacks = db.query(Feedback).filter(
        Feedback.summary_id == summary_id
    ).order_by(Feedback.created_at.desc()).all()
    
    return feedbacks

@router.get("/user", response_model=list[FeedbackResponse])
async def get_user_feedback(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all feedback by current user"""
    feedbacks = db.query(Feedback).filter(
        Feedback.user_id == current_user.user_id
    ).order_by(Feedback.created_at.desc()).all()
    
    return feedbacks
