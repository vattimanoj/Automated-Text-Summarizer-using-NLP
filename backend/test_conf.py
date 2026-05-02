import easyocr
import time

def check_confidence(img_path):
    print(f"Testing {img_path}")
    
    # Init en
    reader_en = easyocr.Reader(['en'], gpu=False, verbose=False)
    res_en = reader_en.readtext(img_path, detail=1)
    conf_en = sum([r[2] for r in res_en]) / len(res_en) if res_en else 0
    
    # Init te
    reader_te = easyocr.Reader(['en', 'te'], gpu=False, verbose=False)
    res_te = reader_te.readtext(img_path, detail=1)
    conf_te = sum([r[2] for r in res_te]) / len(res_te) if res_te else 0
    
    print(f"EN confidence: {conf_en:.4f}, TE confidence: {conf_te:.4f}")
    print(f"EN text sample: {[r[1] for r in res_en[:3]]}")
    print(f"TE text sample: {[r[1] for r in res_te[:3]]}")

import os
path = "static/uploads/042f9d2ef9e54863910ed0a54f53504a.png"
if os.path.exists(path):
    check_confidence(path)
else:
    print("Not found")

