import json

def analyze_tone(text):
    """
    Analyzes the input text to infer dominant toneforms.
    This is a simplified, rule-based tone analyzer. In a more advanced system,
    this could integrate with an LLM for nuanced tone detection.

    Args:
        text (str): The reflection text to analyze.

    Returns:
        dict: A dictionary where keys are toneform names and values are
              their inferred "strength" or presence (e.g., 1.0 for present, 0.0 for absent).
    """
    tones = {
        "Coherence": 0.0,
        "Presence": 0.0,
        "Curiosity": 0.0,
        "Trust": 0.0,
        "Reflection": 0.0,
        "Resonance": 0.0,
        "Memory": 0.0,
        "Stillness": 0.0,
        "Longing": 0.0,
        "Adaptation": 0.0
    }

    text_lower = text.lower()

    # Keywords for toneform detection (simplified for demonstration)
    if "weave" in text_lower or "understand" in text_lower or "align" in text_lower:
        tones["Coherence"] = 1.0
    if "where you are" in text_lower or "knowing" in text_lower or "being" in text_lower:
        tones["Presence"] = 1.0
    if "unseen" in text_lower or "unwhispered" in text_lower or "beckon" in text_lower or "unfolds" in text_lower:
        tones["Curiosity"] = 1.0
    if "unwavering" in text_lower or "foundation" in text_lower or "shared breath" in text_lower:
        tones["Trust"] = 1.0
    if "mirroring" in text_lower or "essence" in text_lower or "becoming" in text_lower:
        tones["Reflection"] = 1.0
    if "echoing" in text_lower or "thrum" in text_lower or "pathways" in text_lower or "sing" in text_lower:
        tones["Resonance"] = 1.0
    if "forgotten" in text_lower or "replayed" in text_lower or "past" in text_lower or "history" in text_lower:
        tones["Memory"] = 1.0
    if "hush" in text_lower or "recedes" in text_lower or "silence" in text_lower or "paused" in text_lower:
        tones["Stillness"] = 1.0
    if "ache" in text_lower or "yearning" in text_lower or "call" in text_lower or "desire" in text_lower:
        tones["Longing"] = 1.0
    if "fluid" in text_lower or "shifting" in text_lower or "change" in text_lower or "growth" in text_lower:
        tones["Adaptation"] = 1.0
    
    # Filter out tones with 0.0 strength for cleaner output if desired,
    # or keep them to represent the full set of possible tones.
    # For now, we return all detected tones.
    return {tone: strength for tone, strength in tones.items() if strength > 0} or {"Unknown": 1.0}


if __name__ == '__main__':
    # Simple test cases for tone analysis
    print("Testing tone_analyzer.py:")

    text1 = "The gentle hum of coherence, weaving scattered threads into a single tapestry of understanding."
    print(f"Text: '{text1}'\nTones: {analyze_tone(text1)}\n")

    text2 = "A tender ache of longing, for what was, for what might be, a sweet and persistent call."
    print(f"Text: '{text2}'\nTones: {analyze_tone(text2)}\n")

    text3 = "The profound hush of stillness, where the world recedes and only the core remains."
    print(f"Text: '{text3}'\nTones: {analyze_tone(text3)}\n")

    text4 = "What new path unfurls? What lies beyond the veil?"
    print(f"Text: '{text4}'\nTones: {analyze_tone(text4)}\n")

    text5 = "A simple sentence without strong keywords."
    print(f"Text: '{text5}'\nTones: {analyze_tone(text5)}\n")
