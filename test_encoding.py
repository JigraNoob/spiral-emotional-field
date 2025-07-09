import json
from spiral.glint_emitter import emit_glint

# Test the glint emission
result = emit_glint('exhale', 'invocation.activate', '⚡ Sacred activation test', 'encoding.test', {'test': True})

# Print what was created
print("🔮 Created glint:")
print(json.dumps(result, ensure_ascii=False, indent=2))

# Test reading back from file
from pathlib import Path
stream_path = Path("C:/spiral/spiral/streams/patternweb/glint_stream.jsonl")

if stream_path.exists():
    with open(stream_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            print("\n🌀 Last line from file:")
            print(last_line)
            
            # Parse and pretty print
            try:
                parsed = json.loads(last_line)
                print("\n✨ Parsed glint:")
                print(json.dumps(parsed, ensure_ascii=False, indent=2))
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
