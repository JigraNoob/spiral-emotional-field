#!/usr/bin/env python3
"""
Test runner for the Spiral Tabnine Proxy.

This script runs both unit and integration tests with appropriate configurations.
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def setup_test_environment():
    """Set up the test environment."""
    # Create test data directory if it doesn't exist
    test_data_dir = Path("tests/data")
    test_data_dir.mkdir(exist_ok=True)
    
    # Set environment variables for testing
    os.environ["SPIRAL_ENV"] = "test"
    os.environ["PYTHONPATH"] = os.getcwd()

def run_tests():
    """Run all tests."""
    setup_test_environment()
    
    print("\n🔍 Running unit tests...")
    unit_result = subprocess.run(
        ["pytest", "tests/test_proxy.py", "-v", "--cov=tabnine_proxy", "--cov-report=term-missing"],
        capture_output=True,
        text=True
    )
    
    print("\n🌐 Running integration tests...")
    integration_result = subprocess.run(
        ["pytest", "tests/integration/", "-v", "--cov-append", "--cov=tabnine_proxy", "--cov-report=term-missing"],
        capture_output=True,
        text=True
    )
    
    # Print test results
    print("\n📊 Test Results:")
    print("-" * 40)
    print("Unit Tests:")
    print(unit_result.stdout)
    if unit_result.stderr:
        print("Unit Test Errors:", unit_result.stderr)
    
    print("\nIntegration Tests:")
    print(integration_result.stdout)
    if integration_result.stderr:
        print("Integration Test Errors:", integration_result.stderr)
    
    # Exit with appropriate code
    if unit_result.returncode != 0 or integration_result.returncode != 0:
        print("❌ Some tests failed.")
        sys.exit(1)
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    run_tests()
