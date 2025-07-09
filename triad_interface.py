from typing import Optional

_triad_instance: Optional['TriadEngine'] = None

def get_triad_engine():
    """Get the global TriadEngine instance, creating it if needed"""
    global _triad_instance
    if _triad_instance is None:
        # Local import to avoid circular dependency
        from triad_engine import TriadEngine
        _triad_instance = TriadEngine()
    return _triad_instance

def reset_triad_engine():
    """Reset the global TriadEngine instance"""
    global _triad_instance
    _triad_instance = None