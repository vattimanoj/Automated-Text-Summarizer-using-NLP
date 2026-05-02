import requests
import json

BASE_URL = "http://localhost:8000"
EMAIL = "manojvatti2004@gmail.com"
PASSWORD = "manoj123"

def test_flow():
    try:
        # 1. Login
        print("Logging in...")
        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={"email": EMAIL, "password": PASSWORD})
        if login_resp.status_code != 200:
            # Try form data if json fails (OAuth2 style)
            login_resp = requests.post(f"{BASE_URL}/api/auth/login", data={"username": EMAIL, "password": PASSWORD})
            
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.status_code} - {login_resp.text}")
            return
            
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Get initial stats
        print("Getting initial stats...")
        stats_resp = requests.get(f"{BASE_URL}/api/user/stats", headers=headers)
        initial_stats = stats_resp.json()
        print(f"Initial Stats: {initial_stats}")

        # 3. Summarize a text
        print("Summarizing text...")
        summ_resp = requests.post(
            f"{BASE_URL}/api/summarize/text",
            headers=headers,
            json={
                "text": "This is a test document to verify statistics. I hope it works and correctly updates the counts in the database for the current user.",
                "domain": "general",
                "max_length": 50,
                "min_length": 10
            }
        )
        if summ_resp.status_code != 200:
            print(f"Summarization failed: {summ_resp.text}")
            return
        print("Summarization successful.")

        # 4. Get final stats
        print("Getting final stats...")
        stats_resp = requests.get(f"{BASE_URL}/api/user/stats", headers=headers)
        final_stats = stats_resp.json()
        print(f"Final Stats: {final_stats}")

        # 5. Compare
        doc_diff = final_stats.get("documents_count", 0) - initial_stats.get("documents_count", 0)
        summ_diff = final_stats.get("summaries_count", 0) - initial_stats.get("summaries_count", 0)

        print(f"\nResults:")
        print(f"Documents increased by: {doc_diff}")
        print(f"Summaries increased by: {summ_diff}")

        if doc_diff >= 1 and summ_diff >= 1:
            print("\n✅ BACKEND IS WORKING CORRECTLY!")
        else:
            print("\n❌ BACKEND STATS DID NOT INCREASE!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_flow()
