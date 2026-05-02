
import sys

def test_encoding():
    # Tamil text: "இந்தியா"
    tamil_text = "இந்தியா"
    
    print(f"Original Text: {tamil_text}")
    print("-" * 50)
    
    # Simulate saving in one encoding (UTF-8) and reading as ASCII
    try:
        bytes_data = tamil_text.encode('utf-8')
        decoded_ascii = bytes_data.decode('ascii', errors='replace')
        print(f"Read UTF-8 bytes as ASCII: {decoded_ascii}")
        
        # Simulate saving as latin-1 (which will replace characters with ?)
        bytes_latin1 = tamil_text.encode('latin-1', errors='replace')
        decoded_latin1 = bytes_latin1.decode('latin-1')
        print(f"Saved as latin-1 (replace) and read back: {decoded_latin1}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_encoding()
