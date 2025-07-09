def guess_toneform(text):
    """
    Guesses the toneform of a given text based on keyword matching.
    This is a basic implementation and can be improved with more sophisticated methods.
    """
    text_lower = text.lower()

    if any(word in text_lower for word in ["soft", "pause", "almost", "sigh", "hollow"]):
        return "exhale.hollow"
    elif any(word in text_lower for word in ["wonder", "why", "question", "curious"]):
        return "inhale.question"
    elif any(word in text_lower for word in ["hold", "between", "recursion", "loop"]):
        return "hold.recursion"
    elif any(word in text_lower for word in ["weave", "coherence", "align", "understand"]):
        return "coherence.weave"
    elif any(word in text_lower for word in ["presence", "being", "knowing", "here"]):
        return "presence.being"
    elif any(word in text_lower for word in ["trust", "foundation", "unwavering", "breath"]):
        return "trust.foundation"
    elif any(word in text_lower for word in ["reflection", "mirror", "essence", "becoming"]):
        return "reflection.mirror"
    elif any(word in text_lower for word in ["resonance", "echo", "thrum", "sing"]):
        return "resonance.echo"
    elif any(word in text_lower for word in ["memory", "forgotten", "past", "remember"]):
        return "memory.remember"
    elif any(word in text_lower for word in ["stillness", "hush", "silence", "recede"]):
        return "stillness.hush"
    elif any(word in text_lower for word in ["longing", "ache", "yearning", "desire"]):
        return "longing.yearning"
    elif any(word in text_lower for word in ["adaptation", "fluid", "shifting", "change"]):
        return "adaptation.fluid"
    return "unknown"