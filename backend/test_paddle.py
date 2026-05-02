import json
from paddleocr import PaddleOCR

# Load image
path = "static/uploads/5a217eecd91d4f87a0160b455513d63a.png"

# We must specify language depending on PaddleOCR's model. 'te' for Telugu.
ocr = PaddleOCR(use_angle_cls=True, lang="te") 
result = ocr.ocr(path)

# Format the results
text_res = "\n".join([line[1][0] for line in result[0]]) if result and result[0] else ""

with open("test_paddle.json", "w", encoding="utf-8") as f:
    json.dump({"paddle_te": text_res}, f, ensure_ascii=False, indent=2)
print("Saved to test_paddle.json")
