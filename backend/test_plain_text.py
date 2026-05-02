
from app.ml_model.summarizer import SummarizationModel
import os

def test_plain_text():
    model = SummarizationModel()
    
    with open('user_test_text.txt', 'r', encoding='utf-8') as f:
        test_text = f.read()
    
    summary = model.summarize(test_text)
    
    with open('plain_text_result.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("Done!")

if __name__ == "__main__":
    test_plain_text()
