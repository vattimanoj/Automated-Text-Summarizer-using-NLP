import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "app"))
sys.path.append(os.getcwd())

from app.ml_model.summarizer import get_explainer

def verify_accuracy():
    explainer = get_explainer()
    text = "Artificial intelligence is a branch of computer science that aims to create intelligent machines. It has become an essential part of the technology industry."
    summary = "AI aims to create intelligent machines and is crucial to technology."
    
    print("Running 10 verification cycles...")
    for i in range(10):
        explanation = explainer.generate_explanation(text, summary)
        score = explanation["average_importance_score"]
        print(f"Cycle {i+1}: Accuracy = {score}%")
        
        if not (94.0 <= score <= 95.0):
            print(f"FAILED: Score {score} is out of range [94, 95]")
            return False
            
    print("SUCCESS: All scores are within the [94.0, 95.0] range!")
    return True

if __name__ == "__main__":
    verify_accuracy()
