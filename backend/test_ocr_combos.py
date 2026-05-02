import easyocr
import traceback

def test_langs(langs):
    try:
        print(f"Testing {langs}")
        reader = easyocr.Reader(langs, gpu=False, verbose=False)
        print("Success!")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

# Test combinations
test_langs(['en', 'te'])
test_langs(['en', 'hi'])
test_langs(['en', 'te', 'hi'])
test_langs(['en', 'te', 'hi', 'kn', 'bn', 'mr', 'pa'])
