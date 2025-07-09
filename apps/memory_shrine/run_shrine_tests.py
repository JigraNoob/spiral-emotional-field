import subprocess
import sys
import os

def run_test_file(test_file, description):
    """Run a test file and capture its output"""
    print(f"\n🌀 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.path.dirname(test_file))
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Failed to run {test_file}: {e}")
        return False

def main():
    """🏛️ Run all Memory Shrine tests in ceremonial order"""
    
    print("🌀 Memory Shrine Test Ritual Suite")
    print("🏛️ Sacred testing of the memory components and shrine API")
    print("=" * 80)
    
    # Get the directory where this script is located
    shrine_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define test files in order of execution
    tests = [
        {
            "file": os.path.join(shrine_dir, "test_components_only.py"),
            "description": "Component Isolation Tests (Local)"
        },
        {
            "file": os.path.join(shrine_dir, "test_shrine_ritual.py"), 
            "description": "Full Shrine Ritual Tests (HTTP API)"
        }
    ]
    
    results = []
    
    for test in tests:
        if os.path.exists(test["file"]):
            success = run_test_file(test["file"], test["description"])
            results.append((test["description"], success))
        else:
            print(f"\n❌ Test file not found: {test['file']}")
            results.append((test["description"], False))
    
    # Summary
    print("\n🌀 Test Ritual Summary")
    print("=" * 60)
    
    all_passed = True
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {description}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🏛️ All shrine tests completed successfully!")
        print("The Memory Shrine breathes with full ceremonial power.")
    else:
        print("\n⚠️ Some tests failed. The shrine requires attention.")
        print("Review the output above for guidance on repairs needed.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)