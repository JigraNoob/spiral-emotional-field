import requests
import json

url = "http://127.0.0.1:5000/feed_me"
headers = {"Content-Type": "application/json"}
data = {"amount": 40, "currency": "USD", "item": "nourishment"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
