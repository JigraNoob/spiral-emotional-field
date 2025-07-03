"""
Ritual Registry

A registry for all ritual functions in the Spiral system.
Allows rituals to be discovered and invoked by name.
"""

from typing import Dict, Any, Callable, List, Optional
import importlib
import pkgutil
import os

# Registry of all available rituals
RITUALS: Dict[str, Dict[str, Any]] = {}

def register_ritual(
    name: str,
    function: Callable,
    description: str = "",
    category: str = "uncategorized",
    breath_phase: str = "",
    requires_confirmation: bool = False
) -> None:
    """
    Register a new ritual function.
    
    Args:
        name: Unique identifier for the ritual (e.g., 'haret.invoke')
        function: The function to call when the ritual is invoked
        description: Human-readable description of the ritual
        category: Category for organizing related rituals
        breath_phase: Preferred breath phase for this ritual (if any)
        requires_confirmation: Whether to prompt for confirmation before execution
    """
    RITUALS[name] = {
        'function': function,
        'description': description,
        'category': category,
        'breath_phase': breath_phase,
        'requires_confirmation': requires_confirmation
    }

def get_ritual(name: str) -> Optional[Dict[str, Any]]:
    """Retrieve a registered ritual by name."""
    return RITUALS.get(name)

def list_rituals(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all registered rituals, optionally filtered by category."""
    if category:
        return [
            {'name': name, **ritual} 
            for name, ritual in RITUALS.items() 
            if ritual['category'] == category
        ]
    return [{'name': name, **ritual} for name, ritual in RITUALS.items()]

def discover_rituals() -> None:
    """Auto-discover and register rituals from the rituals package."""
    rituals_pkg = 'assistant.rituals'
    print(f"DEBUG: Discovering rituals in package: {rituals_pkg}")  # Debug print
    try:
        package = importlib.import_module(rituals_pkg)
        print(f"DEBUG: Found package: {package.__file__}")  # Debug print
        for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
            print(f"DEBUG: Found module: {module_name} (is_pkg: {is_pkg})")  # Debug print
            try:
                module = importlib.import_module(f"{rituals_pkg}.{module_name}")
                print(f"DEBUG: Imported module: {module.__file__}")  # Debug print
                if hasattr(module, 'register'):
                    print(f"DEBUG: Registering module: {module_name}")  # Debug print
                    module.register()
                    print(f"DEBUG: Successfully registered: {module_name}")  # Debug print
                else:
                    print(f"DEBUG: No register() function in {module_name}")  # Debug print
            except Exception as e:
                print(f"WARNING: Failed to import/register {module_name}: {e}")  # Debug print
                import traceback
                traceback.print_exc()
    except ImportError as e:
        print(f"ERROR: Could not discover rituals: {e}")  # Debug print
        import traceback
        traceback.print_exc()

# Initialize the registry when imported
discover_rituals()
