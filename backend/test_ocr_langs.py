import easyocr
try:
    reader = easyocr.Reader(['en', 'te', 'hi', 'ta'], gpu=False, verbose=False)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
