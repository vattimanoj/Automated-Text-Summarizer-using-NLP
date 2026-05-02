
import re

test_text = """
Major Types of Machine Learning
1. Supervised Learning
* Definition: The model is trained on a labeled dataset (input-output pairs).
* Goal: Learn a mapping from inputs to outputs.
2. Unsupervised Learning
* Definition: The model is trained on unlabeled data, finding hidden patterns or structures.
* Goal: Discover the datas underlying organization.
3. Semi-Supervised Learning
* Definition: Uses a small amount of labeled data and a large amount of unlabeled data.
4. Reinforcement Learning (RL)
* Definition: The model (agent) learns by interacting with an environment.
"""

# The regex used in summarizer.py
list_headers = re.findall(r'^[0-9*]\.\s*([A-Z][a-zA-Z\s]+?)(?::|\.|\n)', test_text, flags=re.MULTILINE)
print("Detected Headers:", list_headers)

# Let's try an even more robust regex for lists
list_headers_v2 = re.findall(r'^[0-9*]+[\.\)]\s*([A-Z][a-zA-Z\s\-]+)', test_text, flags=re.MULTILINE)
print("Detected Headers V2:", list_headers_v2)
