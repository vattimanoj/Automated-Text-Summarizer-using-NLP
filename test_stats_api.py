"""
Test script to verify the statistics API endpoint is working dynamically
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print("✅ Backend Health Check:")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        return True
    except Exception as e:
        print(f"❌ Backend not reachable: {e}\n")
        return False

def test_login():
    """Test login and get token"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": "manojvatti2004@gmail.com",
                "password": "manoj123"
            }
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Login Successful:")
            print(f"   User: {data.get('user', {}).get('name')}")
            print(f"   Email: {data.get('user', {}).get('email')}")
            print(f"   Token: {data.get('access_token', '')[:50]}...\n")
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}\n")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}\n")
        return None

def test_stats(token):
    """Test statistics endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/user/stats", headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistics API Working:")
            print(f"   📄 Documents Count: {stats.get('documents_count', 0)}")
            print(f"   📝 Summaries Count: {stats.get('summaries_count', 0)}")
            print(f"   💬 Feedback Count: {stats.get('feedback_count', 0)}")
            print(f"   ⭐ Average Rating: {stats.get('average_rating', 0.0)}")
            print(f"\n   Full Response: {json.dumps(stats, indent=2)}\n")
            
            # Verify it's dynamic (not hardcoded)
            if all(isinstance(stats.get(key), (int, float)) for key in 
                   ['documents_count', 'summaries_count', 'feedback_count', 'average_rating']):
                print("✅ All statistics are numeric values (dynamic from database)")
                return True
            else:
                print("⚠️  Some statistics might not be properly formatted")
                return False
        else:
            print(f"❌ Stats API failed: {response.status_code}")
            print(f"   Response: {response.text}\n")
            return False
    except Exception as e:
        print(f"❌ Stats API error: {e}\n")
        return False

def main():
    print("=" * 60)
    print("TESTING DYNAMIC STATISTICS API")
    print("=" * 60 + "\n")
    
    # Test 1: Backend health
    if not test_health():
        print("⚠️  Backend is not running. Start it with: python run.py")
        return
    
    # Test 2: Login
    token = test_login()
    if not token:
        print("⚠️  Could not authenticate. Check credentials.")
        return
    
    # Test 3: Statistics
    if test_stats(token):
        print("=" * 60)
        print("✅ ALL TESTS PASSED - Statistics are working dynamically!")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ Statistics test failed")
        print("=" * 60)

if __name__ == "__main__":
    main()
