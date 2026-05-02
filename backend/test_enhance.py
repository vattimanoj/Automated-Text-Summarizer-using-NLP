import easyocr
import io
import numpy as np
import json
from PIL import Image, ImageEnhance, ImageOps

path = "static/uploads/5a217eecd91d4f87a0160b455513d63a.png"

# Normal extraction
img_normal = np.array(Image.open(path).convert("RGB"))
reader = easyocr.Reader(['te', 'en'], gpu=False, verbose=False)
res_normal = reader.readtext(img_normal, detail=0, paragraph=True)

# Enhanced extraction
img = Image.open(path).convert("RGB")
img = ImageOps.grayscale(img)
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.5) # High Contrast
img_enh = np.array(img.convert("RGB"))  # EasyOCR expects 3 channels
res_enh = reader.readtext(img_enh, detail=0, paragraph=True)

out = {
    "normal": "\n".join(res_normal).strip(),
    "enhanced": "\n".join(res_enh).strip()
}

with open("test_enhance.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
