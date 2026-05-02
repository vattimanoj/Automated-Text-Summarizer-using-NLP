import torch
from sqlalchemy.orm import Session
from app.models import Feedback, Summary, Document
from app.config import settings
import logging
from typing import List
import threading
import os
from app.ml_model.dataset_collector import DatasetCollector
from app.ml_model.model_trainer import ModelTrainer

logger = logging.getLogger(__name__)

def trigger_auto_training_if_needed(db: Session, new_feedback: Feedback):
    """Trigger auto-training if enough high-quality feedback is available"""
    if not settings.AUTO_TRAINING_ENABLED:
        return
    
    # Count high-quality feedback that hasn't been used for training
    high_quality_feedback = db.query(Feedback).filter(
        Feedback.rating >= settings.MIN_FEEDBACK_RATING,
        Feedback.used_for_training == False
    ).count()
    
    if high_quality_feedback >= settings.BATCH_SIZE_FOR_TRAINING:
        # Run training in background thread
        thread = threading.Thread(
            target=run_incremental_training,
            args=(db,),
            daemon=True
        )
        thread.start()
        logger.info("Auto-training triggered in background")

def run_incremental_training(db: Session):
    """Run incremental fine-tuning using user feedback"""
    try:
        logger.info("Starting incremental training with user feedback...")
        
        csv_path = "./training_data.csv"
        collector = DatasetCollector(csv_path)
        
        # Update CSV with new feedback from database
        collector.update_csv_from_database(db)
        
        # Get all high-quality feedback (including new ones)
        feedbacks = db.query(Feedback).join(Summary).join(Document).filter(
            Feedback.rating >= settings.MIN_FEEDBACK_RATING,
            Feedback.used_for_training == False
        ).all()
        
        if len(feedbacks) < settings.BATCH_SIZE_FOR_TRAINING:
            logger.info(f"Not enough feedback for training. Need {settings.BATCH_SIZE_FOR_TRAINING}, got {len(feedbacks)}")
            return
        
        # Load existing CSV and prepare full training dataset
        df = collector.load_from_csv()
        
        if df.empty:
            logger.error("CSV file is empty. Cannot train.")
            return
        
        # Prepare trainer
        trainer = ModelTrainer()
        
        # Load all data from CSV (including old + new)
        train_texts, train_summaries, val_texts, val_summaries = trainer.load_data(csv_path, train_ratio=0.9)
        
        if not train_texts:
            logger.error("No training data available")
            return
        
        logger.info(f"Training with {len(train_texts)} samples (including {len(feedbacks)} new feedback samples)")
        
        # Fine-tune model (fewer epochs for incremental training)
        results = trainer.train(
            train_texts=train_texts,
            train_summaries=train_summaries,
            val_texts=val_texts,
            val_summaries=val_summaries,
            epochs=2,  # Fewer epochs for incremental training
            batch_size=2,
            learning_rate=1e-5,  # Lower learning rate for fine-tuning
            target_accuracy=0.96
        )
        
        if results:
            logger.info(f"Incremental training completed successfully!")
            logger.info(f"ROUGE-1: {results['rouge1']:.4f}")
            logger.info(f"Average ROUGE: {results['avg_rouge']:.4f}")
            
            # Reload model in summarizer (this will happen automatically on next request)
            # The summarizer will load the newly trained model
        
    except Exception as e:
        logger.error(f"Error in incremental training: {e}", exc_info=True)
        if db:
            db.rollback()
