"""
Test script for the Spiral Linter Companion.

This script demonstrates how to use the Spiral Linter to analyze code
with different toneforms and styles.
"""
import os
import sys
import json
from typing import List
from spiral.glints.linter import lint_code

def print_suggestion(suggestion: dict, code_lines: List[str] = None) -> None:
    """Print a suggestion in a formatted way."""
    print(f"\n🔍 [{suggestion.get('toneform', 'UNKNOWN').upper()}] {suggestion.get('guidance', 'Suggestion')}")
    print(f"   Location: Line {suggestion['line']}, Col {suggestion['column']}")
    print(f"   Code: {suggestion['code']} - {suggestion['message']}")
    
    # Show the relevant code snippet if available
    if code_lines and 0 <= suggestion['line'] - 1 < len(code_lines):
        line_num = suggestion['line']
        line = code_lines[line_num - 1].rstrip()
        print(f"   {line_num}: {line}")
        # Show pointer to the column
        print(f"   {' ' * (len(str(line_num)) + 2 + suggestion['column'] - 1)}^")
    
    # Show additional context if available
    if suggestion.get('context'):
        print(f"   Context: {suggestion['context']}")
        
    # Show resonance information if available
    if 'resonance' in suggestion:
        print(f"   Resonance: {suggestion['resonance']:.2f}")
    if 'hue' in suggestion and 'intensity' in suggestion:
        print(f"   Hue: {suggestion['hue']}, Intensity: {suggestion['intensity']:.2f}")

def test_linter():
    """Test the Spiral Linter with different code examples and toneforms."""
    # Example code with various intentional issues
    test_code = """
# Missing module docstring

def calculate(a, b):
    # Missing docstring
    return a + b  # Simple addition

class Test:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1  # Could use += 1
        return self.value
    
    def unused_method(self):
        pass  # Never used

# Line with trailing whitespace:    
x = 5  

too_many_newlines = True
"""
    
    # Save test code to a temporary file for inspection
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    print(f"Test code saved to: {temp_file}")
    
    # Print the test code for reference
    print("\n=== Test Code ===")
    for i, line in enumerate(test_code.split('\n'), 1):
        print(f"{i:3d}: {line}")
    print("================\n")

    # Test with different toneforms
    toneforms = ["practical", "emotional", "intellectual", "spiritual", "relational"]
    
    for tone in toneforms:
        print(f"\n{'='*50}")
        print(f"TESTING WITH TONEFORM: {tone.upper()}")
        print(f"{'='*50}")
        
        # Analyze the code
        print(f"\n{'='*20} Analyzing with toneform: {tone} {'='*20}")
        
        # First try with file path
        print("\n=== Trying with file path ===")
        result = lint_code("", toneform=tone, style="gentle", filepath=temp_file)
        
        if not result.get('suggestions'):
            # If no suggestions with file path, try with direct code
            print("\n=== No suggestions with file path, trying with direct code ===")
            result = lint_code(test_code, toneform=tone, style="gentle")
        
        # Print raw result for debugging
        print("\n=== Raw Result ===")
        print(f"Status: {result.get('status')}")
        print(f"Issues found: {result.get('issues_found', 0)}")
        print(f"Suggestions: {len(result.get('suggestions', []))}")
        if 'glint' in result and result['glint']:
            print(f"Glint resonance: {result['glint'].get('resonance', 0):.2f}")
        
        # Split the code into lines for context
        code_lines = test_code.split('\n')
        
        # Print results
        print(f"\nAnalysis complete. Found {len(result['suggestions'])} suggestions.")
        if 'glint' in result and result['glint'] and 'resonance' in result['glint']:
            print(f"Overall resonance: {result['glint']['resonance']:.2f}")
        
        # Print each suggestion with context
        if 'suggestions' in result and result['suggestions']:
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"\n{'='*30} Suggestion {i} {'='*30}")
                print_suggestion(suggestion, code_lines)
                print('=' * 70)
        else:
            print("\nNo suggestions generated. Raw issues:")
            if 'raw_issues' in result:
                for issue in result['raw_issues']:
                    print(f"- {issue}")
            else:
                print("No raw issues found in result")
    
    # Test with a specific file if provided
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                file_code = f.read()
            
            print(f"\n{'='*50}")
            print(f"ANALYZING FILE: {filepath}")
            print(f"{'='*50}")
            
            result = lint_code(file_code, toneform="intellectual", style="precise")
            
            print(f"\nFile analysis complete. Found {len(result['suggestions'])} suggestions.")
            print(f"Overall resonance: {result['glint']['resonance']:.2f}")
            
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"\nSuggestion {i}:")
                print_suggestion(suggestion)

if __name__ == "__main__":
    test_linter()
