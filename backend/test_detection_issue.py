
from langdetect import detect, detect_langs

def test_detection():
    # Tamil text (India description)
    tamil_text = "இந்தியா (ஆங்கிலம்: India) என்பது தெற்காசியாவில் உள்ள ஒரு நாடாகும். இது அதிகாரப்பூர்వமாக இந்தியக் குடியரசு என்று அழைக்கப்படுகிறது."
    
    # Telugu text
    telugu_text = "భారతదేశం (ఆంగ్లం: India) అనేది దక్షిణాసియాలో ఉన్న ఒక దేశం. ఇది అధికారికంగా రిపబ్లిక్ ఆఫ్ ఇండియా అని పిలువబడుతుంది."
    
    print(f"Tamil Text: {tamil_text[:50]}...")
    try:
        print(f"  Detected: {detect(tamil_text)}")
        print(f"  Probs: {detect_langs(tamil_text)}")
    except Exception as e:
        print(f"  Error: {e}")
        
    print(f"\nTelugu Text: {telugu_text[:50]}...")
    try:
        print(f"  Detected: {detect(telugu_text)}")
        print(f"  Probs: {detect_langs(telugu_text)}")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    test_detection()
