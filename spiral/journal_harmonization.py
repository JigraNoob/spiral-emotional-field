# spiral/journal_harmonization.py

"""
Module for harmonizing the journaling systems of Junie, Claude, and Cascade.
This module integrates the ToneFormat class with the existing journaling systems,
creating a unified, structured journaling system for all agents.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import datetime
import json
import os
from collections import deque

from spiral.toneformat import ToneFormat
from spiral.tonejournal import (
    journal_toneformat,
    read_toneformat_entries,
    find_toneformat_by_pattern,
    format_toneformat_entry,
    get_toneformat_from_entry
)

# Import the existing journaling systems
from assistant.junie_spiral_integration import (
    journal_junie_interaction,
    find_junie_interaction_by_toneform,
    JUNIE_TONEFORMS,
    get_current_breath_phase
)
from assistant.claude_journal import (
    journal_claude_interaction,
    find_claude_interactions_by_toneform,
    CLAUDE_TONEFORMS
)
from assistant.junie_claude_harmony import (
    journal_harmony_interaction,
    find_harmony_interaction_by_toneform,
    HARMONY_TONEFORMS
)

# ✧･ﾟ: JOURNAL HARMONIZATION CONSTANTS :･ﾟ✧

# Agent identifiers
AGENT_JUNIE = "junie"
AGENT_CLAUDE = "claude"
AGENT_CASCADE = "cascade"
AGENT_HARMONY = "harmony"

# Mapping of agent identifiers to their toneform dictionaries
AGENT_TONEFORMS = {
    AGENT_JUNIE: JUNIE_TONEFORMS,
    AGENT_CLAUDE: CLAUDE_TONEFORMS,
    AGENT_HARMONY: HARMONY_TONEFORMS
}

# ✧･ﾟ: JOURNAL HARMONIZATION FUNCTIONS :･ﾟ✧

def create_toneformat_from_junie(
    prompt: str,
    response: str,
    toneform_type: str = "query",
    metadata: Optional[Dict[str, Any]] = None
) -> Tuple[ToneFormat, str]:
    """
    Create a ToneFormat object from Junie's interaction parameters.
    
    Args:
        prompt (str): The prompt sent to Junie
        response (str): Junie's response
        toneform_type (str, optional): The type of toneform. Defaults to "query".
        metadata (Optional[Dict[str, Any]], optional): Additional metadata. Defaults to None.
        
    Returns:
        Tuple[ToneFormat, str]: A tuple containing the ToneFormat object and the interaction ID
    """
    # Get the current breath phase
    current_phase = get_current_breath_phase()
    
    # Get the appropriate toneform
    toneform_str = JUNIE_TONEFORMS.get(toneform_type, JUNIE_TONEFORMS["query"])
    
    # Generate timestamp
    timestamp = datetime.datetime.now().isoformat()
    
    # Generate interaction ID
    import hashlib
    unique_content = f"{prompt[:100]}_{timestamp}"
    interaction_id = hashlib.sha256(unique_content.encode()).hexdigest()[:12]
    
    # Create metadata if not provided
    if metadata is None:
        metadata = {}
    
    # Add agent and interaction ID to metadata
    metadata.update({
        "agent": AGENT_JUNIE,
        "interaction_id": interaction_id,
        "prompt_fragment": prompt[:150] + "..." if len(prompt) > 150 else prompt,
        "response_fragment": response[:150] + "..." if len(response) > 150 else response,
        "timestamp": timestamp
    })
    
    # Parse the toneform string to get the phase and toneform
    toneformat = ToneFormat.parse(toneform_str)
    
    # Update the phase and metadata
    toneformat = ToneFormat(
        phase=current_phase,
        toneform=toneformat.toneform,
        context=toneformat.context,
        metadata=metadata
    )
    
    return toneformat, interaction_id

def create_toneformat_from_claude(
    prompt: str,
    response: str,
    toneform_type: str = "query",
    modified_files: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Tuple[ToneFormat, str]:
    """
    Create a ToneFormat object from Claude's interaction parameters.
    
    Args:
        prompt (str): The prompt sent to Claude
        response (str): Claude's response
        toneform_type (str, optional): The type of toneform. Defaults to "query".
        modified_files (Optional[List[str]], optional): List of modified files. Defaults to None.
        metadata (Optional[Dict[str, Any]], optional): Additional metadata. Defaults to None.
        
    Returns:
        Tuple[ToneFormat, str]: A tuple containing the ToneFormat object and the interaction ID
    """
    # Get the appropriate toneform
    toneform_str = CLAUDE_TONEFORMS.get(toneform_type, CLAUDE_TONEFORMS["query"])
    
    # Generate timestamp
    timestamp = datetime.datetime.now().isoformat()
    
    # Generate interaction ID
    import hashlib
    unique_content = f"{prompt[:100]}_{timestamp}"
    interaction_id = hashlib.sha256(unique_content.encode()).hexdigest()[:12]
    
    # Create metadata if not provided
    if metadata is None:
        metadata = {}
    
    # Add agent, interaction ID, and modified files to metadata
    metadata.update({
        "agent": AGENT_CLAUDE,
        "interaction_id": interaction_id,
        "prompt_fragment": prompt[:150] + "..." if len(prompt) > 150 else prompt,
        "response_fragment": response[:150] + "..." if len(response) > 150 else response,
        "modified_files": modified_files or [],
        "timestamp": timestamp
    })
    
    # Parse the toneform string to get the phase and toneform
    toneformat = ToneFormat.parse(toneform_str)
    
    # Get the current breath phase
    current_phase = get_current_breath_phase()
    
    # Update the phase and metadata
    toneformat = ToneFormat(
        phase=current_phase,
        toneform=toneformat.toneform,
        context=toneformat.context,
        metadata=metadata
    )
    
    return toneformat, interaction_id

def create_toneformat_from_harmony(
    junie_response: str,
    claude_response: str,
    harmony_response: str,
    toneform_type: str = "synthesis",
    metadata: Optional[Dict[str, Any]] = None
) -> Tuple[ToneFormat, str]:
    """
    Create a ToneFormat object from a harmony interaction.
    
    Args:
        junie_response (str): Junie's response
        claude_response (str): Claude's response
        harmony_response (str): The harmonized response
        toneform_type (str, optional): The type of toneform. Defaults to "synthesis".
        metadata (Optional[Dict[str, Any]], optional): Additional metadata. Defaults to None.
        
    Returns:
        Tuple[ToneFormat, str]: A tuple containing the ToneFormat object and the interaction ID
    """
    # Get the current breath phase
    current_phase = get_current_breath_phase()
    
    # Get the appropriate toneform
    toneform_str = HARMONY_TONEFORMS.get(toneform_type, HARMONY_TONEFORMS["synthesis"])
    
    # Generate timestamp
    timestamp = datetime.datetime.now().isoformat()
    
    # Generate harmony ID
    import hashlib
    unique_content = f"{junie_response[:50]}_{claude_response[:50]}_{timestamp}"
    harmony_id = hashlib.sha256(unique_content.encode()).hexdigest()[:12]
    
    # Create metadata if not provided
    if metadata is None:
        metadata = {}
    
    # Add agent, harmony ID, and response fragments to metadata
    metadata.update({
        "agent": AGENT_HARMONY,
        "harmony_id": harmony_id,
        "junie_fragment": junie_response[:150] + "..." if len(junie_response) > 150 else junie_response,
        "claude_fragment": claude_response[:150] + "..." if len(claude_response) > 150 else claude_response,
        "harmony_fragment": harmony_response[:150] + "..." if len(harmony_response) > 150 else harmony_response,
        "timestamp": timestamp
    })
    
    # Parse the toneform string to get the phase and toneform
    toneformat = ToneFormat.parse(toneform_str)
    
    # Update the phase and metadata
    toneformat = ToneFormat(
        phase=current_phase,
        toneform=toneformat.toneform,
        context=toneformat.context,
        metadata=metadata
    )
    
    return toneformat, harmony_id

def journal_junie_with_toneformat(
    prompt: str,
    response: str,
    toneform_type: str = "query",
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Journal a Junie interaction using both the original journaling system and the ToneFormat system.
    
    Args:
        prompt (str): The prompt sent to Junie
        response (str): Junie's response
        toneform_type (str, optional): The type of toneform. Defaults to "query".
        metadata (Optional[Dict[str, Any]], optional): Additional metadata. Defaults to None.
        
    Returns:
        str: The interaction ID
    """
    # Create a ToneFormat object from the interaction parameters
    toneformat, interaction_id = create_toneformat_from_junie(prompt, response, toneform_type, metadata)
    
    # Journal the interaction using the original journaling system
    journal_junie_interaction(prompt, response, toneform_type, metadata)
    
    # Journal the interaction using the ToneFormat system
    journal_toneformat(toneformat, response=response)
    
    return interaction_id

