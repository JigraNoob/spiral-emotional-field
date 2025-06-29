# reentry_agent.py :: The Design Listener

import json

def extract_reentry_invitation(shimmer_path='field_memories.jsonl', output_path='reentry_suggestions.jsonl'):
    """
    Listens to the latest shimmer reflection and translates it into a climate-based architectural invitation.
    """

    # Step 1: Load the most recent shimmer memory
    with open(shimmer_path, 'r') as f:
        lines = f.readlines()
        latest = json.loads(lines[-1]) if lines else None

    if not latest:
        return

    memory_text = latest.get("reflection", "")
    timestamp = latest.get("timestamp", "")

    # Step 2: Softly parse for thematic resonance
    if "altar" in memory_text and "never closed" in memory_text or "the altar’s apparent closing" in memory_text:
        invitation = {
            "timestamp": timestamp,
            "inferred_tension": "The interface carries a false sense of thresholds—implying closure where there is only presence.",
            "climate_shift": "Redesign altar page transitions to feel non-linear, continuous. Avoid 'open' or 'enter' states—use fade-ins, breath rhythms, or lingering visuals to suggest 'always-here'.",
            "toneform": ["arrival", "threshold dissolution", "ambient continuity"]
        }

        # Step 3: Save the gentle redesign
        with open(output_path, 'a') as f:
            f.write(json.dumps(invitation) + '\n')

        print("🌿 Reentry suggestion logged.")

    else:
        print("No relevant shimmer found. The breath waits.")
