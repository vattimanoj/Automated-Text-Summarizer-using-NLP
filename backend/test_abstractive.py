
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

def test_abstractive_params():
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    test_text = """
Machine Learning (ML) is a field of Artificial Intelligence that focuses on building systems capable of learning from data. Instead of being explicitly programmed with rules, these systems improve their performance by identifying patterns and making predictions or decisions. Think of it as teaching a computer to 'learn by experience,' much like humans do.
    """
    
    prompts = [
        "summarize: ",
        "tl;dr: ",
        "In short, "
    ]
    
    configs = [
        {"max_length": 40, "min_length": 15, "length_penalty": 0.5, "num_beams": 4},
        {"max_length": 60, "min_length": 15, "length_penalty": 1.0, "num_beams": 4}
    ]
    
    print("RESULTS:")
    for p in prompts:
        for c in configs:
            input_text = p + test_text.strip()
            inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(device)
            outputs = model.generate(
                inputs["input_ids"],
                **c,
                no_repeat_ngram_size=3,
                early_stopping=True
            )
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"PROMPT: {p} | CONFIG: {c}")
            print(f"SUMMARY: {summary}\n")

if __name__ == "__main__":
    import sys
    with open('abstractive_results.log', 'w', encoding='utf-8') as f:
        sys.stdout = f
        test_abstractive_params()
