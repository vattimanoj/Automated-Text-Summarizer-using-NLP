import asyncio
from app.routers.summarization import _translate, get_model

async def simulate():
    # 1. Simulate OCR extraction
    extracted_text = "గౌరివా ముస్తాఫుడు సింపోలు బోరాయా ఎసకం ఒరకం" # Random telugu snippet
    detected_lang = "te"
    
    # 4. Translate out
    text_for_summary = _translate(extracted_text, "en")
    print(f"EN Translated: {text_for_summary}")
    
    # 5. Summarize
    model = get_model()
    summary_en = model.summarize(text_for_summary, max_length=256, min_length=50)
    print(f"EN Summary: {summary_en}")
    
    # 6. Translate back
    summary_text = summary_en if detected_lang == "en" else _translate(summary_en, detected_lang)
    print(f"TE Summary: {summary_text}")

asyncio.run(simulate())
