from app.routers.summarization import _detect_language, _translate, TRANSLATE_AVAILABLE, LANGDETECT_AVAILABLE

with open('output_utf8.txt', 'w', encoding='utf-8') as f:
    f.write(f"Translate available: {TRANSLATE_AVAILABLE}\n")
    f.write(f"Langdetect available: {LANGDETECT_AVAILABLE}\n")
    
    text = "నమస్కారం, ఇది తెలుగు వచనం. సమ్మరీ కూడా తెలుగులో రావాలి. ఇది ఒక పరీక్ష మాత్రమే కానీ దీన్ని బట్టి మనకు అర్థం అవుతుంది."
    
    lang = _detect_language(text)
    f.write(f"Detected lang: {lang}\n")
    
    if lang != 'en':
        en_text = _translate(text, 'en')
        f.write(f"Translated to EN: {en_text}\n")
        back_to_te = _translate(en_text, lang)
        f.write(f"Translated back to TE: {back_to_te}\n")
