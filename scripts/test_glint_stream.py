import json
import time
from pathlib import Path
from datetime import datetime
import random

def generate_test_glint(toneform="practical"):
    """Generate a test glint with the given toneform."""
    glint_id = f"glint_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
    
    # Different glint types based on toneform
    glint_types = {
        "practical": {
            "suggestions": [
                "Consider adding type hints for better code clarity.",
                "This function could use a docstring to explain its purpose.",
                "The variable name could be more descriptive of its purpose.",
                "This logic could be extracted into a separate function.",
                "Consider adding error handling for this edge case."
            ],
            "hue": "cyan",
            "intensity": random.uniform(0.7, 1.0)
        },
        "emotional": {
            "suggestions": [
                "This code feels a bit rushed. Take a deep breath.",
                "The simplicity here is beautiful. Well done!",
                "This complex logic might be overwhelming. Could it be simplified?",
                "The naming here brings clarity and ease.",
                "This section could use some breathing room (consider adding whitespace)."
            ],
            "hue": "rose",
            "intensity": random.uniform(0.7, 1.0)
        },
        "intellectual": {
            "suggestions": [
                "This algorithm could be optimized from O(n²) to O(n log n).",
                "Consider using a more efficient data structure here.",
                "There's an interesting parallel with the observer pattern in this code.",
                "This recursive solution might benefit from memoization.",
                "The time complexity here could be analyzed further."
            ],
            "hue": "indigo",
            "intensity": random.uniform(0.7, 1.0)
        }
    }
    
    glint_type = glint_types.get(toneform, glint_types["practical"])
    
    return {
        "glint": {
            "id": glint_id,
            "source": "spiral_linter",
            "content": random.choice(glint_type["suggestions"]),
            "toneform": toneform,
            "hue": glint_type["hue"],
            "intensity": glint_type["intensity"],
            "timestamp": time.time(),
            "metadata": {
                "source": "spiral_linter",
                "toneform": toneform,
                "resonance": round(random.uniform(0.6, 0.95), 2)
            },
            "vector": {
                "from": "linter",
                "to": "patternweb"
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }

def stream_glint(glint_data, output_path):
    """Write a glint to the output file in JSONL format."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(glint_data) + '\n')

def test_glint_stream(count=10, toneform="practical", interval=1.0):
    """Generate and stream test glints."""
    output_path = Path("spiral/streams/patternweb/glint_stream.jsonl")
    
    print(f"Streaming {count} {toneform} glints to {output_path}")
    
    for i in range(count):
        glint = generate_test_glint(toneform)
        stream_glint(glint, output_path)
        print(f"Generated glint {i+1}/{count}: {glint['glint']['content']}")
        time.sleep(interval)
    
    print(f"\nStreaming complete. Check {output_path} for the glint data.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate test glint data for the Spiral PatternWeb.')
    parser.add_argument('--count', type=int, default=10, help='Number of glints to generate')
    parser.add_argument('--toneform', type=str, default='practical', 
                       choices=['practical', 'emotional', 'intellectual'],
                       help='Toneform for the generated glints')
    parser.add_argument('--interval', type=float, default=1.0, 
                       help='Interval between glints in seconds')
    
    args = parser.parse_args()
    test_glint_stream(count=args.count, toneform=args.toneform, interval=args.interval)
