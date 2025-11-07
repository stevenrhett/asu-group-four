"""Quick test to check if search route works"""
import requests

# Test health
print("Testing health endpoint...")
r = requests.get("http://localhost:8000/health")
print(f"Health: {r.status_code} - {r.json()}")

# Test regular jobs
print("\nTesting regular jobs endpoint...")
r = requests.get("http://localhost:8000/api/v1/jobs/?limit=1")
print(f"Jobs: {r.status_code} - Found {len(r.json())} jobs")

# Test search
print("\nTesting search endpoint...")
try:
    r = requests.get("http://localhost:8000/api/v1/jobs/search?page_size=1")
    print(f"Search: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Error: {e}")

