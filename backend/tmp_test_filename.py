import os
import uuid
import sys

def test_filename_handling(filename):
    # Set encoding for output just in case
    # This might fail if the terminal doesn't support it
    print(f"Testing filename: {repr(filename)}")
    try:
        # Simulate extension extraction
        ext = os.path.splitext(filename or "image.png")[1] or ".png"
        print(f"Extracted extension: {ext}")
        
        # Simulate UUID filename generation
        img_filename = f"{uuid.uuid4().hex}{ext}"
        print(f"Generated physical filename: {img_filename}")
        
        # Simulate path joining
        upload_dir = "static/uploads"
        img_path = os.path.join(upload_dir, img_filename)
        print(f"Full path: {img_path}")
        
        print("Success for this filename.")
    except Exception as e:
        print(f"Failed for {filename}: {e}")

if __name__ == "__main__":
    # Test with Tamil name
    test_filename_handling("தமிழ்_கோப்பு.png")
    print("-" * 20)
    # Test with mixed characters
    test_filename_handling("summary_தமிழ்_123.txt")
