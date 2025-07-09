#!/usr/bin/env python3
"""
Simple test runner for GlintOrchestrator tests.
"""

import sys
import os
import pytest

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def run_tests():
    """Run all GlintOrchestrator tests using pytest."""
    # Run pytest on the specific test file
    test_file = os.path.join(current_dir, "tests", "test_glint_orchestrator.py")
    
    # Set up pytest arguments
    pytest_args = [
        test_file,
        "-v",
        "--tb=short"
    ]
    
    # Run pytest
    exit_code = pytest.main(pytest_args)
    
    return exit_code == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 