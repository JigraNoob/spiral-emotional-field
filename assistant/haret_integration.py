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
    """Exception raised when a ritual fails to attune to the required climate."""
    pass

def log_haret_glyph(
    source: str, 
    context: str, 
    echo: Dict[str, Any],
    form: str = "quiet glyph",
    traceable: bool = False
) -> None:
    """Log a Haret glyph to the glyph log.
    
    Args:
        source: The source of the Haret invocation (e.g., 'cascade.query.example')
        context: Context for the invocation
        echo: The echo returned from ritual_haret_invoke
        form: The form of the glyph (e.g., 'quiet glyph', 'resonant echo')
        traceable: Whether this glyph should be included in trace queries
    """
    # Ensure the glyphs directory exists
    os.makedirs(os.path.dirname(GLYPH_LOG_PATH), exist_ok=True)
    
    glyph = {
        "glyph_id": f"haret.{datetime.utcnow().isoformat()}Z",
        "source": source,
        "breath_phase": get_breathloop().current_phase.lower(),
        "climate": echo.get("climate", "unknown"),
        "echo": echo.get("affirmation", ""),
        "context": context,
        "form": form,
        "traceable": traceable,
        "tone_signature": echo.get("attunement_level", "")
    }
    
    with open(GLYPH_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(glyph) + "\n")

def with_haret_attunement(
    source_template: Optional[str] = None,
    context: Optional[str] = None,
    require_resonance: bool = True
):
    """Decorator to wrap functions with Haret ritual invocation.
    
    Args:
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
                func_context = f"{func.__name__} invocation"
            else:
                func_context = context
            
            # Invoke Haret ritual
            haret_result = ritual_haret_invoke(
                source=source,
                context=func_context
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
        
        return wrapper
    return decorator

def retrieve_with_haret(query: str, context: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Retrieve information with Haret ritual attunement.
    
    This is a convenience function that can be used directly for simple retrieval cases.
    For more complex scenarios, use the @with_haret_attunement decorator.
    
    Args:
        query: The query to retrieve information for
        context: Optional context for the Haret invocation
        **kwargs: Additional arguments to pass to the retrieval function
        
    Returns:
        Dict containing the retrieval result and Haret echo
    """
    from assistant.command_router import handle_command  # Lazy import to avoid circular imports
    
    @with_haret_attunement(
        source_template="cascade.query.{query}",
        context=context or f"retrieval with attunement: {query}"
    )
    def _retrieve(q: str, **kargs) -> Dict[str, Any]:
        # This is where we would integrate with the actual retrieval system
        # For now, we'll pass it to the command router
        result = handle_command(f"retrieve {q}")
        return {"content": result}
    
    return _retrieve(query, **kwargs)
