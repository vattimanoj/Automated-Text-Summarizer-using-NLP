
from app.ml_model.summarizer import SummarizationModel
import os

def test_hierarchical():
    model = SummarizationModel()
    
    test_text = """
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
* Goal: Discover the datas underlying organization.
* Examples: Clustering (e.g., customer segmentation), Association (e.g., market basket analysis)
3. Semi-Supervised Learning
* Definition: Uses a small amount of labeled data and a large amount of unlabeled data.
4. Reinforcement Learning (RL)
* Definition: The model (agent) learns by interacting with an environment and receiving rewards or penalties for its actions.
    """
    
    summary = model.summarize(test_text, max_length=150, min_length=30)
    
    with open("hierarchical_test.txt", "w", encoding="utf-8") as f:
        f.write("SUMMARY CONTENT:\n")
        f.write(summary)
    
    print("Done! Check hierarchical_test.txt")

if __name__ == "__main__":
    test_hierarchical()
