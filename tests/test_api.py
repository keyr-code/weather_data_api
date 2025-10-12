import requests
import json

BASE_URL = "http://localhost:5000"

def test_api():
    """Test API endpoints"""
    
    # Get all locations
    print("=== GET /weather/locations ===")
    response = requests.get(f"{BASE_URL}/weather/locations")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Get current weather for Tokyo
    print("=== GET /weather/current/Tokyo ===")
    response = requests.get(f"{BASE_URL}/weather/current/Tokyo")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Get historical weather for London
    print("=== GET /weather/historical/London?limit=10 ===")
    response = requests.get(f"{BASE_URL}/weather/historical/London", params={"limit": 10})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure Flask app is running on localhost:5000")
        print("Run: python main.py")