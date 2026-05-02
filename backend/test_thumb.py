import easyocr
import time
from PIL import Image
import numpy as np

def test_fast_ocr(img_path):
    # Resize image small
    img = Image.open(img_path)
    img.thumbnail((400, 400))
    img_array = np.array(img.convert("RGB"))
    
    reader_en = easyocr.Reader(['en'], gpu=False, verbose=False)
    reader_te = easyocr.Reader(['te', 'en'], gpu=False, verbose=False)
    reader_hi = easyocr.Reader(['hi', 'en'], gpu=False, verbose=False)
    
    t0 = time.time()
    res_en = reader_en.readtext(img_array, detail=1)
    t1 = time.time()
    conf_en = sum([r[2] for r in res_en]) / len(res_en) if res_en else 0
    print(f"EN Time: {t1-t0:.2f}s, Conf: {conf_en:.4f}")
    
    t0 = time.time()
    res_te = reader_te.readtext(img_array, detail=1)
    t1 = time.time()
    conf_te = sum([r[2] for r in res_te]) / len(res_te) if res_te else 0
    print(f"TE Time: {t1-t0:.2f}s, Conf: {conf_te:.4f}")

    t0 = time.time()
    res_hi = reader_hi.readtext(img_array, detail=1)
    t1 = time.time()
    conf_hi = sum([r[2] for r in res_hi]) / len(res_hi) if res_hi else 0
    print(f"HI Time: {t1-t0:.2f}s, Conf: {conf_hi:.4f}")


import os
path = "static/uploads/042f9d2ef9e54863910ed0a54f53504a.png"
if os.path.exists(path):
    test_fast_ocr(path)
else:
    print("Not found")

