"""
Initial Training Script - Manual training command
Run with: python train_model.py

Backend does NOT run training automatically - it starts immediately.
"""
import os
import logging
from app.ml_model.dataset_collector import DatasetCollector
from app.ml_model.model_trainer import ModelTrainer
from app.config import settings

logger = logging.getLogger(__name__)

def run_initial_training(force_retrain: bool = False):
    """
    Run training with datasets
    This is a MANUAL command - backend does NOT call this automatically.
    Usage: python train_model.py [--force]
    """
    csv_path = "./training_data.csv"
    model_dir = "./models/trained"
    
    # Check if trained model already exists
    model_config_path = os.path.join(model_dir, "config.json")
    model_pytorch_path = os.path.join(model_dir, "pytorch_model.bin")
    model_safetensors_path = os.path.join(model_dir, "model.safetensors")
    
    model_exists = (
        os.path.exists(model_config_path) and 
        (os.path.exists(model_pytorch_path) or os.path.exists(model_safetensors_path))
    )
    
    if model_exists and not force_retrain:
        logger.info("=" * 50)
        logger.info("Trained model already exists. Skipping training.")
        logger.info("Model location: " + model_dir)
        logger.info("Use --force flag to retrain anyway.")
        logger.info("=" * 50)
        return True
    
    # Check if CSV exists
    collector = DatasetCollector(csv_path)
    
    # Load existing CSV first
    existing_df = collector.load_from_csv()
    
    if existing_df.empty or force_retrain:
        logger.info("Collecting datasets...")
        
        # Collect datasets (adjust sample sizes as needed)
        # Smaller sizes for faster training - increase for better results
        all_data = collector.collect_all_datasets(
            cnn_samples=5000,    # CNN/DailyMail
            xsum_samples=2000,   # XSum
            wikihow_samples=2000 # WikiHow
        )
        
        if not all_data and existing_df.empty:
            logger.error("Failed to collect datasets and no existing CSV found. Cannot train.")
            return False
        elif all_data:
            # If CSV exists, append new data; otherwise create new
            collector.save_to_csv(all_data, append=not existing_df.empty and not force_retrain)
    else:
        logger.info(f"Using existing CSV with {len(existing_df)} records")
    
    # Train model
    logger.info("Starting model training...")
    trainer = ModelTrainer()
    
    train_texts, train_summaries, val_texts, val_summaries = trainer.load_data(csv_path)
    
    if not train_texts:
        logger.error("No training data available. Cannot train model.")
        return False
    
    # Train with optimized settings for CPU (FAST training with 95% accuracy target)
    results = trainer.train(
        train_texts=train_texts,
        train_summaries=train_summaries,
        val_texts=val_texts,
        val_summaries=val_summaries,
        epochs=2,  # 2 epochs for better accuracy while staying fast
        batch_size=6,  # Increased batch size for faster training
        learning_rate=3e-5,  # Optimal LR for T5 model convergence
        target_accuracy=0.95  # Target 95% accuracy
    )
    
    if results:
        logger.info("=" * 50)
        logger.info("Training completed successfully!")
        logger.info(f"ROUGE-1: {results['rouge1']:.4f} ({results['rouge1']*100:.2f}%)")
        logger.info(f"ROUGE-2: {results['rouge2']:.4f} ({results['rouge2']*100:.2f}%)")
        logger.info(f"ROUGE-L: {results['rougeL']:.4f} ({results['rougeL']*100:.2f}%)")
        logger.info(f"Average ROUGE: {results['avg_rouge']:.4f} ({results['avg_rouge']*100:.2f}%)")
        logger.info("Model saved. Backend will use it automatically.")
        logger.info("=" * 50)
        return True
    else:
        logger.error("Training failed")
        return False

if __name__ == "__main__":
    # Run training standalone
    logging.basicConfig(level=logging.INFO)
    run_initial_training(force_retrain=True)
