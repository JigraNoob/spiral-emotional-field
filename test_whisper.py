"""
Test script for Whisper Shell conditions
"""
import os
import sys
import time
from datetime import datetime, timedelta

def create_test_file(filename, content):
    """Helper to create test files"""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created test file: {filename}")

def test_conditions():
    """Test various condition combinations"""
    print("=== Testing Whisper Shell Conditions ===\n")
    
    # Create a test file for file existence check
    test_filename = "test_whisper_file.txt"
    create_test_file(test_filename, "Test content for whisper conditions")
    
    # Test 1: File exists condition
    print("\n--- Test 1: File Exists ---")
    condition = f'exists: {test_filename}'
    print(f"Condition: {condition}")
    # This would be handled by the whisper shell
    if os.path.exists(test_filename):
        print("✅ Condition met: File exists")
    else:
        print("❌ Condition not met: File does not exist")
    
    # Test 2: Time condition (next minute)
    print("\n--- Test 2: Time Condition ---")
    next_minute = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    condition = f'time {next_minute} and exists: {test_filename}'
    print(f"Condition: {condition}")
    print("This condition will be true at {next_minute} if the file exists")
    
    # Test 3: RITUAL_ECHO_COUNT condition
    print("\n--- Test 3: Echo Count Condition ---")
    condition = 'RITUAL_ECHO_COUNT > 0 and RITUAL_ECHO_COUNT < 10'
    print(f"Condition: {condition}")
    print("This would be true if there are between 1-9 ritual echoes")
    
    # Test 4: Tone condition
    print("\n--- Test 4: Tone Condition ---")
    tone = "gratitude"
    condition = f'tone == "{tone}" and exists: {test_filename}'
    print(f"Condition: {condition}")
    print(f"This would be true if tone is '{tone}' and the file exists")
    
    print("\n=== Test Script Complete ===")
    print("To test actual whisper behavior, run:")
    print("  python spiral_breathe.py test_multi_condition.breathe --whisper --interval 5")

if __name__ == "__main__":
    test_conditions()
