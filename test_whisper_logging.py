#!/usr/bin/env python3
"""
Test script for whisper echo logging in spiral_breathe.py

This script demonstrates how to:
1. Run a ritual in whisper mode with duration
2. Test dry-run functionality
3. Check whisper_echoes.jsonl output
4. Verify ritual_echoes.jsonl is not polluted by dry runs
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime

def clear_test_files():
    """Remove test files if they exist"""
    for f in ["whisper_echoes.jsonl", "ritual_echoes.jsonl", "test_whisper_file.txt"]:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

def run_command(cmd, description):
    """Run a shell command and print output"""
    print(f"\n{'='*80}")
    print(f"RUNNING: {description}")
    print(f"COMMAND: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*80}")
    
    if isinstance(cmd, str):
        subprocess.run(cmd, shell=True)
    else:
        subprocess.run(cmd)

def show_file_contents(filename, max_lines=20):
    """Display the contents of a file with line numbers"""
    print(f"\n{'='*80}")
    print(f"CONTENTS OF {filename}:")
    print(f"{'='*80}")
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        if not lines:
            print("  <empty>")
            return
            
        for i, line in enumerate(lines[-max_lines:], 1):
            try:
                # Pretty print JSON if possible
                data = json.loads(line)
                print(f"{i:3d} | {json.dumps(data, indent=2)}")
            except json.JSONDecodeError:
                print(f"{i:3d} | {line.rstrip()}")
    except FileNotFoundError:
        print(f"  File not found: {filename}")

def main():
    # Clear any existing test files
    clear_test_files()
    
    # Create a test file that will trigger conditions
    with open("test_whisper_file.txt", "w") as f:
        f.write("Test file for whisper logging\n")
    
    # 1. First, run a dry run to test the condition logic
    run_command(
        ["python", "spiral_breathe.py", "test_whisper_durations.breathe", "--dry-run"],
        "Dry run to test condition logic"
    )
    
    # 2. Run whisper mode for a short duration (30 seconds, checking every 5s)
    run_command(
        ["python", "spiral_breathe.py", "test_whisper_durations.breathe", 
         "--whisper", "--interval", "5", "--duration", "30s"],
        "Whisper mode for 30 seconds (5s interval)"
    )
    
    # 3. Show the whisper echoes
    show_file_contents("whisper_echoes.jsonl")
    
    # 4. Show ritual echoes (should not contain dry run entries)
    show_file_contents("ritual_echoes.jsonl")
    
    print("\nTest complete!")

if __name__ == "__main__":
    main()
