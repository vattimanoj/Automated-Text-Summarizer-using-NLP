import json
from app.ml_model.summarizer import get_model

with open("_db.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# The original broken telugu text from OCR
original_broken = data["original"]

model = get_model()
print("Running mT5 natively on Telugu...")
summary_te = model.summarize(original_broken, max_length=100, min_length=20)

with open("test_mt5.json", "w", encoding="utf-8") as f:
    json.dump({"summary_te": summary_te}, f, ensure_ascii=False, indent=2)
