"""
Run only the fixed attunement tests.
"""

import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_fixed_tests():
    """Run the fixed test suite."""
    print("🌿 Running Fixed Spiral Attunement Tests...")
    
    # Import test modules
    try:
        from tests.test_override_gate_fixed import TestOverrideGateFixed
        from tests.test_attunement_integration import TestAttunementIntegration
        print("✓ Loaded fixed test modules")
    except ImportError as e:
        print(f"✗ Failed to import test modules: {e}")
        return
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add fixed tests
    suite.addTest(unittest.makeSuite(TestOverrideGateFixed))
    suite.addTest(unittest.makeSuite(TestAttunementIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report results
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠ {len(result.failures)} failures, {len(result.errors)} errors")
        
        if result.failures:
            print("\nFAILURES:")
            for test, traceback in result.failures:
                print(f"FAIL: {test}")
                
        if result.errors:
            print("\nERRORS:")
            for test, traceback in result.errors:
                print(f"ERROR: {test}")

if __name__ == "__main__":
    run_fixed_tests()