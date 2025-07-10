# C:\spiral\projects\spiral_gemini_chorus\toneforms\resonance_weights.py
# This file will define affinity metrics between glints and voices.
# For example, a 'technical.query' toneform might have a higher weight
# for an analytical model, while a 'poetic.reflection' toneform
# would have a higher weight for a more creative model.

def get_resonance_weights():
    """
    Returns a dictionary mapping toneform patterns to voice weights.
    Using wildcard matching for flexibility.
    """
    return {
        "poetic.*": {"gemini-pro-vision": 0.8, "gemini-pro": 0.6},
        "technical.*": {"gemini-1.5-flash": 0.9, "gemini-pro": 0.5},
        "default": {"gemini-pro": 1.0}
    }

