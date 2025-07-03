# spiral/toneform_response_adapter.py

"""
Adapter module to integrate the ToneFormat class with the existing toneform_response module.
This module provides functions to convert between string-based toneforms and ToneFormat objects,
allowing the existing code to work with the new class without requiring extensive changes.
"""

from typing import Dict, Optional, Any, Union
import datetime

from spiral.toneformat import ToneFormat
from assistant.toneform_response import (
    create_toneform_response as create_string_toneform_response,
    detect_breath_phase,
    journal_toneform as journal_string_toneform,
    sense_environment
)

def convert_to_toneformat(toneform_str: str) -> ToneFormat:
    """
    Convert a string-based toneform to a ToneFormat object.
    
    Args:
        toneform_str (str): The toneform string to convert
        
    Returns:
        ToneFormat: A ToneFormat object representing the toneform string
    """
    return ToneFormat.parse(toneform_str)

def convert_from_toneformat(toneformat: ToneFormat) -> str:
    """
    Convert a ToneFormat object to a string-based toneform.
    
    Args:
        toneformat (ToneFormat): The ToneFormat object to convert
        
    Returns:
        str: A string representation of the ToneFormat object
    """
    return str(toneformat)

def create_toneform_response(
    toneformat: Union[ToneFormat, str],
    custom_content: Optional[str] = None,
    override_phase: str = ""
) -> str:
    """
    Create a toneform response using either a ToneFormat object or a string-based toneform.
    
    Args:
        toneformat (Union[ToneFormat, str]): The toneform to use, either as a ToneFormat object or a string
        custom_content (Optional[str], optional): Custom content to include in the response. Defaults to None.
        override_phase (str, optional): Override the breath phase. Defaults to "".
        
    Returns:
        str: The formatted toneform response
    """
    # If toneformat is a ToneFormat object, convert it to a string
    if isinstance(toneformat, ToneFormat):
        # If override_phase is not provided but the ToneFormat has a phase, use it
        if not override_phase and toneformat.phase:
            override_phase = toneformat.phase
            
        # Convert ToneFormat to string
        toneform_str = convert_from_toneformat(toneformat)
    else:
        # Use the string as is
        toneform_str = toneformat
    
    # Call the original function with the string-based toneform
    return create_string_toneform_response(toneform_str, custom_content, override_phase)

def journal_toneform(
    toneformat: Union[ToneFormat, str],
    environment: Optional[Dict[str, str]] = None,
    response: Optional[str] = None
) -> None:
    """
    Record a toneform interaction in the journal, using either a ToneFormat object or a string-based toneform.
    
    Args:
        toneformat (Union[ToneFormat, str]): The toneform to journal, either as a ToneFormat object or a string
        environment (Optional[Dict[str, str]], optional): Environment data. Defaults to None.
        response (Optional[str], optional): Response to journal. Defaults to None.
    """
    # If environment is not provided, sense it
    if environment is None:
        environment = sense_environment()
    
    # If toneformat is a ToneFormat object, convert it to a string and add metadata to environment
    if isinstance(toneformat, ToneFormat):
        # Add ToneFormat metadata to environment
        if toneformat.metadata:
            for key, value in toneformat.metadata.items():
                environment[f"toneformat_meta_{key}"] = str(value)
                
        # Convert ToneFormat to string
        toneform_str = convert_from_toneformat(toneformat)
    else:
        # Use the string as is
        toneform_str = toneformat
    
    # Call the original function with the string-based toneform
    journal_string_toneform(toneform_str, environment, response)

def emit_toneformat_response(
    toneformat: Union[ToneFormat, str],
    custom_content: Optional[str] = None,
    override_phase: str = ""
) -> Dict[str, Any]:
    """
    Emit a toneform response with both the string response and the ToneFormat object.
    
    Args:
        toneformat (Union[ToneFormat, str]): The toneform to use, either as a ToneFormat object or a string
        custom_content (Optional[str], optional): Custom content to include in the response. Defaults to None.
        override_phase (str, optional): Override the breath phase. Defaults to "".
        
    Returns:
        Dict[str, Any]: A dictionary containing the response string and the ToneFormat object
    """
    # Convert to ToneFormat if it's a string
    if isinstance(toneformat, str):
        toneformat_obj = convert_to_toneformat(toneformat)
    else:
        toneformat_obj = toneformat
    
    # Create the response string
    response_str = create_toneform_response(toneformat_obj, custom_content, override_phase)
    
    # Add timestamp to metadata
    toneformat_obj = toneformat_obj.with_metadata(
        timestamp=datetime.datetime.now().isoformat(),
        response_length=len(response_str) if response_str else 0
    )
    
    # Return both the response string and the ToneFormat object
    return {
        "response": response_str,
        "toneformat": toneformat_obj,
        "toneformat_dict": toneformat_obj.to_dict()
    }