
from app.ml_model.summarizer import SummarizationModel
import os

def test_final_quality():
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
    """
    
    summary = model.summarize(test_text, max_length=256, min_length=80)
    
    with open("final_summary_test.txt", "w", encoding="utf-8") as f:
        f.write("ORIGINAL LENGTH: " + str(len(test_text)) + "\n")
        f.write("SUMMARY LENGTH: " + str(len(summary)) + "\n")
        f.write("SUMMARY CONTENT:\n")
        f.write(summary)
    
    print("Done! Check final_summary_test.txt")

if __name__ == "__main__":
    test_final_quality()
