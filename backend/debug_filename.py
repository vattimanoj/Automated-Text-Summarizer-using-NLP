import re
import os

def get_safe_filename(filename: str) -> str:
    if not filename:
        return "unnamed_file"
    base, ext = os.path.splitext(filename)
    print(f"DEBUG: base={repr(base)}, ext={repr(ext)}")
    safe_base = re.sub(r'[^a-zA-Z0-9._-]', '_', base)
    print(f"DEBUG: safe_base after sub={repr(safe_base)}")
    stripped = safe_base.strip('_')
    print(f"DEBUG: stripped={repr(stripped)}")
    if not stripped:
        safe_base = "file"
        print(f"DEBUG: safe_base set to 'file'")
    return f"{safe_base}{ext}"

print(get_safe_filename("!@#$%^.png"))
print("-" * 20)
print(get_safe_filename("summary_தமிழ்_123.txt"))
