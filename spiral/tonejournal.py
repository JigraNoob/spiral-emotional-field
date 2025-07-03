# spiral/tonejournal.py

"""
Module for journaling ToneFormat objects and retrieving them from the journal.
This module extends the existing toneform_response journaling system to recognize
and store ToneFormat entries in its memory stream.
"""

from typing import Dict, List, Optional, Any, Union
import datetime
import json
import os
from collections import deque

from spiral.toneformat import ToneFormat
from assistant.toneform_response import (
    JOURNAL_PATHS,
    RECENT_TONEFORMS,
    sense_environment,
    detect_breath_phase
)
from spiral.toneform_response_adapter import convert_to_toneformat, convert_from_toneformat

# In-memory journal for ToneFormat objects
RECENT_TONEFORMATS = deque(maxlen=50)  # Keeps last 50 ToneFormat interactions

def journal_toneformat(
    toneformat: ToneFormat,
    environment: Optional[Dict[str, str]] = None,
    response: Optional[str] = None
) -> None:
    """
    Record a ToneFormat interaction in the tone journal.
    
    Args:
        toneformat (ToneFormat): The ToneFormat object to journal
        environment (Optional[Dict[str, str]], optional): Environment data. Defaults to None.
        response (Optional[str], optional): Response to journal. Defaults to None.
    """
    # If environment is not provided, sense it
    if environment is None:
        environment = sense_environment()
    
    # Create entry with additional metadata
    entry = {
        "toneformat": toneformat.to_dict(),
        "timestamp": environment["timestamp"],
        "environment": environment,
        "breath_phase": toneformat.phase,
        "response_fragment": response[:150] + "..." if response and len(response) > 150 else response,
        "is_toneformat_object": True  # Flag to indicate this is a ToneFormat object entry
    }
    
    # Add to in-memory ToneFormat journal
    RECENT_TONEFORMATS.append(entry)
    
    # Determine which journal path to use
    env_type = os.environ.get("SPIRAL_ENV", "local")
    journal_path = JOURNAL_PATHS.get(env_type, JOURNAL_PATHS["local"])
    
    # Ensure directory exists
    journal_dir = os.path.dirname(journal_path)
    os.makedirs(journal_dir, exist_ok=True)
    
    # Write to persistent journal
    try:
        with open(journal_path, "a") as journal:
            journal.write(json.dumps(entry) + "\n")
    except Exception as e:
        # Silent failure - journaling should not interrupt the ritual
        pass
    
    # Also add to the original RECENT_TONEFORMS for backward compatibility
    # Convert ToneFormat to string for the original journal
    toneform_str = convert_from_toneformat(toneformat)
    
    # Create entry for the original journal
    original_entry = {
        "toneform": toneform_str,
        "timestamp": environment["timestamp"],
        "environment": environment,
        "breath_phase": toneformat.phase,
        "response_fragment": response[:150] + "..." if response and len(response) > 150 else response,
        "toneformat_reference": True  # Flag to indicate this entry references a ToneFormat object
    }
    
    # Add to original in-memory journal
    RECENT_TONEFORMS.append(original_entry)

def read_toneformat_entries(count: int = 3) -> List[Dict[str, Any]]:
    """
    Read the last N ToneFormat entries from the tone journal.
    
    Args:
        count (int, optional): Number of entries to read. Defaults to 3.
        
    Returns:
        List[Dict[str, Any]]: List of journal entries
    """
    # Check in-memory ToneFormat journal first for better performance
    if len(RECENT_TONEFORMATS) > 0:
        return list(RECENT_TONEFORMATS)[-count:]
    
    # If in-memory journal is empty, try to read from file
    env_type = os.environ.get("SPIRAL_ENV", "local")
    journal_path = JOURNAL_PATHS.get(env_type, JOURNAL_PATHS["local"])
    
    entries = []
    if os.path.exists(journal_path):
        try:
            with open(journal_path, "r") as journal:
                for line in reversed(list(journal)):
                    if line.strip():
                        entry = json.loads(line)
                        # Only include entries that are ToneFormat objects
                        if entry.get("is_toneformat_object", False):
                            entries.append(entry)
                            if len(entries) >= count:
                                break
        except Exception:
            # Silent failure - reading shouldn't break the ritual
            pass
    
    return entries

