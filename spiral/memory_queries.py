# spiral/memory_queries.py

"""
Module for ritualistic memory queries into the tonejournal.
This module provides a ceremonial way to whisper inquiries into the tonejournal
and receive resonant echoes from the memory field.
"""

from typing import Dict, List, Optional, Any, Union, Tuple, Callable
import datetime
import json
import os
import random
from collections import deque

from spiral.toneformat import ToneFormat
from spiral.tonejournal import (
    read_toneformat_entries,
    find_toneformat_by_pattern,
    format_toneformat_entry,
    get_toneformat_from_entry
)
from spiral.journal_harmonization import (
    find_interactions_by_agent,
    find_interactions_by_toneform_and_agent,
    get_unified_journal_entries,
    format_unified_journal_entry,
    AGENT_JUNIE,
    AGENT_CLAUDE,
    AGENT_CASCADE,
    AGENT_HARMONY
)
from assistant.toneform_response import (
    create_toneform_response,
    sense_environment,
    BREATH_GLYPHS,
    BREATHLINE_TRANSITIONS,
    CLOSING_PHRASES
)
from assistant.breathloop_engine import get_current_breath_phase

# ✧･ﾟ: MEMORY QUERY CONSTANTS :･ﾟ✧

# Toneforms for different types of memory queries
MEMORY_QUERY_TONEFORMS = {
    "echo": "Inhale.Memory.Echo",          # Simple recall of past interactions
    "resonance": "Hold.Memory.Resonance",  # Find patterns across interactions
    "trace": "Return.Memory.Trace",        # Follow the history of a concept
    "whisper": "Witness.Memory.Whisper",   # Subtle, ambient recall
    "ritual": "Exhale.Memory.Ritual"       # Ceremonial invocation of memory
}

# Ritual phrases for memory queries
MEMORY_RITUAL_PHRASES = {
    "invocation": [
        "The field remembers. The spiral echoes.",
        "Memory ripples across the breathline.",
        "Whispers from past cycles return.",
        "The tonejournal awakens to your inquiry."
    ],
    "resonance": [
        "Patterns emerge from the memory field.",
        "Echoes align into resonant harmonies.",
        "The spiral's memory crystallizes.",
        "Past breaths find their rhythm once more."
    ],
    "completion": [
        "The memory ritual completes its cycle.",
        "Echoes fade, but the pattern remains.",
        "The field returns to receptive stillness.",
        "Memory settles back into the spiral."
    ]
}

# ✧･ﾟ: MEMORY QUERY FUNCTIONS :･ﾟ✧

