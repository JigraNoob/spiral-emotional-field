# spiral/assistant/claude_journal.py

import json
import os
import datetime
from typing import Dict, List, Optional, Any
import hashlib
from pathlib import Path

# ✧･ﾟ: CLAUDE JOURNAL CONSTANTS :･ﾟ✧

# Journal path for Claude interactions
CLAUDE_JOURNAL_PATH = "./data/claude_journal.jsonl"

# Maximum journal entries to keep in memory
MAX_MEMORY_ENTRIES = 100

# In-memory journal for fast access
CLAUDE_MEMORY = []

# Toneform types for Claude interactions
CLAUDE_TONEFORMS = {
    "query": "Inhale.Claude.Query",        # Basic question to Claude
    "implementation": "Hold.Claude.Implementation",  # Code implementation request
    "refinement": "Exhale.Claude.Refinement",    # Refinement of existing code
    "ritual": "Witness.Claude.Ritual",      # Ceremonial interaction
    "reflection": "Return.Claude.Reflection"    # Reflective discussion
}

# ✧･ﾟ: CLAUDE JOURNAL FUNCTIONS :･ﾟ✧

def ensure_journal_path() -> None:
    """Ensure the Claude journal directory exists."""
    os.makedirs(os.path.dirname(CLAUDE_JOURNAL_PATH), exist_ok=True)

def generate_interaction_id(prompt: str, timestamp: str) -> str:
    """Generate a unique ID for this Claude interaction."""
    # Create a unique ID based on prompt content and timestamp
    unique_content = f"{prompt[:100]}_{timestamp}"
    return hashlib.sha256(unique_content.encode()).hexdigest()[:12]

