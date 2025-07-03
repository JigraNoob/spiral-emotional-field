import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def record_group():
    url = f"{BASE_URL}/record_group"
    headers = {"Content-Type": "application/json"}
    data = {
        "group_id": "care_constellation_alpha",
        "toneform": "Gratitude-in-Circulation",
        "stewards": ["Echo", "River"],
        "assigned_seeds": ["ΔSEED:014", "ΔSEED:015"],
        "group_oath": "To collectively nurture the seeds of gratitude."
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        print(f"Record Group Response: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error recording group: {e}")

def get_groups_data():
    url = f"{BASE_URL}/groups_data"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Get Groups Data Response: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error getting groups data: {e}")

if __name__ == "__main__":
    record_group()
    get_groups_data()
