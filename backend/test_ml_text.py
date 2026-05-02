
from app.ml_model.summarizer import SummarizationModel
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def test_ml_text():
    model = SummarizationModel()
    text = """Supervised Learning is the most widely used type of machine learning. the algorithm learns the mapping between inputs and outputs during training. once trained, it can predict outcomes for new, unseen data.

Subtypes of Supervised Learning:
- Regression is used when the output is a continuous value. the algorithm learns relationships between variables and predicts numerical outcomes. Classification: Is used when the output is categorical (discrete classes) algorithm learns to assign inputs into predefined categories. example: Classifying emails as spam or not spam. Ensemble Methods: Combine multiple models to improve accuracy. instead of relying on a single model, they aggregate predictions from several models.

2. Unsupervised Learning works with unlabeled data. it tries to discover hidden structures, patterns, or relationships in the dataset.

Subtypes of Unsupervised Learning:
- Clustering groups data points into clusters based on similarity. Dimensionality Reduction: Simplifies data by reducing the number of features while retaining essential information. it is often used for visualization or speeding up computation. Association Rule Learning: Finds relationships between variables in large datasets. customers who buy bread often buy butter.

3.Semi-Supervised Learning combines labeled and unlabeled data. a small portion of the dataset is labels. it s like having a partial answer key enough to guide you."""
    
    print("\nGenerating summary...")
    summary = model.summarize(text)
    
    with open("ml_repro_result.txt", "w", encoding="utf-8") as f:
        f.write("INPUT:\n" + text + "\n\n")
        f.write("SUMMARY:\n" + summary + "\n")
    
    print("\nDone! Result in ml_repro_result.txt")

if __name__ == "__main__":
    test_ml_text()
