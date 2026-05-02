from app.ml_model.summarizer import get_model
import json
import re

def test_ml_summary():
    text = """Machine Learning (ML) is a field of Artificial Intelligence that focuses on building systems capable of learning from data. Instead of being explicitly programmed with rules, these systems improve their performance by identifying patterns and making predictions or decisions. Think of it as teaching a computer to “learn by experience,” much like humans do.
?? Types of Machine Learning
1. Supervised Learning
Supervised learning is the most widely used type of machine learning. It works with labeled data, meaning each input comes with a known output. The algorithm learns the mapping between inputs and outputs during training, and once trained, it can predict outcomes for new, unseen data.
Think of it as a student learning with a teacher who provides the correct answers during practice.
Subtypes of Supervised Learning:
- Regression:
Regression is used when the output is a continuous value. The algorithm learns relationships between variables and predicts numerical outcomes.
Example: Predicting house prices based on features like size, location, and age.
Algorithms: Linear Regression, Polynomial Regression, Support Vector Regression.
- Classification:
Classification is used when the output is categorical (discrete classes). The algorithm learns to assign inputs into predefined categories.
Example: Classifying emails as spam or not spam.
- Algorithms: Logistic Regression, Decision Trees, Random Forests, Support Vector Machines, k-Nearest Neighbors.
- Ensemble Methods:
Ensemble methods combine multiple models to improve accuracy and robustness. Instead of relying on a single model, they aggregate predictions from several models.
Example: Random Forest (bagging), Gradient Boosting, AdaBoost, Stacking.
2. Unsupervised Learning
Unsupervised learning works with unlabeled data. The algorithm does not know the correct output; instead, it tries to discover hidden structures, patterns, or relationships in the dataset.
It’s like exploring a new city without a guide – you discover neighborhoods and landmarks on your own.
Subtypes of Unsupervised Learning:
- Clustering:
Clustering groups data points into clusters based on similarity. It helps identify natural groupings in data.
Example: Customer segmentation in marketing.
Algorithms: K-means, Hierarchical Clustering, DBSCAN.
- Dimensionality Reduction:
Dimensionality reduction simplifies data by reducing the number of features while retaining essential information. It’s often used for visualization or speeding up computation.
Example: Visualizing high-dimensional genetic data in 2D.
Algorithms: Principal Component Analysis (PCA), t-SNE, Autoencoders.
- Association Rule Learning:
- Association rule learning finds relationships between variables in large datasets. It’s often used in market basket analysis to discover co-purchasing patterns.
Example: “Customers who buy bread often buy butter.”
Algorithms: Apriori, FP-Growth.
3.Semi-Supervised Learning
Semi-supervised learning combines both labeled and unlabeled data. A small portion of the dataset is labeled, and the algorithm uses that to make sense of the larger unlabeled portion.
It’s like having a partial answer key – enough to guide you, but not complete.
"""
    print("Testing ML Summary Coverage (Section Mode)...")
    model = get_model()
    
    # Debug: Check sections
    sections_found = model._extract_sections(model._clean_text(text))
    
    summary = model.summarize(text)
    
    print("\n" + "="*50)
    print("FINAL SUMMARY:")
    print(summary)
    print("="*50)
    
    key_terms = ["Regression", "Classification", "Ensemble Methods", "Clustering", "Dimensionality Reduction", "Association Rule"]
    found = [t for t in key_terms if t.lower() in summary.lower()]
    print(f"\nVerification: Found concepts {found} out of {key_terms}")
    
    with open("ml_debug.txt", "w") as f:
        f.write("SECTIONS DETECTED:\n")
        if sections_found:
            for h, b in sections_found[1]:
                f.write(f"- {h}\n")
        else:
            f.write("NONE\n")
        f.write("\nSUMMARY:\n")
        f.write(summary)

if __name__ == "__main__":
    test_ml_summary()
