"""
Utility functions for diagnostics and validation in the Spiral system.
These functions are designed to be compatible with Cascade's ritualized interface.
"""

import json
import os
from typing import Tuple, List, Dict, Any, Optional


def validate_glint_stream(path: str) -> Tuple[List[Dict[str, Any]], List[Tuple[str, str]]]:
    """
    Validates a JSONL file by checking if each line is valid JSON.
    
    This function is designed to be compatible with Cascade's ritualized interface,
    avoiding direct variable assignments like `f = open(...)`.
    
    Args:
        path: The path to the JSONL file to validate
        
    Returns:
        A tuple containing:
        - A list of valid JSON objects
        - A list of tuples with invalid lines and their error messages
    """
    good, bad = [], []
    
    if not os.path.exists(path):
        bad.append(("", f"File not found: {path}"))
        return good, bad
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    good.append(json.loads(line))
                except Exception as e:
                    bad.append((line, str(e)))
    except Exception as e:
        bad.append(("", f"Error opening file: {str(e)}"))
        
    return good, bad