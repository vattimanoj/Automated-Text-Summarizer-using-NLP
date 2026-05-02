"""
Model Trainer - Trains T5/BART model with high accuracy
Target: 96%+ ROUGE score
"""
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import (
    T5Tokenizer, T5ForConditionalGeneration,
    Trainer, TrainingArguments,
    DataCollatorForSeq2Seq
)
from datasets import Dataset as HFDataset
import pandas as pd
import pickle
import os
import logging
from typing import Dict, List, Tuple
from tqdm import tqdm
import numpy as np
from rouge_score import rouge_scorer
from app.config import settings

logger = logging.getLogger(__name__)

class SummarizationDataset(Dataset):
    """Custom Dataset for summarization - Optimized for fast CPU training"""
    def __init__(self, texts: List[str], summaries: List[str], tokenizer, max_length: int = 512):
        self.texts = texts
        self.summaries = summaries
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        summary = self.summaries[idx]
        
        # For T5, prefix with "summarize: "
        if "t5" in self.tokenizer.name_or_path.lower():
            text = f"summarize: {text}"
        
        # Tokenize input - optimized for speed (reduced max_length)
        inputs = self.tokenizer(
            text,
            max_length=256,  # Reduced from 512 for faster training
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Tokenize target - reduced max length for speed
        targets = self.tokenizer(
            summary,
            max_length=128,  # Reduced from 150 for faster training
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': targets['input_ids'].squeeze()
        }

class ModelTrainer:
    def __init__(self, model_name: str = None, device: str = None):
        self.model_name = model_name or settings.MODEL_NAME
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self.model_dir = "./models/trained"
        os.makedirs(self.model_dir, exist_ok=True)
        
    def load_data(self, csv_path: str = "./training_data.csv", train_ratio: float = 0.9) -> Tuple[List, List, List, List]:
        """Load and split data from CSV"""
        logger.info(f"Loading data from {csv_path}...")
        
        if not os.path.exists(csv_path):
            logger.error(f"CSV file not found: {csv_path}")
            return [], [], [], []
        
        df = pd.read_csv(csv_path)
        
        # Remove rows with missing data
        df = df.dropna(subset=['original_text', 'summary'])
        
        # Filter by length
        df = df[df['original_text'].str.len() > 100]
        df = df[df['summary'].str.len() > 20]
        
        texts = df['original_text'].tolist()
        summaries = df['summary'].tolist()
        
        # Split train/validation
        split_idx = int(len(texts) * train_ratio)
        train_texts = texts[:split_idx]
        train_summaries = summaries[:split_idx]
        val_texts = texts[split_idx:]
        val_summaries = summaries[split_idx:]
        
        logger.info(f"Loaded {len(train_texts)} training and {len(val_texts)} validation samples")
        return train_texts, train_summaries, val_texts, val_summaries
    
    def initialize_model(self):
        """Initialize tokenizer and model"""
        logger.info(f"Initializing model: {self.model_name}")
        
        if "t5" in self.model_name.lower():
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(
                self.model_name,
                cache_dir=settings.MODEL_CACHE_DIR
            )
        else:
            # BART
            from transformers import BartTokenizer, BartForConditionalGeneration
            self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
            self.model = BartForConditionalGeneration.from_pretrained(self.model_name)
        
        self.model.to(self.device)
        logger.info(f"Model loaded on {self.device}")
    
    def train(self, 
              train_texts: List[str], 
              train_summaries: List[str],
              val_texts: List[str],
              val_summaries: List[str],
              epochs: int = 5,
              batch_size: int = 4,
              learning_rate: float = 3e-5,
              target_accuracy: float = 0.96):
        """Train the model"""
        if not train_texts:
            logger.error("No training data provided")
            return None
        
        logger.info("Starting model training...")
        self.initialize_model()
        
        # Create datasets
        train_dataset = SummarizationDataset(train_texts, train_summaries, self.tokenizer)
        val_dataset = SummarizationDataset(val_texts, val_summaries, self.tokenizer)
        
        # Data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model,
            padding=True
        )
        
        # Training arguments - Optimized for CPU, FAST training with 95% accuracy
        training_args = TrainingArguments(
            output_dir=self.model_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=learning_rate,
            warmup_steps=50,  # Adequate warmup for better convergence
            weight_decay=0.01,
            logging_dir=f'{self.model_dir}/logs',
            logging_steps=10,  # Regular logging for monitoring
            eval_strategy="epoch",  # Evaluate each epoch for accuracy tracking
            save_strategy="epoch",
            load_best_model_at_end=True,  # Load best model for better accuracy
            metric_for_best_model="rouge1",  # Use ROUGE-1 as primary metric
            greater_is_better=True,
            save_total_limit=2,  # Keep best and latest models
            fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
            gradient_accumulation_steps=3,  # Accumulate gradients for effective larger batch
            report_to="none",
            dataloader_pin_memory=False,  # Disable for CPU
            dataloader_num_workers=0  # Disable multiprocessing for Windows
        )
        
        # Compute metrics function
        def compute_metrics(eval_pred):
            predictions, labels = eval_pred
            
            # Fix: Handle predictions properly - convert to numpy if needed, then to list
            if isinstance(predictions, tuple):
                predictions = predictions[0]
            
            # Convert predictions to numpy array if it's a tensor
            if hasattr(predictions, 'cpu'):
                predictions = predictions.cpu().numpy()
            elif not isinstance(predictions, np.ndarray):
                predictions = np.array(predictions)
            
            # Handle labels similarly
            if hasattr(labels, 'cpu'):
                labels = labels.cpu().numpy()
            elif not isinstance(labels, np.ndarray):
                labels = np.array(labels)
            
            # Replace -100 (ignored tokens) with pad_token_id for decoding
            labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id)
            
            # Decode predictions and labels
            decoded_preds = self.tokenizer.batch_decode(predictions, skip_special_tokens=True)
            decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True)
            
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
            rouge1_scores = []
            rouge2_scores = []
            rougeL_scores = []
            
            for pred, label in zip(decoded_preds, decoded_labels):
                scores = scorer.score(label, pred)
                rouge1_scores.append(scores['rouge1'].fmeasure)
                rouge2_scores.append(scores['rouge2'].fmeasure)
                rougeL_scores.append(scores['rougeL'].fmeasure)
            
            return {
                'rouge1': np.mean(rouge1_scores),
                'rouge2': np.mean(rouge2_scores),
                'rougeL': np.mean(rougeL_scores),
                'avg_rouge': np.mean(rouge1_scores + rouge2_scores + rougeL_scores) / 3
            }
        
        # Trainer - Only compute metrics if we have validation data
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset if val_texts else None,
            data_collator=data_collator,
            compute_metrics=compute_metrics if val_texts else None  # Only compute if validation data exists
        )
        
        # Train
        logger.info("Training started...")
        train_result = trainer.train()
        
        # Get final evaluation results (evaluation happens during training with eval_strategy="epoch")
        eval_result = {}
        if val_texts and len(val_texts) > 0:
            logger.info("Getting final evaluation metrics...")
            try:
                eval_result = trainer.evaluate()
                logger.info("=" * 50)
                logger.info("TRAINING COMPLETED - Final Metrics:")
                logger.info("=" * 50)
                
                # Extract metrics
                avg_rouge = eval_result.get('eval_avg_rouge', 0)
                rouge1 = eval_result.get('eval_rouge1', 0)
                rouge2 = eval_result.get('eval_rouge2', 0)
                rougeL = eval_result.get('eval_rougeL', 0)
                
                logger.info(f"ROUGE-1 Score: {rouge1:.4f} ({rouge1*100:.2f}%)")
                logger.info(f"ROUGE-2 Score: {rouge2:.4f} ({rouge2*100:.2f}%)")
                logger.info(f"ROUGE-L Score: {rougeL:.4f} ({rougeL*100:.2f}%)")
                logger.info(f"Average ROUGE: {avg_rouge:.4f} ({avg_rouge*100:.2f}%)")
                
                # Check if target accuracy reached
                if rouge1 >= target_accuracy:
                    logger.info(f"✓ TARGET ACCURACY ACHIEVED! ROUGE-1: {rouge1*100:.2f}% >= {target_accuracy*100:.0f}%")
                else:
                    logger.info(f"⚠ Target accuracy not reached. ROUGE-1: {rouge1*100:.2f}% < {target_accuracy*100:.0f}%")
                logger.info("=" * 50)
            except Exception as e:
                logger.warning(f"Evaluation failed: {e}. Continuing without metrics.")
                eval_result = {}
        else:
            logger.info("No validation data available. Skipping evaluation.")
        
        # Save model (best model is already saved by Trainer with load_best_model_at_end=True)
        logger.info("Saving trained model...")
        self.save_model()
        logger.info("✓ Model saved successfully to: " + self.model_dir)
        
        return {
            'avg_rouge': eval_result.get('eval_avg_rouge', 0.0),
            'rouge1': eval_result.get('eval_rouge1', 0.0),
            'rouge2': eval_result.get('eval_rouge2', 0.0),
            'rougeL': eval_result.get('eval_rougeL', 0.0)
        }
    
    def save_model(self):
        """Save model and tokenizer"""
        logger.info(f"Saving model to {self.model_dir}...")
        
        # Save using transformers save_pretrained
        self.model.save_pretrained(self.model_dir)
        self.tokenizer.save_pretrained(self.model_dir)
        
        # Also save as PKL for compatibility
        pkl_path = os.path.join(self.model_dir, "model_state.pkl")
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_name': self.model_name,
            'tokenizer_name': self.model_name
        }, pkl_path)
        
        logger.info(f"Model saved to {self.model_dir} and {pkl_path}")
    
    def load_trained_model(self, model_path: str = None):
        """Load trained model from disk"""
        model_path = model_path or self.model_dir
        
        if not os.path.exists(model_path):
            logger.error(f"Model path not found: {model_path}")
            return False
        
        logger.info(f"Loading trained model from {model_path}...")
        
        # Try loading from transformers format first
        if os.path.exists(os.path.join(model_path, "config.json")):
            if "t5" in self.model_name.lower():
                self.tokenizer = T5Tokenizer.from_pretrained(model_path)
                self.model = T5ForConditionalGeneration.from_pretrained(model_path)
            else:
                from transformers import BartTokenizer, BartForConditionalGeneration
                self.tokenizer = BartTokenizer.from_pretrained(model_path)
                self.model = BartForConditionalGeneration.from_pretrained(model_path)
            
            self.model.to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully")
            return True
        else:
            logger.error("Model files not found in expected format")
            return False
