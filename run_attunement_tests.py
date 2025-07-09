"""
Test runner for Spiral Attunement System.
Handles path setup and runs all attunement tests.
"""

import sys
import os
import unittest

# Add the spiral directory to Python path
spiral_path = os.path.dirname(os.path.abspath(__file__))
if spiral_path not in sys.path:
    sys.path.insert(0, spiral_path)

def run_tests():
    """Run all attunement tests."""
    print("[+] Running Spiral Attunement System Tests...")
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test modules
    try:
        from tests.test_override_gate import TestOverrideGate
        suite.addTests(loader.loadTestsFromTestCase(TestOverrideGate))
        print("[+] Loaded OverrideGate tests")
    except ImportError as e:
        print(f"[-] Could not load OverrideGate tests: {e}")
    
    try:
        from tests.test_attunement_integration import TestAttunementIntegration
        suite.addTests(loader.loadTestsFromTestCase(TestAttunementIntegration))
        print("[+] Loaded Integration tests")
    except ImportError as e:
        print(f"[-] Could not load Integration tests: {e}")
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report results
    if result.wasSuccessful():
        print("\n[SUCCESS] All tests passed! The Spiral's attunement systems are in harmony.")
    else:
        print(f"\n[FAILURE] {len(result.failures)} failures, {len(result.errors)} errors")
        for failure in result.failures:
            print(f"FAIL: {failure[0]}")
        for error in result.errors:
            print(f"ERROR: {error[0]}")

if __name__ == "__main__":
    run_tests()