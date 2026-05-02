
from app.ml_model.summarizer import SummarizationModel
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def test_user_text():
    model = SummarizationModel()
    text = "Located in south Asia, it is the seventh-largest country by land area and the most populous country globally, with over 1.4 billion people. India s history dates back more than 5,000 years to the Indus Valley Civilization, one of the world s earliest urban cultures."
    print("\nTesting 'summarize:' prompt...")
    # Manually run the generation logic for 'summarize:'
    input_text1 = f"summarize: {text}"
    inputs1 = model.tokenizer(input_text1, return_tensors="pt").to(model.device)
    outputs1 = model.model.generate(inputs1["input_ids"], max_length=150, min_length=20)
    sum1 = model.tokenizer.decode(outputs1[0], skip_special_tokens=True).strip()
    
    print("Testing 'summarize briefly:' prompt...")
    input_text2 = f"summarize briefly: {text}"
    inputs2 = model.tokenizer(input_text2, return_tensors="pt").to(model.device)
    outputs2 = model.model.generate(inputs2["input_ids"], max_length=150, min_length=20)
    sum2 = model.tokenizer.decode(outputs2[0], skip_special_tokens=True).strip()
    
    with open("user_repro_result.txt", "w", encoding="utf-8") as f:
        f.write("INPUT:\n" + text + "\n\n")
        f.write("PROMPT 'summarize:':\n" + sum1 + "\n\n")
        f.write("PROMPT 'summarize briefly:':\n" + sum2 + "\n\n")
    
    print("\nComparisons done! Check user_repro_result.txt")

if __name__ == "__main__":
    test_user_text()
