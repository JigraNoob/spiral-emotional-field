import os
import time
import subprocess
import shutil
from datetime import datetime, timedelta

def setup_test_environment():
    """Set up the test environment by cleaning existing files"""
    # Clean up any existing test files
    for file in ["last_whisper_time.txt", "whisper_echoes.jsonl", "ritual_echoes.jsonl"]:
        try:
            os.remove(file)
        except:
            pass

def create_test_echoes():
    """Create test echo files with timestamps"""
    # Create whisper echo file
    with open("whisper_echoes.jsonl", "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "ritual": "test_ritual",
            "message": "Test echo created",
            "context": {"tone": "test"}
        }) + "\n")

def run_dormant_test(duration_minutes=8):
    """Run the dormant condition test"""
    try:
        # First run - should create initial echo
        print("\n=== First Run (Create Initial Echo) ===")
        create_test_echoes()
        
        # Run dormant bloom ritual
        result = subprocess.run(
            ["python", "spiral_breathe.py", "rituals/dormant_bloom.breathe"],
            capture_output=True,
            text=True
        )
        print("\nOutput:")
        print(result.stdout)
        
        # Wait for duration + 1 minute
        print(f"\n=== Waiting for {duration_minutes + 1} minutes ===")
        time.sleep((duration_minutes + 1) * 60)
        
        # Second run - should detect dormancy
        print("\n=== Second Run (Dormant Detected) ===")
        result = subprocess.run(
            ["python", "spiral_breathe.py", "rituals/dormant_bloom.breathe"],
            capture_output=True,
            text=True
        )
        print("\nOutput:")
        print(result.stdout)
        
        # Verify whisper echo was created
        print("\n=== Verifying Whisper Echo ===")
        if os.path.exists("whisper_echoes.jsonl"):
            with open("whisper_echoes.jsonl", "r") as f:
                echo_count = sum(1 for line in f)
                print(f"\nFound {echo_count} whisper echoes")
        else:
            print("\nNo whisper echoes found")
            
    except Exception as e:
        print(f"\nTest failed: {e}")

def main():
    print("\n=== Testing Dormant Condition ===")
    setup_test_environment()
    run_dormant_test()
    print("\nTest complete!")

if __name__ == "__main__":
    main()