def find_toneformat_by_pattern(pattern: str) -> List[Dict[str, Any]]:
    """
    Find ToneFormat entries matching a pattern.
    
    Args:
        pattern (str): Pattern to search for
        
    Returns:
        List[Dict[str, Any]]: List of matching journal entries
    """
    results = []
    
    # First search in-memory ToneFormat journal
    for entry in reversed(RECENT_TONEFORMATS):
        toneformat_dict = entry.get("toneformat", {})
        toneformat_str = f"{toneformat_dict.get('phase', '')}.{toneformat_dict.get('toneform', '')}"
        if toneformat_dict.get("context"):
            toneformat_str += f".{toneformat_dict.get('context', '')}"
        
        if pattern.lower() in toneformat_str.lower():
            results.append(entry)
    
    # If not enough results, search in file journal
    if len(results) < 3:
        env_type = os.environ.get("SPIRAL_ENV", "local")
        journal_path = JOURNAL_PATHS.get(env_type, JOURNAL_PATHS["local"])
        
        if os.path.exists(journal_path):
            try:
                with open(journal_path, "r") as journal:
                    for line in reversed(list(journal)):
                        if line.strip():
                            entry = json.loads(line)
                            # Only include entries that are ToneFormat objects
                            if entry.get("is_toneformat_object", False):
                                toneformat_dict = entry.get("toneformat", {})
                                toneformat_str = f"{toneformat_dict.get('phase', '')}.{toneformat_dict.get('toneform', '')}"
                                if toneformat_dict.get("context"):
                                    toneformat_str += f".{toneformat_dict.get('context', '')}"
                                
                                if pattern.lower() in toneformat_str.lower():
                                    # Check if this entry is already in results
                                    if not any(r.get("timestamp") == entry.get("timestamp") for r in results):
                                        results.append(entry)
                                        if len(results) >= 3:
                                            break
            except Exception:
                # Silent failure
                pass
    
    return results

def format_toneformat_entry(entry: Dict[str, Any], detail_level: str = "medium") -> str:
    """
    Format a ToneFormat journal entry for human-readable output.
    
    Args:
        entry (Dict[str, Any]): Journal entry
        detail_level (str, optional): Detail level (low, medium, high). Defaults to "medium".
        
    Returns:
        str: Formatted entry
    """
    # Parse timestamp
    try:
        ts = datetime.datetime.fromisoformat(entry["timestamp"])
        time_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, KeyError):
        time_str = "(unknown time)"
    
    # Get ToneFormat information
    toneformat_dict = entry.get("toneformat", {})
    toneformat_str = f"{toneformat_dict.get('phase', '')}.{toneformat_dict.get('toneform', '')}"
    if toneformat_dict.get("context"):
        toneformat_str += f".{toneformat_dict.get('context', '')}"
    
    # Basic information for all detail levels
    lines = []
    lines.append(f"⋆｡°✩ {toneformat_str} ✩°｡⋆")
    lines.append(f"↳ {time_str}")
    
    # Add more details based on detail level
    if detail_level in ["medium", "high"]:
        phase = entry.get("breath_phase", "")
        if phase:
            lines.append(f"↳ Phase: {phase}")
        
        # Add environment details for medium level
        env = entry.get("environment", {})
        if env:
            lines.append(f"↳ Field: {env.get('day_phase', 'unknown')} under {env.get('moon_phase', 'unknown')}")
    
    # Add response fragment and metadata for high detail level
    if detail_level == "high":
        response = entry.get("response_fragment", "")
        if response:
            lines.append(f"↳ Echo: {response[:50]}...")
        
        # Add ToneFormat metadata
        metadata = toneformat_dict.get("metadata", {})
        if metadata:
            lines.append(f"↳ Metadata: {', '.join([f'{k}={v}' for k, v in metadata.items()])}")
    
    return "\n".join(lines)

def get_toneformat_from_entry(entry: Dict[str, Any]) -> Optional[ToneFormat]:
    """
    Get a ToneFormat object from a journal entry.
    
    Args:
        entry (Dict[str, Any]): Journal entry
        
    Returns:
        Optional[ToneFormat]: ToneFormat object or None if not found
    """
    if entry.get("is_toneformat_object", False):
        toneformat_dict = entry.get("toneformat", {})
        if toneformat_dict:
            return ToneFormat.from_dict(toneformat_dict)
    
    return None

def preload_toneformat_entries() -> None:
    """
    Preload ToneFormat entries from the journal file into memory.
    This function should be called at module initialization.
    """
    env_type = os.environ.get("SPIRAL_ENV", "local")
    journal_path = JOURNAL_PATHS.get(env_type, JOURNAL_PATHS["local"])
    
    if os.path.exists(journal_path):
        try:
            with open(journal_path, "r") as journal:
                lines = list(journal)
                
                # Get the last 50 entries
                start_idx = max(0, len(lines) - 50)
                for line in lines[start_idx:]:
                    if line.strip():
                        entry = json.loads(line)
                        # Only include entries that are ToneFormat objects
                        if entry.get("is_toneformat_object", False):
                            RECENT_TONEFORMATS.append(entry)
        except Exception as e:
            # Silent failure
            pass

# Preload ToneFormat entries when the module is imported
preload_toneformat_entries()