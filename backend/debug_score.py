
import re
from app.ml_model.summarizer import get_explainer

def test_score_variation():
    explainer = get_explainer()
    
    texts = {
        "Short": "Machine Learning is a field of AI that focuses on building systems capable of learning from data.",
        "Medium": "Machine Learning (ML) is a field of Artificial Intelligence that focuses on building systems capable of learning from data. Instead of being explicitly programmed with rules, these systems improve their performance by identifying patterns and making predictions or decisions. Think of it as teaching a computer to learn by experience, much like humans do.",
        "Large": """Machine Learning (ML) is a field of Artificial Intelligence that focuses on building systems capable of learning from data. Instead of being explicitly programmed with rules, these systems improve their performance by identifying patterns and making predictions or decisions. Think of it as teaching a computer to “learn by experience,” much like humans do.
        Types of Machine Learning:
        1. Supervised Learning: Supervised learning is the most widely used type of machine learning. It works with labeled data, meaning each input comes with a known output. The algorithm learns the mapping between inputs and outputs during training, and once trained, it can predict outcomes for new, unseen data.
        2. Unsupervised Learning: Unsupervised learning works with unlabeled data. The algorithm does not know the correct output; instead, it tries to discover hidden structures, patterns, or relationships in the dataset.
        3. Semi-Supervised Learning: Semi-supervised learning combines both labeled and unlabeled data. A small portion of the dataset is labeled, and the algorithm uses that to make sense of the larger unlabeled portion.
        """
    }
    
    scenarios = [
        {"label": "Short Text, Med Summary", "text": texts["Short"], "summary": "Machine Learning is a field of AI that focuses on building systems capable of learning from data."},
        {"label": "Med Text, Small Summary", "text": texts["Medium"], "summary": "ML helps computers learn."},
        {"label": "Large Text, Large Summary", "text": texts["Large"], "summary": "Machine Learning (ML) is a subfield of artificial intelligence that empowers systems to learn from experience and identify data patterns autonomously. It encompasses major types like supervised learning with labeled data, unsupervised learning for discovery, and semi-supervised techniques for efficiency."}
    ]
    
    for s in scenarios:
        explanation = explainer.generate_explanation(s["text"], s["summary"])
        print(f"[{s['label']}] Text Len: {len(s['text'])}, Sum Len: {len(s['summary'])}, Score: {explanation['average_importance_score']}")

if __name__ == "__main__":
    test_score_variation()
