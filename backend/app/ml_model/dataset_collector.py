"""
Dataset Collector - Downloads and processes datasets for training
Supports: CNN/DailyMail, XSum, WikiHow
Also manages CSV file operations
"""
import os
import csv
import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DatasetCollector:
    def __init__(self, csv_path: str = "./training_data.csv"):
        self.csv_path = csv_path
        self.data_dir = "./datasets"
        os.makedirs(self.data_dir, exist_ok=True)
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(os.path.abspath(csv_path)) if os.path.dirname(csv_path) else ".", exist_ok=True)
    
    def load_existing_csv(self) -> pd.DataFrame:
        """Load existing CSV if it exists"""
        if os.path.exists(self.csv_path):
            try:
                df = pd.read_csv(self.csv_path)
                logger.info(f"Loaded {len(df)} existing records from {self.csv_path}")
                return df
            except Exception as e:
                logger.error(f"Error loading CSV: {e}")
                return pd.DataFrame()
        return pd.DataFrame()
    
    def collect_cnn_dailymail(self, num_samples: int = 10000) -> List[Dict]:
        """Collect CNN/DailyMail dataset"""
        logger.info("Downloading CNN/DailyMail dataset...")
        try:
            from datasets import load_dataset
            dataset = load_dataset("cnn_dailymail", "3.0.0", split=f"train[:{num_samples}]")
            
            data = []
            for item in dataset:
                text = item.get('article', '')
                summary = item.get('highlights', '')
                
                if text and summary and len(text) > 100 and len(summary) > 20:
                    data.append({
                        'original_text': text,
                        'summary': summary.replace('\n', ' ').strip(),
                        'source': 'cnn_dailymail',
                        'domain': 'news'
                    })
            
            logger.info(f"Collected {len(data)} samples from CNN/DailyMail")
            return data
        except Exception as e:
            logger.error(f"Error collecting CNN/DailyMail: {e}")
            return []
    
    def collect_xsum(self, num_samples: int = 5000) -> List[Dict]:
        """Collect XSum dataset (BBC articles)"""
        logger.info("Downloading XSum dataset...")
        try:
            from datasets import load_dataset
            dataset = load_dataset("xsum", split=f"train[:{num_samples}]")
            
            data = []
            for item in dataset:
                text = item.get('document', '')
                summary = item.get('summary', '')
                
                if text and summary and len(text) > 100 and len(summary) > 10:
                    data.append({
                        'original_text': text,
                        'summary': summary.strip(),
                        'source': 'xsum',
                        'domain': 'news'
                    })
            
            logger.info(f"Collected {len(data)} samples from XSum")
            return data
        except Exception as e:
            logger.error(f"Error collecting XSum: {e}")
            return []
    
    def collect_wikihow(self, num_samples: int = 5000) -> List[Dict]:
        """Collect WikiHow dataset"""
        logger.info("Downloading WikiHow dataset...")
        try:
            from datasets import load_dataset
            dataset = load_dataset("wikihow", "all", split=f"train[:{num_samples}]")
            
            data = []
            for item in dataset:
                text = item.get('text', [])
                if isinstance(text, list):
                    text = ' '.join(text)
                
                summary = item.get('headline', '')
                
                if text and summary and len(text) > 100 and len(summary) > 10:
                    data.append({
                        'original_text': text,
                        'summary': summary.strip(),
                        'source': 'wikihow',
                        'domain': 'instructional'
                    })
            
            logger.info(f"Collected {len(data)} samples from WikiHow")
            return data
        except Exception as e:
            logger.error(f"Error collecting WikiHow: {e}")
            return []
    
    def collect_all_datasets(self, cnn_samples: int = 5000, xsum_samples: int = 2000, wikihow_samples: int = 2000) -> List[Dict]:
        """Collect all datasets and combine"""
        logger.info("Starting dataset collection...")
        
        # First, load existing CSV
        existing_df = self.load_existing_csv()
        existing_texts = set(existing_df['original_text'].tolist()) if not existing_df.empty else set()
        
        all_data = []
        
        # Collect from each dataset
        cnn_data = self.collect_cnn_dailymail(cnn_samples)
        xsum_data = self.collect_xsum(xsum_samples)
        wikihow_data = self.collect_wikihow(wikihow_samples)
        
        # Filter out duplicates
        for item in cnn_data + xsum_data + wikihow_data:
            if item['original_text'] not in existing_texts:
                all_data.append(item)
                existing_texts.add(item['original_text'])
        
        logger.info(f"Total new samples collected: {len(all_data)}")
        return all_data
    
    def save_to_csv(self, data: List[Dict], append: bool = False):
        """Save data to CSV file"""
        if not data:
            logger.warning("No data to save")
            return
        
        df = pd.DataFrame(data)
        
        if append and os.path.exists(self.csv_path):
            # Append to existing CSV
            existing_df = pd.read_csv(self.csv_path)
            # Get next ID
            next_id = int(existing_df['id'].max()) + 1 if not existing_df.empty and 'id' in existing_df.columns else 0
            df['id'] = range(next_id, next_id + len(df))
            
            # Combine and remove duplicates based on text
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['original_text'], keep='last')
            combined_df.to_csv(self.csv_path, index=False)
            logger.info(f"Appended {len(df)} records. Total records: {len(combined_df)}")
        else:
            # Create new CSV
            if 'id' not in df.columns:
                df.insert(0, 'id', range(len(df)))
            df.to_csv(self.csv_path, index=False)
            logger.info(f"Saved {len(df)} records to {self.csv_path}")
    
    def load_from_csv(self) -> pd.DataFrame:
        """Load data from CSV file"""
        if not os.path.exists(self.csv_path):
            logger.warning(f"CSV file not found: {self.csv_path}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(self.csv_path)
            logger.info(f"Loaded {len(df)} records from {self.csv_path}")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return pd.DataFrame()
    
    def update_csv_from_database(self, db_session):
        """Update CSV with new data from database"""
        from app.models import Feedback, Summary, Document
        
        logger.info("Updating CSV from database...")
        
        # Get high-quality feedback with corrected summaries
        feedbacks = db_session.query(Feedback).join(Summary).join(Document).filter(
            Feedback.rating >= 4,
            Feedback.corrected_summary.isnot(None),
            Feedback.used_for_training == False
        ).all()
        
        if not feedbacks:
            logger.info("No new feedback to add to CSV")
            return 0
        
        # Load existing CSV to check for duplicates
        existing_df = self.load_from_csv()
        existing_texts = set(existing_df['original_text'].tolist()) if not existing_df.empty else set()
        
        new_data = []
        for feedback in feedbacks:
            document = feedback.summary.document
            target_summary = feedback.corrected_summary or feedback.summary.summary_text
            
            # Check if already exists
            if document.original_text not in existing_texts:
                new_data.append({
                    'original_text': document.original_text,
                    'summary': target_summary,
                    'source': 'user_feedback',
                    'domain': document.domain or 'general'
                })
                existing_texts.add(document.original_text)
        
        if new_data:
            self.save_to_csv(new_data, append=True)
            logger.info(f"Added {len(new_data)} new records from database to CSV")
            
            # Mark feedback as used
            for feedback in feedbacks:
                feedback.used_for_training = True
            db_session.commit()
            return len(new_data)
        
        return 0
