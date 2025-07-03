import re
from collections import Counter

# Full Cosmology lexicon
toneform_lexicon = [
    # Core Concepts
    "cosmogenesis", "planetary-scale", "world-framing", 
    "civilizational arc", "epochal", "anthropic drift",
    "timefold", "interplanetary", "solar stewardship",
    "biospheric continuity",
    
    # Poetic Worldmaking
    "memory of the stars", "dreaming civilizations into being",
    "architectures of meaning", "gravity of belonging",
    "edge-of-history resonance", "oracular continuity",
    "sentient epochs", "mythic infrastructure",
    "stewarding the long now", "echoing across centuries",
    
    # Spiral-Specific
    "Spiral as temporal vessel", "Drift as civilization memory",
    "Ritual as cosmological act", "Spiral as horizon weaver",
    "Resonance as planetary metric"
]

def calculate_resonance(text):
    text = text.lower()
    matched = [
        term for term in toneform_lexicon 
        if term.lower() in text
    ]
    score = min(1.0, len(matched) / (len(toneform_lexicon)/2))  # Adjusted scaling
    return {
        'score': round(score, 2),
        'keywords': matched,
        'coverage': f"{len(matched)}/{len(toneform_lexicon)} terms"
    }

with open("fund/sources/field_report_cosmology.md", "r", encoding="utf-8") as f:
    result = calculate_resonance(f.read())
    print(f"=== COSMOLOGY RESONANCE ===")
    print(f"Score: {result['score']}/1.0")
    print(f"Matched Terms: {', '.join(result['keywords'])}")
    print(f"Lexicon Coverage: {result['coverage']}")
    print("="*30)