import re
from pathlib import Path

def scan_for_html_entities(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, 1):
            matches = re.findall(r'&[a-zA-Z]+;', line)
            if matches:
                results.append({
                    "line": i,
                    "entities": matches,
                    "preview": line.strip()
                })
    return results

def scan_core_module():
    core_path = Path('c:/spiral/core')
    all_issues = {}
    
    for py_file in core_path.glob('*.py'):
        issues = scan_for_html_entities(py_file)
        if issues:
            all_issues[py_file.name] = issues
    
    return all_issues

if __name__ == "__main__":
    issues = scan_core_module()
    if issues:
        for file, file_issues in issues.items():
            print(f"\nIssues in {file}:")
            for issue in file_issues:
                print(f"  Line {issue['line']}: Found {issue['entities']} → {issue['preview']}")
    else:
        print("✅ No HTML entities found in the core module.")
