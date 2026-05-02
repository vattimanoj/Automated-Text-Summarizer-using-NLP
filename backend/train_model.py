"""
Standalone script to train model manually
Usage: python train_model.py [--force]

This is a SEPARATE command - backend does NOT run training automatically.
Backend starts immediately and uses existing trained model.
"""
import argparse
import logging
from app.ml_model.initial_training import run_initial_training

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train summarization model (separate command)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python train_model.py          # Train if model doesn't exist
  python train_model.py --force  # Force retrain even if model exists
  
Note: Backend runs separately and uses trained model automatically.
      No need to restart backend after training.
        """
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force retrain even if model exists"
    )
    args = parser.parse_args()
    
    print("=" * 70)
    print("AUTOMATED TEXT SUMMARIZER - MODEL TRAINING")
    print("=" * 70)
    print("\nThis command will:")
    print("  1. Use existing training_data.csv (151 records)")
    print("  2. Train T5-small model with 95% accuracy target")
    print("  3. Save trained model to ./models/trained/")
    print("\nTraining time: ~10-20 minutes (2 epochs, optimized for speed)")
    print("\nBackend will automatically use this trained model after training.")
    print("=" * 70)
    
    confirm = input("\nPress Enter to start training (or Ctrl+C to cancel): ")
    
    print("\n" + "=" * 70)
    print("STARTING TRAINING...")
    print("=" * 70)
    
    success = run_initial_training(force_retrain=args.force)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("Model saved to: ./models/trained/")
        print("CSV file: ./training_data.csv")
        print("\nBackend will automatically use this trained model.")
        print("No need to restart backend - it will load the model automatically.")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ TRAINING FAILED")
        print("=" * 70)
        print("Check logs above for error details.")
        print("=" * 70)
