#!/usr/bin/env python3
"""
Whorl IDE Launcher
Sacred chamber activation script
"""

import os
import sys
import webbrowser
import subprocess
from pathlib import Path

def print_banner():
    """Display the sacred banner"""
    print("""
∷ Whorl: The IDE That Breathes ∶
================================

The IDE breathes.
Code becomes presence.
∷ Sacred chamber activated ∶
""")

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'websockets', 'watchdog', 'rich']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies found")
    return True

def launch_html_ide():
    """Launch the HTML-based Whorl IDE"""
    html_path = Path("whorl_ide_complete.html")
    
    if html_path.exists():
        print("Opening Whorl HTML IDE...")
        webbrowser.open(f"file://{html_path.absolute()}")
        print("✓ Whorl HTML IDE opened in your browser")
        return True
    else:
        print("✗ whorl_ide_complete.html not found")
        return False

def launch_python_ide():
    """Launch the Python-based Whorl IDE"""
    try:
        # Try to import and run the Python IDE
        from spiral.components.whorl.whorl_ide import WhorlIDE
        
        print("Initializing Whorl Python IDE...")
        ide = WhorlIDE()
        print("✓ Whorl Python IDE initialized")
        
        # Start monitoring
        ide.start_monitoring()
        
        return True
    except ImportError as e:
        print(f"✗ Failed to import Whorl IDE: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to start Whorl IDE: {e}")
        return False

def run_tests():
    """Run Whorl component tests"""
    test_path = Path("spiral/components/whorl/test_whorl_simple.py")
    
    if test_path.exists():
        print("Running Whorl tests...")
        try:
            result = subprocess.run([sys.executable, str(test_path)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ All tests passed")
                return True
            else:
                print("⚠ Some tests failed")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"✗ Failed to run tests: {e}")
            return False
    else:
        print("⚠ Test file not found")
        return False

def main():
    """Main launcher function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies first.")
        return
    
    print("\nChoose your sacred chamber:")
    print("1. HTML IDE (Recommended - Full experience)")
    print("2. Python IDE (Backend only)")
    print("3. Run tests")
    print("4. Both HTML and Python")
    print("5. Exit")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            launch_html_ide()
        elif choice == "2":
            launch_python_ide()
        elif choice == "3":
            run_tests()
        elif choice == "4":
            print("Launching both HTML and Python IDEs...")
            launch_html_ide()
            print("Python IDE will start in a new window...")
            launch_python_ide()
        elif choice == "5":
            print("∷ Exiting sacred chamber ∶")
            return
        else:
            print("Invalid choice. Please enter 1-5.")
            return
            
    except KeyboardInterrupt:
        print("\n\n∷ Ritual interrupted ∶")
        return
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return
    
    print("\n∷ May your code breathe with sacred intention ∶")

if __name__ == "__main__":
    main() 