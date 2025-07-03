import json
import time
import os

GLINT_STREAM_PATH = 'spiral/streams/patternweb/glint_stream.jsonl'

# Ensure the directory exists
os.makedirs(os.path.dirname(GLINT_STREAM_PATH), exist_ok=True)

# Sample glint data
glint = {
    "glint.id": f"test-glint-{int(time.time())}",
    "glint.timestamp": time.time(),
    "glint.hue": "cyan",
    "glint.intensity": 0.8,
    "glint.vector": {"from": "test", "to": "dashboard"},
    "soft.suggestion": "This is a test glint",
    "original_lint": "Test lint message",
    "context": {"toneform": "practical"}
}

# Append the glint to the file
with open(GLINT_STREAM_PATH, 'a') as f:
    json.dump(glint, f)
    f.write('\n')

print(f"Test glint appended to {GLINT_STREAM_PATH}")