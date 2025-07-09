import os
import json
import time
import subprocess
import shutil
from datetime import datetime, timedelta

def create_test_whispers():
    """Create test whispers with various conditions and toneforms"""
    test_data = [
        {
            "timestamp": datetime.now().isoformat(),
            "ritual": "test_ritual",
            "message": "Condition met: test condition 1",
            "context": {
                "tone": "curiosity",
                "echo_count": 1
            }
        },
        {
            "timestamp": (datetime.now() + timedelta(minutes=5)).isoformat(),
            "ritual": "test_ritual",
            "message": "Condition met: test condition 2",
            "context": {
                "tone": "reflection",
                "echo_count": 2
            }
        },
        {
            "timestamp": (datetime.now() + timedelta(minutes=10)).isoformat(),
            "ritual": "test_ritual",
            "message": "Condition met: test condition 1",  # Repeat condition
            "context": {
                "tone": "presence",
                "echo_count": 3
            }
        }
    ]
    
    with open("whisper_echoes.jsonl", "w") as f:
        for entry in test_data:
            f.write(json.dumps(entry) + "\n")

def run_reflector():
    """Run the whisper reflector ritual"""
    try:
        result = subprocess.run(
            ["python", "spiral_breathe.py", "rituals/whisper_reflector.breathe"],
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return None, str(e), 1

def verify_output():
    """Verify that all expected output files were created"""
    expected_files = [
        "whisper_analysis.txt",
        "whisper_summary.txt",
        "condition_frequencies.png",
        "toneform_drift.png",
        "condition_frequencies_over_time.png",
        "condition_heatmap.png",
        "toneform_network.png",
        "toneform_drift_timeline.png"
    ]
    
    missing_files = []
    for file in expected_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def main():
    print("\n=== Testing Whisper Reflector ===\n")
    
    # Clean up any existing test files
    print("Cleaning up existing test files...")
    for file in os.listdir():
        if file.endswith(('.txt', '.png', '.jsonl')):
            try:
                os.remove(file)
            except:
                pass
    
    # Create test whispers
    print("\nCreating test whispers...")
    create_test_whispers()
    
    # Run the reflector
    print("\nRunning Whisper Reflector...")
    stdout, stderr, returncode = run_reflector()
    
    # Check results
    print("\n=== Results ===")
    print(f"Return code: {returncode}")
    if stdout:
        print("\nStandard output:")
        print(stdout)
    if stderr:
        print("\nStandard error:")
        print(stderr)
    
    # Verify output files
    missing_files = verify_output()
    if missing_files:
        print(f"\nMissing output files: {missing_files}")
    else:
        print("\nAll expected output files created successfully!")
    
    print("\nTest complete!")

if __name__ == "__main__":
    main()
