
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath("backend"))

from app.ml_model.summarizer import get_model
from app.config import settings

text = """
Machine Learning (ML) is a branch of artificial intelligence (AI) that enables computers to learn from data and improve their performance automatically without being explicitly programmed.
It uses algorithms to identify patterns and make predictions or decisions based on new data.
?? Major Types of Machine Learning
1. Supervised Learning
* Definition: The model is trained on a labeled dataset (input-output pairs).
* Goal: Learn a mapping from inputs to outputs.
* Examples: 
o Classification: Predicting a category (e.g., spam email detection)
o Regression: Predicting a continuous value (e.g., house price prediction)
2. Unsupervised Learning
* Definition: The model is trained on unlabeled data, finding hidden patterns or structures.
* Goal: Discover the data’s underlying organization.
* Examples: 
o Clustering: Grouping similar data points (e.g., customer segmentation)
o Association: Finding relationships between variables (e.g., market basket analysis)
3. Semi-Supervised Learning
* Definition: Uses a small amount of labeled data and a large amount of unlabeled data.
* Goal: Improve learning accuracy when labels are scarce or expensive to obtain.
* Example: Image classification with few labeled samples.
4. Reinforcement Learning (RL)
* Definition: The model (agent) learns by interacting with an environment and receiving rewards or penalties for its actions.
* Goal: Learn a strategy (policy) to maximize cumulative rewards.
* Examples: Game playing (e.g., AlphaGo), robotics, autonomous driving.
?? Summary Table
Type
Data Used
Objective
Example
Supervised Learning
Labeled
Predict known outputs
Spam detection, house prices
Unsupervised Learning
Unlabeled
Find hidden patterns
Customer grouping
Semi-Supervised
Mixed
Improve learning with few labels
Image recognition
"""

model = get_model()
print(f"Using model: {model.model_name}")

summary = model.summarize(text, max_length=256, min_length=50)
print("\n--- Summary ---")
print(summary)
print("\nLength in words:", len(summary.split()))
