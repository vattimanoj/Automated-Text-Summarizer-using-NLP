
import re

def test_example_extract():
    test_text = """
1. Supervised Learning
* Definition: The model is trained on a labeled dataset (input-output pairs).
* Goal: Learn a mapping from inputs to outputs.
* Examples: 
o Classification: Predicting a category (e.g., spam email detection)
o Regression: Predicting a continuous value (e.g., house price prediction)
2. Unsupervised Learning
* Definition: The model is trained on unlabeled data, finding hidden patterns or structures.
* Goal: Discover the datas underlying organization.
* Examples: Clustering, Association
    """
    
    # 1. Identify categories
    list_headers = re.findall(r'^[0-9*]\.\s*([A-Z][a-zA-Z\s\-\(\)]+?)(?::|\.|\n)', test_text, flags=re.MULTILINE)
    
    category_details = {}
    for cat in list_headers:
        escaped_cat = re.escape(cat)
        # Find the block for this category
        # It starts with the category name and ends at the next numbered title or end of string
        pattern = rf"{escaped_cat}\s*(.*?)(?=\n[0-9]+\.|\Z)"
        match = re.search(pattern, test_text, re.DOTALL | re.MULTILINE)
        
        if match:
            block = match.group(1).strip()
            # Extract definition
            def_match = re.search(r'(?:Definition:|:|\-)\s*(.*?)(?:\.|\n)', block, re.IGNORECASE)
            definition = def_match.group(1).strip() if def_match else ""
            
            # Extract examples
            ex_match = re.search(r'(?:Examples|Sub-types):\s*(.*?)(?:\n[0-9*]\.|\n\n|\Z)', block, re.DOTALL | re.IGNORECASE)
            examples = ex_match.group(1).strip() if ex_match else ""
            
            # Clean up examples (remove bullet points, etc.)
            examples = re.sub(r'^[o*]\s+', '', examples, flags=re.MULTILINE)
            examples = examples.replace("\n", "; ")
            
            detail = definition
            if examples:
                detail += f" (Examples: {examples})"
            
            category_details[cat] = detail

    print("Extracted Details:")
    for cat, detail in category_details.items():
        print(f"- {cat}: {detail}")

if __name__ == "__main__":
    test_example_extract()
