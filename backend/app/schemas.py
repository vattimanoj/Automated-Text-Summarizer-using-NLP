from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    user_id: int
    role: str
    created_at: datetime
    is_active: bool
    profile_photo: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Document Schemas
class DocumentCreate(BaseModel):
    original_text: str
    domain: Optional[str] = "general"

class DocumentResponse(BaseModel):
    doc_id: int
    user_id: int
    original_text: str
    domain: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Summary Schemas
class SummaryRequest(BaseModel):
    document_id: int
    max_length: Optional[int] = 256
    min_length: Optional[int] = 50

class SummaryResponse(BaseModel):
    summary_id: int
    doc_id: int
    model_version: str
    summary_text: str
    rouge_1_score: float
    rouge_2_score: float
    rouge_l_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Explanation Schemas
class ExplanationResponse(BaseModel):
    explanation_id: int
    summary_id: int
    sentence_importance: Dict
    attention_weights: Dict
    highlighted_words: Dict
    average_importance_score: float
    explanation_text: str

# Feedback Schemas
class FeedbackCreate(BaseModel):
    summary_id: int
    rating: int  # 1-5
    corrected_summary: Optional[str] = None
    comments: Optional[str] = None

class FeedbackResponse(BaseModel):
    feedback_id: int
    summary_id: int
    user_id: int
    rating: int
    corrected_summary: Optional[str]
    comments: Optional[str]
    created_at: datetime
    used_for_training: bool
    
    class Config:
        from_attributes = True

# Summarize Text Directly
class SummarizeTextRequest(BaseModel):
    text: str
    domain: Optional[str] = "general"
    max_length: Optional[int] = 256
    min_length: Optional[int] = 50

class SummarizeTextResponse(BaseModel):
    summary: str
    explanation: Dict
    document_id: int
    summary_id: int

class HistoryResponse(BaseModel):
    summary_id: Optional[int]
    doc_id: int
    summary_text: Optional[str]
    original_text: str
    domain: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    name: str

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
