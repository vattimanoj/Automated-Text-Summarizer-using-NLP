import json
from deep_translator import GoogleTranslator

with open("_db.json", "r", encoding="utf-8") as f:
    data = json.load(f)

summary_en = data["summary"]

print(f"Len: {len(summary_en)}")
try:
    translator = GoogleTranslator(source='auto', target="te")
    chunk = summary_en[:500]
    res = translator.translate(chunk)
    with open("_db3.json", "w", encoding="utf-8") as f:
        json.dump({"res": res}, f, ensure_ascii=False)
except Exception as e:
    with open("_db3.json", "w", encoding="utf-8") as f:
        json.dump({"error": str(e)}, f, ensure_ascii=False)
