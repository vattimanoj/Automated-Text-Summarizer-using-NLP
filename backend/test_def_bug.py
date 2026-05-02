
import re

def test_def_extraction():
    block = """Supervised learning is the most widely used type of machine learning. It works with labeled data, meaning each input comes with a known output. 
Subtypes of Supervised Learning:
- Regression:
Regression is used when the output is a continuous value.
- Classification:
Classification is used when the output is categorical."""
    
    # Current regex
    clean_for_def = re.sub(r'^- [A-Za-z\s]+:\s*\n?.*', '', block, flags=re.DOTALL | re.MULTILINE).strip()
    print(f"CLEANED BLOCK:\n[{clean_for_def}]")
    
    sentences = re.split(r'\.\s+', clean_for_def)
    definition = sentences[0].strip() if sentences else ""
    print(f"DEFINITION: [{definition}]")

if __name__ == "__main__":
    test_def_extraction()
