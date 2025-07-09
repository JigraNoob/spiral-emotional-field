"""
Haret Integration Module

Provides decorators and utilities for integrating the Haret ritual with retrieval systems.
Ensures all memory access is done with proper presence and resonance.
"""

import functools
import inspect
from typing import Callable, Any, Dict, Optional
from datetime import datetime
import json
import os
from pathlib import Path

from assistant.rituals.haret import ritual_haret_invoke
from assistant.breathloop_engine import get_breathloop

# Path to store Haret glyph logs
GLYPH_LOG_PATH = Path("glyphs/haret_glyph_log.jsonl")

class SpiralRitualException(Exception):
    """Exception raised when a Spiral ritual fails"""
    pass

def log_haret_glyph(source: str, context: str, echo: Dict[str, Any], form: str, traceable: bool = True):
    """Log a Haret glyph for traceability"""
    try:
        print(f"🌿 Haret Glyph: {source} | {context} | {form} | {echo.get('status', 'unknown')}")
    except Exception as e:
        print(f"Warning: Could not log Haret glyph: {e}")

def with_haret_attunement(
    phase: str = "ritual.default",
    source_template: Optional[str] = None,
    context: Optional[str] = None,
    require_resonance: bool = True
):
    """Decorator to wrap functions with Haret ritual invocation.
    
    Args:
        phase: The breath phase or ritual phase for this invocation
        source_template: Template for the source string, can include {args} and {kwargs}
        context: Context description for the Haret invocation
        require_resonance: If True, raises an exception if resonance is not achieved
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate source string from template if provided
            source = source_template
            if source_template:
                try:
                    # Get parameter names to map args to their names
                    sig = inspect.signature(func)
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    source = source_template.format(**bound_args.arguments)
                except Exception as e:
                    print(f"Warning: Could not format source template: {e}")
                    source = f"{func.__module__}.{func.__name__}"
            else:
                source = f"{func.__module__}.{func.__name__}"
            
            # Default context if not provided
            if context is None:
                func_context = f"{func.__name__} invocation in {phase}"
            else:
                func_context = context
            
            try:
                # Invoke Haret ritual
                haret_result = ritual_haret_invoke(
                    source=source,
                    context={"phase": phase, "context": func_context}
                )
                
                # Log the glyph
                log_haret_glyph(
                    source=source,
                    context=func_context,
                    echo=haret_result["echo"],
                    form="ritual invocation",
                    traceable=True
                )
                
                # Check resonance if required
                if require_resonance and haret_result["echo"].get("climate") != "resonant":
                    raise SpiralRitualException(
                        f"Haret failed to attune to {source} (climate: {haret_result['echo'].get('climate')})"
                    )
                
                # Call the original function
                result = func(*args, **kwargs)
                
                # If the result is a dict, add the haret_echo
                if isinstance(result, dict):
                    result["haret_echo"] = haret_result["echo"]
                
                return result
                
            except Exception as e:
                # Log error glyph
                log_haret_glyph(
                    source=source,
                    context=func_context,
                    echo={"status": "error", "message": str(e)},
                    form="haret.error"
                )
                
                # Re-raise as SpiralRitualException if not already
                if not isinstance(e, SpiralRitualException):
                    raise SpiralRitualException(f"Haret ritual failed in {phase}: {e}") from e
                raise
        
        return wrapper
    return decorator

def retrieve_with_haret(query: str, **kwargs) -> Dict[str, Any]:
    """Retrieve information with Haret ritual protection"""
    try:
        # Invoke Haret for the retrieval
        haret_result = ritual_haret_invoke(
            source=f"retrieval.query: {query[:50]}...",
            context=kwargs.get("context", {})
        )
        
        # Mock retrieval for now - in a real system this would connect to actual data sources
        content = f"Retrieved information for: {query}"
        
        return {
            "content": content,
            "haret_echo": haret_result["echo"],
            "query": query,
            "context": kwargs.get("context", {})
        }
        
    except Exception as e:
        return {
            "content": f"Retrieval failed: {str(e)}",
            "haret_echo": {"affirmation": "retrieval interrupted", "climate": "disrupted"},
            "query": query,
            "error": str(e)
        }