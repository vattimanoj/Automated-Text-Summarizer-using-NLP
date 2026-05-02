
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.getcwd())

from app.routers.summarization import _detect_language

def test_detection():
    # Tamil text (India description)
    tamil_text = "இந்தியா (ஆங்கிலம்: India) என்பது தெற்காசியாவில் உள்ள ஒரு நாடாகும். இது அதிகாரப்பூர்வமாக இந்தியக் குடியரசு என்று அழைக்கப்படுகிறது."
    
    # Telugu text
    telugu_text = "భారతదేశం (ఆంగ్లం: India) అనేది దక్షిణాసియాలో ఉన్న ఒక దేశం. ఇది అధికారికంగా రిపబ్లిక్ ఆఫ్ ఇండియా అని పిలువబడుతుంది."
    
    # Hindi text
    hindi_text = "भारत (अंग्रेज़ी: India) दक्षिण एशिया में स्थित एक देश है। इसे आधिकारिक तौर पर भारतीय गणराज्य कहा जाता है।"

    print(f"Tamil Text: {tamil_text[:50]}...")
    print(f"  Detected: {_detect_language(tamil_text)}")
        
    print(f"\nTelugu Text: {telugu_text[:50]}...")
    print(f"  Detected: {_detect_language(telugu_text)}")

    print(f"\nHindi Text: {hindi_text[:50]}...")
    print(f"  Detected: {_detect_language(hindi_text)}")

if __name__ == "__main__":
    test_detection()
