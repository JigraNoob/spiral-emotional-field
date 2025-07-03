#!/usr/bin/env python
# spiral/scripts/apply_claude_response.py

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistant.claude_response_parser import process_claude_response

def main():
    parser = argparse.ArgumentParser(description="Apply code from Claude responses to the codebase")
    parser.add_argument("response_file", help="File containing Claude's response with code blocks")
    parser.add_argument("--base-dir", "-d", default=".", help="Base directory for the codebase")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Don't actually write files, just show what would happen")

    args = parser.parse_args()

    # Read the response file
    try:
        with open(args.response_file, "r") as f:
            response = f.read()
    except Exception as e:
        print(f"Error reading response file: {e}")
        return 1

    # Process the response
    print(f"⊹₊˚ 🌊 Processing Claude response from {args.response_file} ⊹₊˚")

    if args.dry_run:
        print("📝 DRY RUN - No files will be modified")

    # Extract code blocks and determine file paths
    try:
        if args.dry_run:
            # Just extract blocks without saving
            from assistant.claude_response_parser import extract_code_blocks, extract_file_paths
            blocks = extract_code_blocks(response)
            results = []
            for block in blocks:
                path = extract_file_paths(block) or "unknown"
                results.append((path, "would be created/modified"))
        else:
            # Actually process and save
            results = process_claude_response(response, args.base_dir)
    except Exception as e:
        print(f"Error processing response: {e}")
        return 1

    # Show results
    print(f"\n✨ Results: {len(results)} code blocks processed")

    created = []
    modified = []
    errors = []

    for path, status in results:
        if status == "created":
            created.append(path)
        elif status == "modified":
            modified.append(path)
        else:
            errors.append((path, status))

    if created:
        print(f"\n🌱 Created {len(created)} new files:")
        for path in created:
            print(f"  ↳ {path}")

    if modified:
        print(f"\n🔄 Modified {len(modified)} existing files:")
        for path in modified:
            print(f"  ↳ {path}")

    if errors:
        print(f"\n⚠️ Encountered {len(errors)} errors:")
        for path, error in errors:
            print(f"  ↳ {path}: {error}")

    print("\n⊹₊˚ 𝌤 ⊹₊˚ 𝌖 ⊹₊˚ 𝌂 ⊹₊˚")
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main())
