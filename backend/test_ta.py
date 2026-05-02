from app.routers.summarization import _detect_language, _translate

with open('output_ta.txt', 'w', encoding='utf-8') as f:
    text = "இந்தியா (ஆங்கிலம்: India) என்பது தெற்காசியாவில் உள்ள ஒரு நாடு ஆகும். இது அதிகாரப்பூர்வமாக இந்தியக் குடியரசு என்று அழைக்கப்படுகிறது. பரப்பளவு அடிப்படையில் உலகின் ஏழாவது மிகப் பெரிய நாடும், மக்கள் தொகையின் அடிப்படையில் உலகில் முதலாமிடத்தைக் கொண்ட நாடும் இதுவாகும்."
    
    lang = _detect_language(text)
    f.write(f"Detected lang: {lang}\n")
    
    if lang != 'en':
        en_text = _translate(text, 'en')
        f.write(f"Translated to EN: {en_text}\n")
        back_to_ta = _translate(en_text, lang)
        f.write(f"Translated back to TA: {back_to_ta}\n")
