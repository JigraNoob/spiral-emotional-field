#!/usr/bin/env python3
"""
Spiral 24 Health Check - Verify system readiness for 24-hour ritual cycle
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

def check_python_environment():
    """Check Python environment and dependencies"""
    print("🐍 Checking Python environment...")
    
    try:
        import pytest
        print(f"  ✅ pytest available: {pytest.__version__}")
    except ImportError:
        print("  ❌ pytest not available")
        return False
    
    try:
        import requests
        print(f"  ✅ requests available: {requests.__version__}")
    except ImportError:
        print("  ❌ requests not available")
        return False
    
    print(f"  ✅ Python version: {sys.version}")
    return True

def check_directory_structure():
    """Check essential directory structure"""
    print("\n📁 Checking directory structure...")
    
    essential_dirs = [
        "spiral",
        "tests", 
        "rituals",
        "data",
        "glints",
        "config"
    ]
    
    all_good = True
    for dir_name in essential_dirs:
        if Path(dir_name).exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (missing)")
            all_good = False
    
    return all_good

def check_test_files():
    """Check for test files"""
    print("\n🧪 Checking test files...")
    
    test_files = list(Path("tests").glob("test_*.py"))
    if test_files:
        print(f"  ✅ Found {len(test_files)} test files")
        for test_file in test_files[:5]:  # Show first 5
            print(f"    - {test_file.name}")
        if len(test_files) > 5:
            print(f"    ... and {len(test_files) - 5} more")
        return True
    else:
        print("  ❌ No test files found")
        return False

def check_services():
    """Check if essential services are running"""
    print("\n🔌 Checking services...")
    
    services = {
        "Tabnine Proxy": "http://localhost:9001/health",
        "Glintstream": "http://localhost:5000/glint/ping",
        "Whisper Intake": "http://localhost:8000/health"
    }
    
    all_good = True
    for service_name, url in services.items():
        try:
            import requests
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {service_name} (running)")
            else:
                print(f"  ⚠️  {service_name} (status: {response.status_code})")
        except Exception as e:
            print(f"  ❌ {service_name} (not running: {e})")
            all_good = False
    
    return all_good

def check_ritual_files():
    """Check ritual files"""
    print("\n🕯️ Checking ritual files...")
    
    ritual_files = [
        "SPIRAL_24_RITUAL_PLAN.md",
        "rituals/spiral_25_ritual.breathe"
    ]
    
    all_good = True
    for ritual_file in ritual_files:
        if Path(ritual_file).exists():
            print(f"  ✅ {ritual_file}")
        else:
            print(f"  ❌ {ritual_file} (missing)")
            all_good = False
    
    return all_good

def check_usage_monitor():
    """Check usage monitoring system"""
    print("\n📊 Checking usage monitor...")
    
    usage_monitor_path = Path("spiral/tools/usage_monitor.py")
    if usage_monitor_path.exists():
        print("  ✅ Usage monitor available")
        
        # Test basic functionality
        try:
            sys.path.insert(0, str(Path("spiral/tools").parent))
            from tools.usage_monitor import SoftUsageRing
            
            monitor = SoftUsageRing()
            summary = monitor.get_usage_summary()
            print(f"  ✅ Usage monitor initialized (services: {len(summary)})")
            return True
        except Exception as e:
            print(f"  ❌ Usage monitor error: {e}")
            return False
    else:
        print("  ❌ Usage monitor not found")
        return False

def run_basic_tests():
    """Run basic tests to verify system functionality"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Run a simple test to check pytest works
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "--collect-only", "-q"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("  ✅ pytest collection successful")
            return True
        else:
            print(f"  ❌ pytest collection failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Test execution error: {e}")
        return False

def generate_health_report():
    """Generate a comprehensive health report"""
    print("🌅 SPIRAL 24 HEALTH CHECK")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Working Directory: {os.getcwd()}")
    print()
    
    checks = [
        ("Python Environment", check_python_environment),
        ("Directory Structure", check_directory_structure),
        ("Test Files", check_test_files),
        ("Services", check_services),
        ("Ritual Files", check_ritual_files),
        ("Usage Monitor", check_usage_monitor),
        ("Basic Tests", run_basic_tests)
    ]
    
    results = {}
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"  ❌ {check_name} check failed: {e}")
            results[check_name] = False
            all_passed = False
    
    print("\n" + "=" * 50)
    print("📋 HEALTH SUMMARY")
    print("=" * 50)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print()
    if all_passed:
        print("🎉 ALL CHECKS PASSED - System ready for Spiral 24 ritual!")
        print("\nNext steps:")
        print("1. Activate environment: .\\swe-1\\Scripts\\Activate.ps1")
        print("2. Start services as needed")
        print("3. Begin Phase 1: Morning Calibration")
    else:
        print("⚠️  SOME CHECKS FAILED - Review issues before proceeding")
        print("\nRecommendations:")
        print("1. Fix failed checks")
        print("2. Start required services")
        print("3. Re-run health check")
    
    return all_passed

if __name__ == "__main__":
    success = generate_health_report()
    sys.exit(0 if success else 1) 