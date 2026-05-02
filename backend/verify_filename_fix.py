import sys
import os

# Add the project root to sys.path to import app modules
sys.path.append(os.getcwd())

from app.utils import get_safe_filename

def run_test():
    test_cases = [
        ("தமிழ்_కోప్పు.png", "file.png"), # All non-ASCII, fallback to 'file'
        ("document.pdf", "document.pdf"), # Already safe
        ("space in name.jpg", "space_in_name.jpg"), # Spaces replaced by _
        ("!@#$%^.png", "file.png"), # Special chars only -> fallback to 'file'
    ]
    
    print("Running filename sanitization checks...\n")
    all_passed = True
    
    for original, expected in test_cases:
        result = get_safe_filename(original)
        if result == expected:
            print(f"PASS: {repr(original)} -> {repr(result)}")
        else:
            print(f"FAIL: {repr(original)} -> {repr(result)} (Expected: {repr(expected)})")
            all_passed = False
            
    # Special check for mixed case (variable number of underscores)
    mixed_original = "summary_தமிழ்_123.txt"
    mixed_result = get_safe_filename(mixed_original)
    if "summary" in mixed_result and "123" in mixed_result and all(ord(c) < 128 for c in mixed_result):
        print(f"PASS: {repr(mixed_original)} -> {repr(mixed_result)} (ASCII and contains keywords)")
    else:
        print(f"FAIL: {repr(mixed_original)} -> {repr(mixed_result)} (Should be ASCII and contain keywords)")
        all_passed = False

    if all_passed:
        print("\nAll verification checks PASSED!")
    else:
        print("\nSome verification checks FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