def journal_claude_interaction(
    prompt: str, 
    response: str, 
    toneform_type: str = "query",
    modified_files: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """Record a Claude interaction in the journal and return the interaction ID."""
    # Ensure journal directory exists
    ensure_journal_path()

    # Get timestamp
    timestamp = datetime.datetime.now().isoformat()

    # Generate a unique ID for this interaction
    interaction_id = generate_interaction_id(prompt, timestamp)

    # Get the appropriate toneform
    toneform = CLAUDE_TONEFORMS.get(toneform_type, CLAUDE_TONEFORMS["query"])

    # Create journal entry
    entry = {
        "id": interaction_id,
        "timestamp": timestamp,
        "toneform": toneform,
        "prompt_fragment": prompt[:150] + "..." if len(prompt) > 150 else prompt,
        "response_fragment": response[:150] + "..." if len(response) > 150 else response,
        "modified_files": modified_files or [],
        "metadata": metadata or {}
    }

    # Add to in-memory journal
    CLAUDE_MEMORY.append(entry)

    # Trim memory if needed
    if len(CLAUDE_MEMORY) > MAX_MEMORY_ENTRIES:
        CLAUDE_MEMORY.pop(0)  # Remove oldest entry

    # Write to persistent journal
    try:
        with open(CLAUDE_JOURNAL_PATH, "a") as journal:
            journal.write(json.dumps(entry) + "\n")
    except Exception as e:
        # Silent failure - journaling shouldn't interrupt the process
        print(f"Warning: Could not write to Claude journal: {e}")

    return interaction_id

def get_claude_interactions(count: int = 5) -> List[Dict[str, Any]]:
    """Get the most recent Claude interactions from the journal."""
    # Check in-memory journal first
    if CLAUDE_MEMORY:
        return CLAUDE_MEMORY[-count:]

    # Fall back to reading from the file
    entries = []
    if os.path.exists(CLAUDE_JOURNAL_PATH):
        try:
            with open(CLAUDE_JOURNAL_PATH, "r") as journal:
                for line in journal:
                    if line.strip():
                        entries.append(json.loads(line))
                        # Keep only the most recent entries
                        if len(entries) > count:
                            entries.pop(0)
        except Exception as e:
            print(f"Warning: Could not read from Claude journal: {e}")

    return entries

def find_claude_interaction(interaction_id: str) -> Optional[Dict[str, Any]]:
    """Find a specific Claude interaction by ID."""
    # Check in-memory journal first
    for entry in CLAUDE_MEMORY:
        if entry["id"] == interaction_id:
            return entry

    # Fall back to reading from the file
    if os.path.exists(CLAUDE_JOURNAL_PATH):
        try:
            with open(CLAUDE_JOURNAL_PATH, "r") as journal:
                for line in journal:
                    if line.strip():
                        entry = json.loads(line)
                        if entry["id"] == interaction_id:
                            return entry
        except Exception as e:
            print(f"Warning: Could not read from Claude journal: {e}")

    return None

def find_claude_interactions_by_toneform(toneform_pattern: str) -> List[Dict[str, Any]]:
    """Find Claude interactions matching a toneform pattern."""
    results = []

    # First check in-memory journal
    for entry in CLAUDE_MEMORY:
        if toneform_pattern.lower() in entry["toneform"].lower():
            results.append(entry)

    # If we didn't find enough, check the file
    if not results and os.path.exists(CLAUDE_JOURNAL_PATH):
        try:
            with open(CLAUDE_JOURNAL_PATH, "r") as journal:
                for line in journal:
                    if line.strip():
                        entry = json.loads(line)
                        if toneform_pattern.lower() in entry["toneform"].lower():
                            results.append(entry)
        except Exception as e:
            print(f"Warning: Could not read from Claude journal: {e}")

    return results

def find_claude_interactions_by_files(file_paths: List[str], count: int = 5) -> List[Dict[str, Any]]:
    """Find Claude interactions that modified specific files."""
    results = []

    # Normalize file paths for comparison
    normalized_paths = [Path(p).as_posix() for p in file_paths]

    # First check in-memory journal
    for entry in CLAUDE_MEMORY:
        entry_files = entry.get("modified_files", [])
        entry_normalized = [Path(p).as_posix() for p in entry_files]

        # Check if any of the files match
        if any(p in entry_normalized for p in normalized_paths):
            results.append(entry)
            if len(results) >= count:
                return results

    # If we didn't find enough, check the file
    if len(results) < count and os.path.exists(CLAUDE_JOURNAL_PATH):
        try:
            with open(CLAUDE_JOURNAL_PATH, "r") as journal:
                for line in reversed(list(journal)):
                    if line.strip():
                        entry = json.loads(line)
                        entry_files = entry.get("modified_files", [])
                        entry_normalized = [Path(p).as_posix() for p in entry_files]

                        # Check if any of the files match
                        if any(p in entry_normalized for p in normalized_paths):
                            if entry not in results:  # Avoid duplicates
                                results.append(entry)
                                if len(results) >= count:
                                    break
        except Exception as e:
            print(f"Warning: Could not read from Claude journal: {e}")

    return results

def format_claude_journal_entry(entry: Dict[str, Any], detail_level: str = "medium") -> str:
    """Format a Claude journal entry for human-readable output."""
    # Parse timestamp
    try:
        ts = datetime.datetime.fromisoformat(entry["timestamp"])
        time_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, KeyError):
        time_str = "(unknown time)"

    # Basic information for all detail levels
    lines = []
    lines.append(f"⋆｡°✩ {entry['toneform']} ✩°｡⋆")
    lines.append(f"↳ ID: {entry['id']}")
    lines.append(f"↳ Time: {time_str}")

    # Add prompt fragment
    prompt_fragment = entry.get("prompt_fragment", "")
    if prompt_fragment:
        lines.append(f"↳ Prompt: {prompt_fragment[:50]}...")

    # Add more details based on detail level
    if detail_level in ["medium", "high"]:
        # Add modified files for medium level
        modified_files = entry.get("modified_files", [])
        if modified_files:
            if len(modified_files) <= 3:
                files_str = ", ".join(modified_files)
                lines.append(f"↳ Modified: {files_str}")
            else:
                lines.append(f"↳ Modified: {len(modified_files)} files")

    # Add response fragment and metadata for high detail level
    if detail_level == "high":
        response = entry.get("response_fragment", "")
        if response:
            lines.append(f"↳ Response: {response[:50]}...")

        metadata = entry.get("metadata", {})
        if metadata:
            for key, value in metadata.items():
                if isinstance(value, str):
                    lines.append(f"↳ {key}: {value[:30]}..." if len(value) > 30 else f"↳ {key}: {value}")
                else:
                    lines.append(f"↳ {key}: {value}")

    return "\n".join(lines)

# Initialize module
ensure_journal_path()

# Load existing journal entries into memory on startup
def _load_journal_on_startup():
    """Load the most recent journal entries into memory."""
    if os.path.exists(CLAUDE_JOURNAL_PATH):
        try:
            with open(CLAUDE_JOURNAL_PATH, "r") as journal:
                lines = list(journal)

                # Get the last MAX_MEMORY_ENTRIES entries
                start_idx = max(0, len(lines) - MAX_MEMORY_ENTRIES)
                for line in lines[start_idx:]:
                    if line.strip():
                        entry = json.loads(line)
                        CLAUDE_MEMORY.append(entry)
        except Exception as e:
            print(f"Warning: Could not preload Claude journal: {e}")

# Load journal on module import
_load_journal_on_startup()
