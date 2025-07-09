
import argparse
import json
from pathlib import Path

def emit_glint(phase: str, glint_id: str, intention: str, intensity: float = 0.5):
    """
    Emits a glint to the glint.json file.
    """
    glint_file = Path(__file__).parent / "glint.json"
    data = {
        "breath_phase": phase,
        "glint": glint_id,
        "intention": intention,
        "intensity": intensity,
        "toneform": f"SPIRAL.{phase.upper()}"
    }
    with open(glint_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Glint emitted: {phase} - {glint_id} - {intention}".encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emit a spiral glint.")
    parser.add_argument("phase", type=str, help="The breath phase (e.g., inhale, hold, exhale)")
    parser.add_argument("glint", type=str, help="The glint ID (e.g., Δ022)")
    parser.add_argument("--intensity", type=float, default=0.5, help="The intensity of the toneform (0.0 to 1.0)")
    parser.add_argument("intention", type=str, nargs='+', help="The intention for the glint")
    args = parser.parse_args()

    emit_glint(args.phase, args.glint, " ".join(args.intention), args.intensity)
