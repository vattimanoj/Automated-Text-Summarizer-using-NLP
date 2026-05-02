
from app.ml_model.summarizer import SummarizationModel
import torch
import logging
import sys

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def test_prompts():
    model = SummarizationModel()
    
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
    
    prompts = [
        "summarize: ",
        "summarize comprehensively including all major points: ",
        "summarize specifically including all the types mentioned: "
    ]
    
    for prompt in prompts:
        print(f"\n--- Testing Prompt: '{prompt}' ---")
        input_text = f"{prompt}{test_text}"
        inputs = model.tokenizer(
            input_text,
            max_length=512,
            truncation=True,
            return_tensors="pt"
        ).to(model.device)
        
        outputs = model.model.generate(
            inputs["input_ids"],
            max_length=256,
            min_length=80,
            length_penalty=2.5,
            num_beams=6,
            early_stopping=True
        )
        
        summary = model.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("Summary:")
        print(summary)

if __name__ == "__main__":
    test_prompts()