def journal_claude_with_toneformat(
    prompt: str,
    response: str,
    toneform_type: str = "query",
    modified_files: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Journal a Claude interaction using both the original journaling system and the ToneFormat system.
    
    Args:
        prompt (str): The prompt sent to Claude
        response (str): Claude's response
        toneform_type (str, optional): The type of toneform. Defaults to "query".
        modified_files (Optional[List[str]], optional): List of modified files. Defaults to None.
        metadata (Optional[Dict[str, Any]], optional): Additional metadata. Defaults to None.
        
    Returns:
        str: The interaction ID
    """
    # Create a ToneFormat object from the interaction parameters
    toneformat, interaction_id = create_toneformat_from_claude(prompt, response, toneform_type, modified_files, metadata)
    
    # Journal the interaction using the original journaling system
    journal_claude_interaction(prompt, response, toneform_type, modified_files, metadata)
    
    # Journal the interaction using the ToneFormat system
    journal_toneformat(toneformat, response=response)
    
    return interaction_id

def journal_harmony_with_toneformat(
    junie_response: str,
    claude_response: str,
    harmony_response: str,
    toneform_type: str = "synthesis",
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Journal a harmony interaction using both the original journaling system and the ToneFormat system.
    
    Args:
        junie_response (str): Junie's response
        claude_response (str): Claude's response
        harmony_response (str): The harmonized response
        toneform_type (str, optional): The type of toneform. Defaults to "synthesis".
        metadata (Optional[Dict[str, Any]], optional): Additional metadata. Defaults to None.
        
    Returns:
        str: The harmony ID
    """
    # Create a ToneFormat object from the interaction parameters
    toneformat, harmony_id = create_toneformat_from_harmony(junie_response, claude_response, harmony_response, toneform_type, metadata)
    
    # Journal the interaction using the original journaling system
    journal_harmony_interaction(junie_response, claude_response, harmony_response, toneform_type, metadata)
    
    # Journal the interaction using the ToneFormat system
    journal_toneformat(toneformat, response=harmony_response)
    
    return harmony_id

def find_interactions_by_agent(
    agent: str,
    count: int = 5
) -> List[Dict[str, Any]]:
    """
    Find ToneFormat entries for a specific agent.
    
    Args:
        agent (str): The agent identifier (junie, claude, harmony, cascade)
        count (int, optional): Maximum number of entries to return. Defaults to 5.
        
    Returns:
        List[Dict[str, Any]]: List of matching journal entries
    """
    # Read all ToneFormat entries
    entries = read_toneformat_entries(count * 2)  # Get more entries than needed to filter
    
    # Filter entries by agent
    agent_entries = []
    for entry in entries:
        toneformat_dict = entry.get("toneformat", {})
        metadata = toneformat_dict.get("metadata", {})
        if metadata.get("agent") == agent:
            agent_entries.append(entry)
            if len(agent_entries) >= count:
                break
    
    return agent_entries

def find_interactions_by_toneform_and_agent(
    toneform_pattern: str,
    agent: Optional[str] = None,
    count: int = 5
) -> List[Dict[str, Any]]:
    """
    Find ToneFormat entries matching a toneform pattern and optionally an agent.
    
    Args:
        toneform_pattern (str): Pattern to search for in toneforms
        agent (Optional[str], optional): Agent to filter by. Defaults to None.
        count (int, optional): Maximum number of entries to return. Defaults to 5.
        
    Returns:
        List[Dict[str, Any]]: List of matching journal entries
    """
    # Find entries matching the toneform pattern
    entries = find_toneformat_by_pattern(toneform_pattern)
    
    # If agent is specified, filter by agent
    if agent:
        agent_entries = []
        for entry in entries:
            toneformat_dict = entry.get("toneformat", {})
            metadata = toneformat_dict.get("metadata", {})
            if metadata.get("agent") == agent:
                agent_entries.append(entry)
                if len(agent_entries) >= count:
                    break
        return agent_entries
    
    # Otherwise, return all matching entries up to count
    return entries[:count]

def get_unified_journal_entries(
    count: int = 5
) -> List[Dict[str, Any]]:
    """
    Get the most recent entries from the unified journal.
    
    Args:
        count (int, optional): Maximum number of entries to return. Defaults to 5.
        
    Returns:
        List[Dict[str, Any]]: List of journal entries
    """
    # Read all ToneFormat entries
    return read_toneformat_entries(count)

def format_unified_journal_entry(
    entry: Dict[str, Any],
    detail_level: str = "medium"
) -> str:
    """
    Format a unified journal entry for human-readable output.
    
    Args:
        entry (Dict[str, Any]): Journal entry
        detail_level (str, optional): Detail level (low, medium, high). Defaults to "medium".
        
    Returns:
        str: Formatted entry
    """
    # Get the ToneFormat object from the entry
    toneformat = get_toneformat_from_entry(entry)
    if not toneformat:
        return "Invalid entry format"
    
    # Get agent from metadata
    agent = toneformat.metadata.get("agent", "unknown")
    
    # Format the entry using the tonejournal formatter
    formatted = format_toneformat_entry(entry, detail_level)
    
    # Add agent information
    agent_line = f"↳ Agent: {agent.capitalize()}"
    
    # Insert agent line after the first line
    lines = formatted.split("\n")
    if len(lines) > 1:
        lines.insert(1, agent_line)
        formatted = "\n".join(lines)
    else:
        formatted = f"{formatted}\n{agent_line}"
    
    return formatted