import os
import sys
import codecs
from pathlib import Path

# Ensure stdout handles UTF-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def check_spiral_structure():
    """Diagnose the current Spiral module structure"""
    
    base_path = Path(__file__).parent
    
    # Check critical paths
    paths_to_check = [
        'assistant',
        'assistant/__init__.py',
        'assistant/integrations',
        'assistant/integrations/__init__.py',
        'assistant/integrations/tabnine_bridge.py',
        'assistant/cascade.py',
        'assistant/haret_integration.py'
    ]
    
    print("🌀 Spiral Structure Diagnosis:")
    print("=" * 40)
    
    for path in paths_to_check:
        full_path = base_path / path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"{status} {path}")
        
        if exists and full_path.is_file():
            try:
                size = full_path.stat().st_size
                print(f"    📏 {size} bytes")
            except:
                pass
    
    print("\n🔍 Python Path:")
    import sys
    for i, path in enumerate(sys.path[:5]):  # Show first 5 paths
        print(f"  {i}: {path}")
    
    print(f"\n📍 Current working directory: {os.getcwd()}")
    print(f"📍 Script location: {base_path}")

if __name__ == "__main__":
    check_spiral_structure()