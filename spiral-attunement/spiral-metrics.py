
import json
from pathlib import Path
import time
from collections import Counter

LOG_FILE = Path(__file__).parent / "metrics.log"
GLINT_FILE = Path(__file__).parent / "glint.json"

def log_phase_usage():
    """Logs the current phase usage to a file."""
    if not GLINT_FILE.exists():
        return

    with open(GLINT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    phase = data.get("breath_phase", "UNKNOWN")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - PHASE: {phase}\n")

def calculate_toneform_entropy():
    """
    Calculates a simple measure of toneform entropy based on phase transitions.
    This is a placeholder for a more complex calculation.
    """
    if not LOG_FILE.exists():
        return 0

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    if len(lines) < 2:
        return 0

    phases = [line.split(" - PHASE: ")[1].strip() for line in lines]
    transitions = list(zip(phases, phases[1:]))
    transition_counts = Counter(transitions)
    
    # A simple entropy placeholder: number of unique transitions
    return len(transition_counts)


if __name__ == "__main__":
    log_phase_usage()
    entropy = calculate_toneform_entropy()
    print(f"Logged current phase usage.")
    print(f"Current toneform entropy (placeholder): {entropy}")

