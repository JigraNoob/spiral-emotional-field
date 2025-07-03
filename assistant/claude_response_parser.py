# spiral/assistant/claude_response_parser.py

import re
from typing import Dict, List, Optional, Tuple
import os

def extract_code_blocks(response: str) -> List[Dict[str, str]]:
    """
    Extract code blocks from a Claude response.
    Returns a list of dictionaries with 'language' and 'code' keys.
    """
    # Pattern to match markdown code blocks: ```language\ncode\n```
    pattern = r'```([^\n]*)\n([\s\S]*?)\n```'

    # Find all code blocks
    matches = re.findall(pattern, response)

    # Process each match into a dictionary
    code_blocks = []
    for lang, code in matches:
        code_blocks.append({
            'language': lang.strip(),
            'code': code.strip()
        })

    return code_blocks

def extract_file_paths(code_block: Dict[str, str]) -> Optional[str]:
    """
    Try to determine a file path from a code block based on comments or imports.
    Returns None if no path can be determined.
    """
    code = code_block['code']
    language = code_block['language']

    # Look for specific path indicators
    path_patterns = [
        # Common format: # spiral/path/to/file.py
        r'#\s*(?:spiral/)?([\w/]+\.\w+)',
        # File path mentioned in docstring
        r'"""[\s\S]*?(?:spiral/)?([\w/]+\.\w+)[\s\S]*?"""',
        # File path in a more explicit comment
        r'#\s*File:\s*(?:spiral/)?([\w/]+\.\w+)'
    ]

    for pattern in path_patterns:
        match = re.search(pattern, code)
        if match:
            return match.group(1)

    # Try to infer from language
    if language == 'python':
        # Look for main class or function name
        class_match = re.search(r'class\s+(\w+)', code)
        if class_match:
            return f"{class_match.group(1).lower()}.py"

        # Look for main function
        func_match = re.search(r'def\s+(\w+)', code)
        if func_match and func_match.group(1) != '__init__':
            return f"{func_match.group(1).lower()}.py"

    # For JavaScript files
    elif language in ['javascript', 'js']:
        class_match = re.search(r'class\s+(\w+)', code)
        if class_match:
            return f"static/js/{class_match.group(1).lower()}.js"

    # No path could be determined
    return None

def save_code_blocks(code_blocks: List[Dict[str, str]], base_dir: str = ".") -> List[Tuple[str, str]]:
    """
    Save extracted code blocks to appropriate files.
    Returns a list of (filepath, status) tuples.

    Status can be 'created', 'modified', or 'error'.
    """
    results = []

    for block in code_blocks:
        # Try to determine a path
        path = extract_file_paths(block)

        if not path:
            # Skip blocks without a determinable path
            results.append(("unknown", "error: no path determined"))
            continue

        # Ensure the path is relative to the base directory
        if path.startswith('/'):
            path = path[1:]

        full_path = os.path.join(base_dir, path)

        # Make sure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Check if we're creating or modifying
        status = "created" if not os.path.exists(full_path) else "modified"

        try:
            with open(full_path, 'w') as f:
                f.write(block['code'])
            results.append((full_path, status))
        except Exception as e:
            results.append((full_path, f"error: {str(e)}"))

    return results

def process_claude_response(response: str, base_dir: str = ".") -> List[Tuple[str, str]]:
    """
    Process a full Claude response:
    1. Extract code blocks
    2. Save them to appropriate files
    3. Return results
    """
    # Find the replicable marker
    replicable_marker = "Exhale.Response.Replicable"

    if replicable_marker in response:
        # Only process code blocks after the marker
        response_parts = response.split(replicable_marker, 1)
        if len(response_parts) > 1:
            response = response_parts[1]

    # Extract and save code blocks
    code_blocks = extract_code_blocks(response)
    return save_code_blocks(code_blocks, base_dir)

# Command-line interface
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Extract and save code blocks from Claude responses')
    parser.add_argument('input_file', help='Path to file containing Claude response')
    parser.add_argument('--base-dir', '-d', default=".", help='Base directory for saving files')

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            response = f.read()

        results = process_claude_response(response, args.base_dir)

        print(f"Processed {len(results)} code blocks:")
        for path, status in results:
            print(f"  {status}: {path}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
