
import re

def test_extraction_v2():
    with open('user_test_text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. Cleaner Overview extraction (just for logic check)
    overview_text = text.split('\n\n')[0]
    print(f"DEBUG OVERVIEW TARGET: {overview_text[:100]}...")

    # 2. Section aware headers
    # Find headers with their numbers to avoid overlap
    headers = re.findall(r'^([0-9]+\.\s*)([A-Z][a-zA-Z\s\-\(\)]+?)(?::|\.|\n)', text, flags=re.MULTILINE)
    
    for prefix, cat in headers:
        print(f"\n--- PROCESSING: {prefix}{cat} ---")
        escaped_prefix = re.escape(prefix)
        escaped_cat = re.escape(cat)
        
        # Block search using prefix
        block_pattern = rf"^{escaped_prefix}{escaped_cat}.*?\n(.*?)(?=\n[0-9]+\.|\Z)"
        block_match = re.search(block_pattern, text, re.DOTALL | re.MULTILINE)
        
        if block_match:
            block = block_match.group(1).strip()
            # print(f"DEBUG BLOCK: {block[:50]}...")
            
            # Extract Definition
            # Strategy: Look for 'Definition:' or ':' OR just take first sentence
            def_match = re.search(r'(?:Definition:|:)\s*(.*?)(?:\.|\n)', block, re.IGNORECASE)
            if def_match:
                definition = def_match.group(1).strip()
            else:
                # Take first sentence as definition
                sentences = re.split(r'\.\s+', block)
                definition = sentences[0].strip() if sentences else ""
            
            print(f"DEFINITION: {definition}")
            
            # Extract Subtypes
            # Look for lines starting with - and having a name: or just titles
            # The text has "Subtypes of Supervised Learning:" header sometimes
            sub_sections = re.findall(r'^- ([A-Za-z\s]+):\s*\n*(.*?)(?=\n- |\n[A-Z][a-z]+:|\Z)', block, re.DOTALL | re.MULTILINE)
            
            if sub_sections:
                print("SUBTYPES FOUND:")
                for sub_name, sub_desc in sub_sections:
                    # Clean sub_desc (take first sentence)
                    first_sent = re.split(r'\.\s+', sub_desc.strip())[0]
                    print(f"  * {sub_name.strip()}: {first_sent.strip()}")
            else:
                # Fallback to old example extraction
                ex_match = re.search(r'(?:Examples|Sub-types):\s*(.*?)(?:\n\n|\Z)', block, re.DOTALL | re.IGNORECASE)
                if ex_match:
                    print(f"EXAMPLES FALLBACK: {ex_match.group(1).strip()}")

if __name__ == "__main__":
    import sys
    with open('regex_v2.log', 'w', encoding='utf-8') as f:
        sys.stdout = f
        test_extraction_v2()
