from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # user or admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    profile_photo = Column(String(255), nullable=True)
    
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    
    doc_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    original_text = Column(Text, nullable=False)
    domain = Column(String(50))  # news, research, legal, general
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="documents")
    summaries = relationship("Summary", back_populates="document", cascade="all, delete-orphan")

class Summary(Base):
    __tablename__ = "summaries"
    
    summary_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("documents.doc_id"), nullable=False)
    model_version = Column(String(50), default="t5-base-v1")
    summary_text = Column(Text, nullable=False)
    rouge_1_score = Column(Float, default=0.0)
    rouge_2_score = Column(Float, default=0.0)
    rouge_l_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    document = relationship("Document", back_populates="summaries")
    feedbacks = relationship("Feedback", back_populates="summary", cascade="all, delete-orphan")
    explanations = relationship("Explanation", back_populates="summary", cascade="all, delete-orphan")

class Feedback(Base):
    __tablename__ = "feedback"
    
    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    summary_id = Column(Integer, ForeignKey("summaries.summary_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    corrected_summary = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    used_for_training = Column(Boolean, default=False)
    
    summary = relationship("Summary", back_populates="feedbacks")
    user = relationship("User", back_populates="feedbacks")

class Explanation(Base):
    __tablename__ = "explanations"
    
    explanation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    summary_id = Column(Integer, ForeignKey("summaries.summary_id"), nullable=False)
    sentence_importance = Column(Text)  # JSON string of sentence scores
    attention_weights = Column(Text)  # JSON string of attention weights
    highlighted_words = Column(Text)  # JSON string of important words
    
    summary = relationship("Summary", back_populates="explanations")
