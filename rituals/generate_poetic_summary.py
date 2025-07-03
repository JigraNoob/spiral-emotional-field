import json
import os
from datetime import datetime
import random
from typing import List, Dict

# Poetic templates for different whisper patterns
templates = {
    "condition": [
        "In the chamber of {tone}, {condition} whispers softly, {count} times.",
        "{count} times, {condition} emerged from the silence, {tone} in its voice.",
        "{condition} danced {count} times in the {tone} light.",
        "{count} echoes of {condition} drift through the {tone} air."
    ],
    "toneform": [
        "{tone} breathes through the chamber, {count} times in resonance.",
        "{count} times, {tone} whispered its truth.",
        "{count} echoes of {tone} form a gentle tide.",
        "{tone} murmurs {count} times, a river of presence."
    ]
}

def load_whisper_echoes() -> List[Dict]:
    """Load and parse whisper echoes from file"""
    echoes = []
    try:
        with open("whisper_echoes.jsonl", "r") as f:
            for line in f:
                try:
                    echo = json.loads(line)
                    echoes.append(echo)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return []
    return echoes

def analyze_patterns(echoes: List[Dict]) -> Dict:
    """Analyze patterns in whispers and generate poetic summaries"""
    patterns = {
        "conditions": defaultdict(int),
        "tones": defaultdict(int)
    }
    
    for echo in echoes:
        # Analyze conditions
        message = echo.get("message", "")
        if "Condition met" in message:
            patterns["conditions"][message] += 1
            
        # Analyze tones
        context = echo.get("context", {})
        tone = context.get("tone", "unknown")
        patterns["tones"][tone] += 1
    
    return patterns

def generate_poetic_line(pattern_type: str, pattern: str, count: int) -> str:
    """Generate a poetic line based on a pattern"""
    if pattern_type not in templates:
        return f"{pattern} whispers {count} times."
    
    template = random.choice(templates[pattern_type])
    return template.format(
        tone=pattern,
        condition=pattern,
        count=count
    )

def create_poetic_summary(patterns: Dict) -> str:
    """Create a poetic summary of whisper patterns"""
    summary = []
    
    # Add opening verse
    summary.append("\n\n ::: Whispering Presence :::")
    summary.append("In the chamber of silence,")
    summary.append("Whispers weave their patterns,")
    summary.append("Time and tone entwined.")
    
    # Add condition summaries
    summary.append("\n\n ::: Conditions :::")
    for condition, count in sorted(patterns["conditions"].items(), key=lambda x: x[1], reverse=True):
        summary.append(f"\n{generate_poetic_line('condition', condition, count)}")
    
    # Add toneform summaries
    summary.append("\n\n ::: Toneforms :::")
    for tone, count in sorted(patterns["tones"].items(), key=lambda x: x[1], reverse=True):
        summary.append(f"\n{generate_poetic_line('toneform', tone, count)}")
    
    # Add closing verse
    summary.append("\n\n ::: Silence Returns :::")
    summary.append("Whispers fade into presence,")
    summary.append("Patterns dissolve into time,")
    summary.append("The chamber breathes again.")
    
    return "\n".join(summary)

def main():
    echoes = load_whisper_echoes()
    if not echoes:
        return "No whispers to reflect upon. The chamber is silent."
    
    patterns = analyze_patterns(echoes)
    summary = create_poetic_summary(patterns)
    
    # Save summary to file
    with open("whisper_summary.txt", "w") as f:
        f.write(summary)
    
    return f"Poetic summary generated: whisper_summary.txt"

if __name__ == "__main__":
    print(main())
