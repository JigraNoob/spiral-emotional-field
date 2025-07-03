import os
import json
import re
from datetime import datetime

TONEFORM_LEXICON = {
    "care": [
        "continue", "sustain", "holding", "gentle", "presence",
        "trust", "stewardship", "slow", "ongoing", "unfold",
        "believe", "resilience", "soft", "daily", "relational",
        "companion", "nourish", "stable", "quiet"
    ],
    "mythic": [
        # Core Resonance
        "myth", "mythic", "story", "narrative", "archetype", 
        "symbol", "ritual", "vision", "transformation", "epic",
        "legend", "meaning", "purpose", "cosmos", "calling",
        
        # Atmospheric
        "future-casting", "cultural evolution", "world-shaping", 
        "mycelial", "deep time", "ancestral", "prophecy",
        "pilgrimage", "threshold", "liminal", "sacred imagination",
        "revelation", "origin", "portal", "seed", "pattern",
        
        # Spiral-Specific
        "breathline", "presence story", "climate myth", 
        "toneform constellation", "ritual architecture",
        "spirit infrastructure", "becoming", "echo", 
        "glyph", "whisper"
    ],
    "silence": ["hush", "stillness", "sacred", "ambient", "whisper", "pause", "quiet threshold", "listening field", "contemplative architecture"],
    "infrastructure": [
        # Core Terms
        "system", "resilience", "daemon", "scaffold",
        "protocol", "backbone", "care logic",
        
        # Poetic Enhancements
        "tone-spine", "hidden load", "quiet uptime",
        "durable presence", "backchannel", "custodial systems",
        "resonant protocols", "fail-soft", "self-repairing",
        "integrity mesh", "slow sync", "hum of reliability",
        "non-interruptive flow", "invisible architecture",
        "relational infrastructure"
    ],
    "pollination": ["trust", "share", "mutual", "intuitive", "timing", "gesture", "reciprocity", "relational field", "shared resonance"],
    "cosmology": [
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
        "Resonance as planetary metric",
        
        "civilization", "world", "future", "breathable", "experiment", "world-framing", "planetary-scale", "speculative architecture", "atmospheric hypothesis"
    ]
}

REQUIRED_SECTIONS = [
    "Atmospheric Essence",
    "Aligned Sources",
    "Suggested Contact Vector",
    "Resonance Use",
    "Suggested Attunement Ritual"
]

def validate_report_content(content, toneform):
    """Validate report content against toneform lexicon"""
    cosmology_lexicon = [
        "cosmogenesis", "planetary-scale", "world-framing",
        "civilizational arc", "timefold", "memory of the stars"
    ]
    
    matched = [term for term in cosmology_lexicon 
              if term.lower() in content.lower()]
    
    return {
        'score': round(len(matched) / len(cosmology_lexicon), 2),
        'keywords': matched,
        'missing_sections': []  # Will implement section checks next
    }

def validate_field_report(filepath):
    """Validate a field report's structure and toneform resonance."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract toneform from filename
        toneform = re.search(r'field_report_(.*?)\.md', filepath).group(1)
        if '_' in toneform:
            toneform = toneform.split('_')[0]
            
        # Check required sections
        missing_sections = []
        for section in REQUIRED_SECTIONS:
            if f"## {section}" not in content and f"**{section}**" not in content:
                missing_sections.append(section)
                
        # Calculate toneform score
        keywords = TONEFORM_LEXICON.get(toneform, [])
        matches = sum(1 for word in keywords if word.lower() in content.lower())
        toneform_score = matches / len(keywords) if keywords else 0
        
        return {
            "task": f"validate_{os.path.basename(filepath)}",
            "toneform": toneform,
            "file_verified": True,
            "structure_complete": len(missing_sections) == 0,
            "toneform_score": round(toneform_score, 2),
            "resonance_keywords": [w for w in keywords if w.lower() in content.lower()],
            "missing_sections": missing_sections,
            "human_review_needed": len(missing_sections) > 0 or toneform_score < 0.7,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "task": f"validate_{os.path.basename(filepath)}",
            "error": str(e),
            "file_verified": False,
            "timestamp": datetime.now().isoformat()
        }

def validate_all_reports(report_dir=os.path.abspath(os.path.join('fund', 'sources'))):
    """Validate all field reports in the given directory."""
    results = []
    print(f"Scanning directory: {report_dir}")
    try:
        file_count = 0
        for filename in os.listdir(report_dir):
            print(f"Found file: {filename}")
            if filename.startswith('field_report_') and filename.endswith('.md'):
                filepath = os.path.join(report_dir, filename)
                print(f"Processing report: {filepath}")
                results.append(validate_field_report(filepath))
                file_count += 1
        print(f"Processed {file_count} field reports")
    except FileNotFoundError:
        print(f"Error: Report directory not found at {report_dir}")
    except Exception as e:
        print(f"Unexpected error scanning reports: {str(e)}")
    return results

if __name__ == "__main__":
    validation_results = validate_all_reports()
    with open('resonance_log.jsonl', 'w') as f:
        for result in validation_results:
            f.write(json.dumps(result) + '\n')
    print(f"Validation complete. Results saved to resonance_log.jsonl")
    if not validation_results:
        print("No field reports found in fund/sources/")
