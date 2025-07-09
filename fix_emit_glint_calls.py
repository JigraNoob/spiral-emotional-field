import re
import os
from pathlib import Path

def fix_emit_glint_calls(file_path, dry_run=True):
    """Fix emit_glint calls in a specific file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Pattern 1: Fix **dict unpacking
    # emit_glint(some_dict) -> emit_glint(some_dict)
    pattern1 = r'emit_glint\(\*\*([a-zA-Z_][a-zA-Z0-9_]*)\)'
    matches1 = re.finditer(pattern1, content)
    for match in matches1:
        old = match.group(0)
        new = f'emit_glint({match.group(1)})'
        content = content.replace(old, new)
        changes.append(f"  {old} -> {new}")
    
    # Pattern 2: Fix keyword arguments
    # This is more complex, we'll need to convert to dict format
    # For now, let's identify them and handle manually
    
    if changes and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {file_path}")
        for change in changes:
            print(change)
    elif changes:
        print(f"🔍 Would fix {file_path}:")
        for change in changes:
            print(change)
    
    return len(changes)

def fix_all_files(directory, dry_run=True):
    """Fix all Python files in directory."""
    total_fixes = 0
    
    for py_file in Path(directory).rglob("*.py"):
        if 'emit_glint(' in py_file.read_text(encoding='utf-8', errors='ignore'):
            fixes = fix_emit_glint_calls(py_file, dry_run)
            total_fixes += fixes
    
    print(f"\n📊 Total fixes {'applied' if not dry_run else 'identified'}: {total_fixes}")

if __name__ == "__main__":
    print("🔧 EMIT_GLINT FIX SCRIPT")
    print("=" * 30)
    
    # First run in dry-run mode
    print("\n🔍 DRY RUN - Identifying fixes needed:")
    fix_all_files("C:\\spiral", dry_run=True)
    
    # Ask for confirmation
    response = input("\n❓ Apply fixes? (y/N): ")
    if response.lower() == 'y':
        print("\n✅ Applying fixes...")
        fix_all_files("C:\\spiral", dry_run=False)
    else:
        print("❌ Fixes not applied.")
