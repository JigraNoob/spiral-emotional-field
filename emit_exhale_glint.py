import requests
import json

url = "http://localhost:5050/emit_glint"
headers = {"Content-Type": "application/json"}
data = {
    "phase": "exhale",
    "toneform": "glint",
    "source": "cli",
    "suggestion": "Exhale glint emitted from CLI."
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(f"Glint emission successful: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Error emitting glint: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response content: {e.response.text}")
