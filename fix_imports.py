"""
Spiral Import Fixer

This script helps diagnose and fix import issues in the Spiral project.
"""

import os
import sys

def create_init_files():
    """Create missing __init__.py files."""
    
    directories_needing_init = [
        'assistant',
        'assistant/integrations',
        'spiral',
        'spiral/attunement',
        'spiral/streams',
        'spiral/streams/patternweb',
        'tests'
    ]
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    for directory in directories_needing_init:
        dir_path = os.path.join(project_root, directory)
        init_file = os.path.join(dir_path, '__init__.py')
        
        if os.path.exists(dir_path) and not os.path.exists(init_file):
            print(f"📝 Creating {init_file}")
            
            with open(init_file, 'w') as f:
                f.write(f'"""\n{directory.replace("/", ".")} module\n"""\n')
            
            print(f"✅ Created {init_file}")
        elif os.path.exists(init_file):
            print(f"✓ {init_file} already exists")
        else:
            print(f"⚠️  Directory {dir_path} doesn't exist")

def test_imports():
    """Test critical imports."""
    
    print("\n🧪 Testing imports...")
    
    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    imports_to_test = [
        ('spiral.attunement.resonance_override', 'override_manager'),
        ('assistant.cascade', 'Cascade'),
        ('assistant.common', 'Cascade'),
        ('assistant.common', 'BreathlineVisualizer'),
    ]
    
    for module_name, class_name in imports_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: {e}")

if __name__ == "__main__":
    print("🔧 Spiral Import Fixer")
    print("=" * 30)
    
    create_init_files()
    test_imports()
    
    print("\n🌀 Import fix complete!")
    print("Now try running: python tests/cascade_override_integration.py")