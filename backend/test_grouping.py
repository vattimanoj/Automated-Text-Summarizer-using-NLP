
from app.ml_model.summarizer import SummarizationModel
import logging
import sys

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def test_grouping():
    print("Initializing SummarizationModel...")
    model = SummarizationModel()
    
    test_text = """
Machine Learning Core Concepts
Artificial intelligence is a broad field with many sub-branches.
?? Key Types of Learning
1. Supervised Learning
* This involves training a model on labeled data where inputs and outputs are known.
* Regression and classification are two primary forms of supervised learning.
2. Unsupervised Learning
* This involves finding patterns in unlabeled data without predefined outputs.
* Clustering and dimensionality reduction are common techniques used here.
    """
    
    print("\nOriginal Text Length:", len(test_text))
    print("\nGenerating summary with grouping test...")
    
    try:
        summary = model.summarize(test_text, max_length=256, min_length=50)
        
        with open("grouping_result.txt", "w", encoding="utf-8") as f:
            f.write("SUMMARY OUTPUT:\n")
            f.write("-" * 50 + "\n")
            f.write(summary + "\n")
            f.write("-" * 50 + "\n")
            
            if "Key Types of Learning" in summary:
                 if "Supervised Learning:" in summary and "Unsupervised Learning:" in summary:
                      f.write("\n[SUCCESS] Grouping appears to have worked correctly!\n")
                 else:
                      f.write("\n[PARTIAL] Root heading found but children not fully grouped.\n")
            else:
                 f.write("\n[FAILURE] Root heading 'Key Types of Learning' not found in summary.\n")
             
    except Exception as e:
        with open("grouping_result.txt", "w", encoding="utf-8") as f:
            f.write(f"Error during summarization: {e}\n")

if __name__ == "__main__":
    test_grouping()
