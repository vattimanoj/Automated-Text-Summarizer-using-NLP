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

test_langs(['en', 'te', 'hi'])
