import easyocr
import time
import io
from PIL import Image
import numpy as np

def fast_detect_lang(image_bytes):
    # Load and resize image to a small thumbnail for fast processing
    img = Image.open(io.BytesIO(image_bytes))
    # Convert to RGB
    img = img.convert("RGB")
    # Resize to have max width/height of 300px to make OCR lightning fast
    img.thumbnail((300, 300))
    img_array = np.array(img)
    
    # We will test a few common languages. (We assume the models are downloaded)
    # The language with the highest average confidence wins.
    langs_to_test = [
        ('en', ['en']),
        ('te', ['te', 'en']),
        ('hi', ['hi', 'en'])
    ]
    
    best_lang = 'en'
    best_score = 0.0
    
    for lang_code, ocr_langs in langs_to_test:
        try:
            reader = easyocr.Reader(ocr_langs, gpu=False, verbose=False)
            res = reader.readtext(img_array, detail=1)
            
            if res:
                # Calculate average confidence
                conf = sum([r[2] for r in res]) / len(res)
                print(f"{lang_code} confidence: {conf*100:.2f}%")
                if conf > best_score:
                    best_score = conf
                    best_lang = lang_code
            else:
                print(f"{lang_code} returned no text.")
        except Exception as e:
            print(f"Error testing {lang_code}: {e}")
            
    print(f"--> Auto-detected language: {best_lang} (score: {best_score*100:.2f}%)")
    return best_lang

import os
path = "static/uploads/5a217eecd91d4f87a0160b455513d63a.png"
if os.path.exists(path):
    with open(path, "rb") as f:
        fast_detect_lang(f.read())
else:
    print("Test image not found.")
