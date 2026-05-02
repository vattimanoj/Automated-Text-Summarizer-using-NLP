
from app.ml_model.summarizer import SummarizationModel
from transformers import pipeline
import torch
import os

def test_comparison():
    print("Testing T5-small (Trained)...")
    t5_model = SummarizationModel()
    
    test_text = """
Machine Learning (ML) is a branch of artificial intelligence (AI) that enables computers to learn from data and improve their performance automatically without being explicitly programmed.
It uses algorithms to identify patterns and make predictions or decisions based on new data.
Major Types of Machine Learning
1. Supervised Learning
* Definition: The model is trained on a labeled dataset (input-output pairs).
* Goal: Learn a mapping from inputs to outputs.
* Examples: Classification (e.g., spam email detection), Regression (e.g., house price prediction)
2. Unsupervised Learning
* Definition: The model is trained on unlabeled data, finding hidden patterns or structures.
* Goal: Discover the datas underlying organization.
* Examples: Clustering (e.g., customer segmentation), Association (e.g., market basket analysis)
3. Semi-Supervised Learning
* Definition: Uses a small amount of labeled data and a large amount of unlabeled data.
* Goal: Improve learning accuracy when labels are scarce or expensive to obtain.
* Example: Image classification with few labeled samples.
4. Reinforcement Learning (RL)
* Definition: The model (agent) learns by interacting with an environment and receiving rewards or penalties for its actions.
* Goal: Learn a strategy (policy) to maximize cumulative rewards.
* Examples: Game playing (e.g., AlphaGo), robotics, autonomous driving.
    """
    
    print("\n--- T5 SUMMARY ---")
    t5_summary = t5_model.summarize(test_text, max_length=256, min_length=100)
    print(t5_summary)
    
    print("\n\nTesting BART-large-cnn (Pre-trained)...")
    try:
        bart_summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn", 
            device=0 if torch.cuda.is_available() else -1
        )
        print("\n--- BART SUMMARY ---")
        bart_summary = bart_summarizer(test_text, max_length=256, min_length=100, do_sample=False)[0]['summary_text']
        print(bart_summary)
    except Exception as e:
        print(f"BART Test failed: {e}")

if __name__ == "__main__":
    test_comparison()
