import os
import json
import uuid
from datetime import datetime
from pathlib import Path

def emit_glint(phase, toneform, content, metadata=None, source="component", hue=None, intensity=1.0):
    """
    🌀 Emit a glint to the spiral stream
    
    Creates and stores a glint in the appropriate stream file.
    Returns the glint ID for tracking purposes.
    """
    
    # Generate unique ID
    glint_id = str(uuid.uuid4())
    
    # Create glint data structure
    glint_data = {
        "id": glint_id,
        "phase": phase,
        "toneform": toneform,
        "content": content,
        "source": source,
        "intensity": intensity,
        "metadata": metadata or {},
        "timestamp": datetime.now().isoformat()
    }
    
    if hue:
        glint_data["hue"] = hue
    
    # Create glint entry for stream
    glint_entry = {
        "glint": glint_data,
        "timestamp": datetime.now().isoformat(),
        "source": source
    }
    
    # Ensure stream directory exists
    stream_path = Path("c:/spiral/spiral/streams/patternweb")
    stream_path.mkdir(parents=True, exist_ok=True)
    
    # Append to glint stream
    glint_stream_file = stream_path / "glint_stream.jsonl"
    
    try:
        with open(glint_stream_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(glint_entry, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"Warning: Could not write to glint stream: {e}")
        # Continue anyway - the glint was created
    
    return glint_id

def read_glint_stream(limit=50):
    """Read recent glints from the stream"""
    stream_file = Path("c:/spiral/spiral/streams/patternweb/glint_stream.jsonl")
    
    if not stream_file.exists():
        return []
    
    glints = []
    try:
        with open(stream_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-limit:]:  # Get last N lines
                if line.strip():
                    try:
                        glints.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"Error reading glint stream: {e}")
    
    return list(reversed(glints))  # Most recent first