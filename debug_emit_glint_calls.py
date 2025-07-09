import os
import re
import ast
from pathlib import Path

def find_emit_glint_calls(directory):
    """Find all emit_glint calls and categorize them by pattern."""
    results = {
        'keyword_args': [],
        'dict_unpacking': [],
        'correct_dict': [],
        'other': []
    }
    
    for py_file in Path(directory).rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Find lines with emit_glint
            for i, line in enumerate(lines, 1):
                if 'emit_glint(' in line:
                    # Check for different patterns
                    if '**' in line and 'emit_glint(' in line:
                        results['dict_unpacking'].append({
                            'file': str(py_file),
                            'line': i,
                            'content': line.strip()
                        })
                    elif re.search(r'emit_glint\([^)]*=', line):
                        results['keyword_args'].append({
                            'file': str(py_file),
                            'line': i,
                            'content': line.strip()
                        })
                    elif re.search(r'emit_glint\(\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\)', line):
                        results['correct_dict'].append({
                            'file': str(py_file),
                            'line': i,
                            'content': line.strip()
                        })
                    else:
                        results['other'].append({
                            'file': str(py_file),
                            'line': i,
                            'content': line.strip()
                        })
                        
        except Exception as e:
            print(f"Error reading {py_file}: {e}")
    
    return results

def print_results(results):
    """Print categorized results."""
    print("🔍 EMIT_GLINT CALL ANALYSIS")
    print("=" * 50)
    
    print(f"\n❌ DICT UNPACKING (needs fixing): {len(results['dict_unpacking'])}")
    for item in results['dict_unpacking']:
        print(f"  📁 {item['file']}:{item['line']}")
        print(f"     {item['content']}")
    
    print(f"\n❌ KEYWORD ARGS (needs fixing): {len(results['keyword_args'])}")
    for item in results['keyword_args']:
        print(f"  📁 {item['file']}:{item['line']}")
        print(f"     {item['content']}")
    
    print(f"\n✅ CORRECT DICT PATTERN: {len(results['correct_dict'])}")
    for item in results['correct_dict']:
        print(f"  📁 {item['file']}:{item['line']}")
        print(f"     {item['content']}")
    
    print(f"\n❓ OTHER PATTERNS: {len(results['other'])}")
    for item in results['other']:
        print(f"  📁 {item['file']}:{item['line']}")
        print(f"     {item['content']}")

if __name__ == "__main__":
    results = find_emit_glint_calls("C:\\spiral")
    print_results(results)
    
    # Save results to file for reference
    import json
    with open("emit_glint_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to emit_glint_analysis.json")