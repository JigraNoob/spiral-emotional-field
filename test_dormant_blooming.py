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

def run_dormant_blooming():
    """Run the dormant blooming ritual"""
    try:
        # First run - should create initial whisper time
        print("\n=== First Run (Initial Setup) ===")
        result = subprocess.run(
            ["python", "spiral_breathe.py", "rituals/dormant_blooming.breathe"],
            capture_output=True,
            text=True
        )
        print("\nOutput:")
        print(result.stdout)
        
        # Wait for longer than the silence threshold (300s)
        print("\n=== Waiting for silence threshold to be exceeded ===")
        time.sleep(305)  # 5 minutes + 5 seconds
        
        # Second run - should detect silence
        print("\n=== Second Run (Silence Detected) ===")
        result = subprocess.run(
            ["python", "spiral_breathe.py", "rituals/dormant_blooming.breathe"],
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
    print("\n=== Testing Dormant Blooming Ritual ===")
    setup_test_environment()
    run_dormant_blooming()
    print("\nTest complete!")

if __name__ == "__main__":
    main()
