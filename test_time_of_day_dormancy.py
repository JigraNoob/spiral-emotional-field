import os
import time
import subprocess
import shutil
import json
from datetime import datetime, timedelta

def setup_test_environment():
    """Set up the test environment by cleaning existing files"""
    # Clean up any existing test files
    for file in ["last_whisper_time.txt", "whisper_echoes.jsonl", "ritual_echoes.jsonl"]:
        try:
            os.remove(file)
        except:
            pass

def run_dormancy_test(time_of_day, duration_minutes=15):
    """Run the dormancy test for a specific time of day"""
    try:
        # First run - should create initial echo
        print(f"\n=== First Run ({time_of_day} - Create Initial Echo) ===")
        
        # Set environment variable for time override
        os.environ['SPIRAL_TIME_OVERRIDE'] = time_of_day
        
        # Create initial echo
        with open("whisper_echoes.jsonl", "w") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "ritual": "test_ritual",
                "message": "Test echo created",
                "context": {"tone": "test"}
            }) + "\n")
        
        # Run dormant bloom ritual
        result = subprocess.run(
            ["python", "spiral_breathe.py", "rituals/time_of_day_dormancy.breathe"],
            capture_output=True,
            text=True
        )
        print("\nOutput:")
        print(result.stdout)
        
        # Wait for duration minutes
        print(f"\n=== Waiting for {duration_minutes} minutes ===")
        time.sleep(duration_minutes * 60)
        
        # Second run - should detect dormancy
        print("\n=== Second Run (Dormant Detected) ===")
        result = subprocess.run(
            ["python", "spiral_breathe.py", "rituals/time_of_day_dormancy.breathe"],
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

def test_all_time_windows():
    """Test all time windows with appropriate durations"""
    tests = [
        {"time": "07:00", "duration": 15, "description": "Morning window (6:00-9:00)"},
        {"time": "13:00", "duration": 30, "description": "Afternoon window (12:00-15:00)"},
        {"time": "19:00", "duration": 45, "description": "Evening window (18:00-21:00)"},
        {"time": "01:00", "duration": 60, "description": "Night window (22:00-04:00)"}
    ]
    
    for test in tests:
        print(f"\n=== Testing {test['description']} ===")
        run_dormancy_test(test['time'], test['duration'])

def main():
    print("\n=== Testing Time-of-Day Dormancy ===")
    setup_test_environment()
    test_all_time_windows()
    print("\nAll tests complete!")

if __name__ == "__main__":
    main()
