
import re

def test_smart_extract():
    test_text = """
Machine Learning (ML) is a branch of artificial intelligence (AI) that enables computers to learn from data and improve their performance automatically without being explicitly programmed.
It uses algorithms to identify patterns and make predictions or decisions based on new data.
?? Major Types of Machine Learning
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
    
    # Simulate a partial summary from AI
    current_summary = "Machine learning (ML) is a branch of AI that enables computers to learn from data. It uses algorithms to identify patterns. Supervised Learning is trained on a labeled dataset."
    
    # 1. Identify categories
    list_headers = re.findall(r'^[0-9*]\.\s*([A-Z][a-zA-Z\s\-\(\)]+?)(?::|\.|\n)', test_text, flags=re.MULTILINE)
    print("Detected Categories:", list_headers)
    
    # 2. For each category, try to find a definition/description in original text
    extracted_defs = {}
    for cat in list_headers:
        # Escape for regex
        escaped_cat = re.escape(cat)
        # Find the category in text and get the next few lines
        # Look for "Definition: ..." or just the next sentence
        pattern = rf"{escaped_cat}.*?(?:Definition:|:)\s*(.*?)(?:\.|\n)"
        match = re.search(pattern, test_text, re.DOTALL | re.IGNORECASE)
        if match:
            extracted_defs[cat] = match.group(1).strip()
    
    print("\nExtracted Definitions:")
    for cat, d in extracted_defs.items():
        print(f"- {cat}: {d}")
    
    # 3. Check what's missing in summary
    final_summary = current_summary
    missing_elements = []
    for cat in list_headers:
        if cat.lower() not in final_summary.lower():
            definition = extracted_defs.get(cat, "")
            missing_elements.append(f"{cat}: {definition}")
    
    if missing_elements:
        final_summary += "\n\nAdditional Types & Definitions:\n" + "\n".join(missing_elements)
    
    print("\nFINAL ENRICHED SUMMARY:")
    print(final_summary)

if __name__ == "__main__":
    test_smart_extract()
