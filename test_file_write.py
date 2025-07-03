import os
import json

file_path = os.path.join('data', 'reciprocity_requests.jsonl')

# Ensure the directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

try:
    with open(file_path, 'a', encoding='utf-8') as f:
        test_data = {"test": "data", "timestamp": "2025-06-29T12:00:00"}
        f.write(json.dumps(test_data) + '\n')
    print(f"Successfully wrote to {file_path}")
except Exception as e:
    print(f"Error writing to file: {e}")