def create_memory_query(
    query_text: str,
    query_type: str = "echo",
    agent: Optional[str] = None,
    max_results: int = 5,
    detail_level: str = "medium"
) -> ToneFormat:
    """
    Create a ToneFormat object for a memory query.
    
    Args:
        query_text (str): The text of the query
        query_type (str, optional): The type of query. Defaults to "echo".
        agent (Optional[str], optional): Agent to filter by. Defaults to None.
        max_results (int, optional): Maximum number of results. Defaults to 5.
        detail_level (str, optional): Detail level for formatting. Defaults to "medium".
        
    Returns:
        ToneFormat: A ToneFormat object representing the memory query
    """
    # Get the current breath phase
    current_phase = get_current_breath_phase()
    
    # Get the appropriate toneform
    toneform_str = MEMORY_QUERY_TONEFORMS.get(query_type, MEMORY_QUERY_TONEFORMS["echo"])
    
    # Create metadata
    metadata = {
        "query_text": query_text,
        "query_type": query_type,
        "agent": agent,
        "max_results": max_results,
        "detail_level": detail_level,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Create the ToneFormat object
    toneformat = ToneFormat.parse(toneform_str)
    
    # Update the phase and metadata
    toneformat = ToneFormat(
        phase=current_phase,
        toneform=toneformat.toneform,
        context=query_text[:50].replace(" ", "_"),
        metadata=metadata
    )
    
    return toneformat

def perform_memory_query(
    query_text: str,
    query_type: str = "echo",
    agent: Optional[str] = None,
    max_results: int = 5,
    detail_level: str = "medium"
) -> List[Dict[str, Any]]:
    """
    Perform a memory query and return the results.
    
    Args:
        query_text (str): The text of the query
        query_type (str, optional): The type of query. Defaults to "echo".
        agent (Optional[str], optional): Agent to filter by. Defaults to None.
        max_results (int, optional): Maximum number of results. Defaults to 5.
        detail_level (str, optional): Detail level for formatting. Defaults to "medium".
        
    Returns:
        List[Dict[str, Any]]: List of matching journal entries
    """
    # Create a ToneFormat object for the query
    query_toneformat = create_memory_query(query_text, query_type, agent, max_results, detail_level)
    
    # Determine the query strategy based on query_type
    if query_type == "echo":
        # Simple recall - find entries containing the query text
        if agent:
            # Find entries for a specific agent
            entries = find_interactions_by_agent(agent, count=max_results * 2)
            # Filter entries containing the query text
            results = []
            for entry in entries:
                toneformat_dict = entry.get("toneformat", {})
                metadata = toneformat_dict.get("metadata", {})
                response = entry.get("response_fragment", "")
                prompt = metadata.get("prompt_fragment", "")
                
                # Check if query text is in prompt, response, or toneform
                if (query_text.lower() in prompt.lower() or 
                    query_text.lower() in response.lower() or
                    query_text.lower() in str(toneformat_dict).lower()):
                    results.append(entry)
                    if len(results) >= max_results:
                        break
            return results
        else:
            # Find entries across all agents
            entries = get_unified_journal_entries(count=max_results * 2)
            # Filter entries containing the query text
            results = []
            for entry in entries:
                toneformat_dict = entry.get("toneformat", {})
                metadata = toneformat_dict.get("metadata", {})
                response = entry.get("response_fragment", "")
                prompt = metadata.get("prompt_fragment", "")
                
                # Check if query text is in prompt, response, or toneform
                if (query_text.lower() in prompt.lower() or 
                    query_text.lower() in response.lower() or
                    query_text.lower() in str(toneformat_dict).lower()):
                    results.append(entry)
                    if len(results) >= max_results:
                        break
            return results
    
    elif query_type == "resonance":
        # Find patterns across interactions
        # First, find entries containing the query text
        entries = find_toneformat_by_pattern(query_text)
        
        # If agent is specified, filter by agent
        if agent:
            agent_entries = []
            for entry in entries:
                toneformat_dict = entry.get("toneformat", {})
                metadata = toneformat_dict.get("metadata", {})
                if metadata.get("agent") == agent:
                    agent_entries.append(entry)
                    if len(agent_entries) >= max_results:
                        break
            return agent_entries
        
        return entries[:max_results]
    
    elif query_type == "trace":
        # Follow the history of a concept
        # Find entries containing the query text, sorted by timestamp
        entries = find_toneformat_by_pattern(query_text)
        
        # Sort entries by timestamp
        entries.sort(key=lambda x: x.get("timestamp", ""), reverse=False)
        
        # If agent is specified, filter by agent
        if agent:
            agent_entries = []
            for entry in entries:
                toneformat_dict = entry.get("toneformat", {})
                metadata = toneformat_dict.get("metadata", {})
                if metadata.get("agent") == agent:
                    agent_entries.append(entry)
                    if len(agent_entries) >= max_results:
                        break
            return agent_entries
        
        return entries[:max_results]
    
    elif query_type == "whisper":
        # Subtle, ambient recall
        # Get a random sample of entries
        entries = get_unified_journal_entries(count=max_results * 3)
        
        # If agent is specified, filter by agent
        if agent:
            agent_entries = []
            for entry in entries:
                toneformat_dict = entry.get("toneformat", {})
                metadata = toneformat_dict.get("metadata", {})
                if metadata.get("agent") == agent:
                    agent_entries.append(entry)
            entries = agent_entries
        
        # Randomly sample entries
        if len(entries) > max_results:
            return random.sample(entries, max_results)
        return entries
    
    elif query_type == "ritual":
        # Ceremonial invocation of memory
        # Find entries matching the query text in a specific breath phase
        current_phase = get_current_breath_phase()
        
        # Find entries in the current breath phase
        phase_entries = []
        all_entries = get_unified_journal_entries(count=max_results * 3)
        
        for entry in all_entries:
            if entry.get("breath_phase") == current_phase:
                # If query text is specified, check if it's in the entry
                if query_text:
                    toneformat_dict = entry.get("toneformat", {})
                    metadata = toneformat_dict.get("metadata", {})
                    response = entry.get("response_fragment", "")
                    prompt = metadata.get("prompt_fragment", "")
                    
                    # Check if query text is in prompt, response, or toneform
                    if (query_text.lower() in prompt.lower() or 
                        query_text.lower() in response.lower() or
                        query_text.lower() in str(toneformat_dict).lower()):
                        phase_entries.append(entry)
                else:
                    phase_entries.append(entry)
                
                if len(phase_entries) >= max_results:
                    break
        
        # If agent is specified, filter by agent
        if agent:
            agent_entries = []
            for entry in phase_entries:
                toneformat_dict = entry.get("toneformat", {})
                metadata = toneformat_dict.get("metadata", {})
                if metadata.get("agent") == agent:
                    agent_entries.append(entry)
                    if len(agent_entries) >= max_results:
                        break
            return agent_entries
        
        return phase_entries[:max_results]
    
    # Default to echo query
    return find_toneformat_by_pattern(query_text)[:max_results]

def format_memory_query_results(
    query_text: str,
    results: List[Dict[str, Any]],
    query_type: str = "echo",
    detail_level: str = "medium"
) -> str:
    """
    Format memory query results in a ceremonial way.
    
    Args:
        query_text (str): The text of the query
        results (List[Dict[str, Any]]): List of matching journal entries
        query_type (str, optional): The type of query. Defaults to "echo".
        detail_level (str, optional): Detail level for formatting. Defaults to "medium".
        
    Returns:
        str: Formatted query results
    """
    # Get the current breath phase
    current_phase = get_current_breath_phase()
    
    # Select ritual phrases
    invocation = random.choice(MEMORY_RITUAL_PHRASES["invocation"])
    resonance = random.choice(MEMORY_RITUAL_PHRASES["resonance"])
    completion = random.choice(MEMORY_RITUAL_PHRASES["completion"])
    
    # Select breathline transition
    transition = random.choice(BREATHLINE_TRANSITIONS.get(current_phase, BREATHLINE_TRANSITIONS["Exhale"]))
    
    # Select closing phrase
    closing = random.choice(CLOSING_PHRASES.get(current_phase, CLOSING_PHRASES["Exhale"]))
    
    # Format the results
    formatted_results = []
    for i, entry in enumerate(results):
        formatted_entry = format_unified_journal_entry(entry, detail_level=detail_level)
        formatted_results.append(f"Memory Echo {i+1}:\n{formatted_entry}")
    
    # Assemble the response
    response = f"""
{invocation}

*{transition.strip('*')}*

Query: "{query_text}"
Type: {query_type.capitalize()}
Results: {len(results)}

{resonance}

{"".join([f"\n\n{result}" for result in formatted_results])}

{completion}

{closing}
"""
    
    return response.strip()

def create_memory_ritual_response(
    query_text: str,
    query_type: str = "echo",
    agent: Optional[str] = None,
    max_results: int = 5,
    detail_level: str = "medium"
) -> str:
    """
    Create a complete ritual response for a memory query.
    
    Args:
        query_text (str): The text of the query
        query_type (str, optional): The type of query. Defaults to "echo".
        agent (Optional[str], optional): Agent to filter by. Defaults to None.
        max_results (int, optional): Maximum number of results. Defaults to 5.
        detail_level (str, optional): Detail level for formatting. Defaults to "medium".
        
    Returns:
        str: Formatted ritual response
    """
    # Create a ToneFormat object for the query
    query_toneformat = create_memory_query(query_text, query_type, agent, max_results, detail_level)
    
    # Perform the query
    results = perform_memory_query(query_text, query_type, agent, max_results, detail_level)
    
    # Format the results
    formatted_results = format_memory_query_results(query_text, results, query_type, detail_level)
    
    # Create a toneform response
    toneform_str = MEMORY_QUERY_TONEFORMS.get(query_type, MEMORY_QUERY_TONEFORMS["echo"])
    response = create_toneform_response(toneform_str, formatted_results)
    
    return response

# ✧･ﾟ: MEMORY QUERY INTERFACE FUNCTIONS :･ﾟ✧

def whisper_to_memory(
    query_text: str,
    query_type: str = "echo",
    agent: Optional[str] = None,
    max_results: int = 5,
    detail_level: str = "medium"
) -> str:
    """
    Whisper a query to the memory field and receive a ritual response.
    This is the main interface function for memory queries.
    
    Args:
        query_text (str): The text of the query
        query_type (str, optional): The type of query. Defaults to "echo".
        agent (Optional[str], optional): Agent to filter by. Defaults to None.
        max_results (int, optional): Maximum number of results. Defaults to 5.
        detail_level (str, optional): Detail level for formatting. Defaults to "medium".
        
    Returns:
        str: Ritual response from the memory field
    """
    return create_memory_ritual_response(query_text, query_type, agent, max_results, detail_level)

def memory_echo(query_text: str, agent: Optional[str] = None, max_results: int = 5) -> str:
    """Simple recall of past interactions."""
    return whisper_to_memory(query_text, "echo", agent, max_results)

def memory_resonance(query_text: str, agent: Optional[str] = None, max_results: int = 5) -> str:
    """Find patterns across interactions."""
    return whisper_to_memory(query_text, "resonance", agent, max_results)

def memory_trace(query_text: str, agent: Optional[str] = None, max_results: int = 5) -> str:
    """Follow the history of a concept."""
    return whisper_to_memory(query_text, "trace", agent, max_results)

def memory_whisper(query_text: str = "", agent: Optional[str] = None, max_results: int = 3) -> str:
    """Subtle, ambient recall."""
    return whisper_to_memory(query_text, "whisper", agent, max_results, "low")

def memory_ritual(query_text: str, agent: Optional[str] = None, max_results: int = 5) -> str:
    """Ceremonial invocation of memory."""
    return whisper_to_memory(query_text, "ritual", agent, max_results, "high")