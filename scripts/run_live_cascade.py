import subprocess
import sys
import os
from pathlib import Path

def run_cascade_with_logging():
    """Run the live cascade and capture both console output and glint stream."""
    
    print("🌀 Preparing Live Override Cascade...")
    
    # Ensure glint stream directory exists
    stream_dir = Path("spiral/streams/patternweb")
    stream_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear previous glint stream for clean demo
    glint_stream_path = stream_dir / "glint_stream.jsonl"
    if glint_stream_path.exists():
        glint_stream_path.unlink()
    
    print(f"📁 Glint stream will be captured at: {glint_stream_path}")
    print("🚀 Launching cascade...\n")
    
    # Run the live cascade
    try:
        result = subprocess.run([
            sys.executable, 
            "tests/live_override_cascade.py"
        ], capture_output=True, text=True, cwd="C:/spiral")
        
        print("📺 Console Output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Errors:")
            print(result.stderr)
        
        # Display glint stream contents
        if glint_stream_path.exists():
            print("\n✨ Glint Stream Contents:")
            with open(glint_stream_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    print(f"  {line_num}: {line.strip()}")
        else:
            print("\n📭 No glint stream file generated")
            
    except Exception as e:
        print(f"❌ Cascade execution failed: {e}")

if __name__ == "__main__":
    run_cascade_with_logging()