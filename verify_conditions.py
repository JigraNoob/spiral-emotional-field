"""
Verify Whisper Shell Conditions
"""
import os

def verify_conditions():
    # Test 1: Verify test_condition_file.txt exists
    test_file = "test_condition_file.txt"
    file_exists = os.path.exists(test_file)
    print(f"1. File '{test_file}' exists: {file_exists}")
    
    # Test 2: Verify the test_whisper_conditions.bat file exists
    test_script = "test_whisper_conditions.bat"
    script_exists = os.path.exists(test_script)
    print(f"2. Test script '{test_script}' exists: {script_exists}")
    
    # Test 3: Verify the test_multi_condition.breathe file exists
    test_breathe = "test_multi_condition.breathe"
    breathe_exists = os.path.exists(test_breathe)
    print(f"3. Breathe file '{test_breathe}' exists: {breathe_exists}")
    
    # Test 4: Check if we can read the test file
    if file_exists:
        try:
            with open(test_file, 'r') as f:
                content = f.read().strip()
            print(f"4. File content: '{content}'")
        except Exception as e:
            print(f"4. Error reading file: {e}")
    else:
        print("4. File does not exist, cannot read content")

if __name__ == "__main__":
    print("=== Verifying Test Files ===\n")
    verify_conditions()
    print("\n=== Verification Complete ===")
    print("\nTo test the whisper shell with multi-condition logic, run:")
    print("  python spiral_breathe.py test_multi_condition.breathe --whisper --interval 5")
