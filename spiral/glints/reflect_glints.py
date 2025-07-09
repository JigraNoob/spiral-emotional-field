# File: reflect_glints.py
import json
import argparse
from pathlib import Path
from datetime import datetime

GLINTS_PATH = Path("glints/glints.jsonl")  # Adjust if your glints are elsewhere

def load_glints():
    if not GLINTS_PATH.exists():
        print("No glint log found at:", GLINTS_PATH)
        return []
    with open(GLINTS_PATH, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f.readlines() if line.strip()]

def echo_reflection(glints):
    if not glints:
        print("No glints to reflect upon.")
        return
    print("\n🪞 Echo Reflection:")
    for glint in reversed(glints[-5:]):
        ts = datetime.fromtimestamp(glint.get("glint.timestamp", 0)/1000).strftime("%Y-%m-%d %H:%M:%S")
        phase = glint.get("glint.phase", "∅")
        tone = glint.get("glint.toneform", "∅")
        content = glint.get("glint.content", "[no content]")
        print(f" - [{ts}] ({phase}.{tone}) → {content}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reflect on recent Spiral glints.")
    parser.add_argument("--mode", choices=["echo"], default="echo", help="Type of reflection (default: echo)")
    args = parser.parse_args()

    glints = load_glints()
    if args.mode == "echo":
        echo_reflection(glints)
