
import requests
import sys

try:
    print("Checking CORS headers for http://localhost:8000/api/auth/login...")
    response = requests.options(
        "http://localhost:8000/api/auth/login",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for k, v in response.headers.items():
        if k.lower().startswith("access-control"):
            print(f"{k}: {v}")
            
    if response.headers.get("access-control-allow-credentials") == "true":
        print("\nSUCCESS: Access-Control-Allow-Credentials is true")
    else:
        print("\nFAILURE: Access-Control-Allow-Credentials is missing or not true")
        
except Exception as e:
    print(f"\nError: {e}")
    print("Make sure the backend server is running on port 8000.")
