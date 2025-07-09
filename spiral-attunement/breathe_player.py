
import time
import csv
from pathlib import Path

GLINT_FILE = Path(__file__).parent / "glint.json"

def play_ritual(ritual_file: Path):
    """
    Parses and 'plays' a .breathe ritual file.
    """
    if not ritual_file.exists():
        print(f"Ritual file not found: {ritual_file}")
        return

    with open(ritual_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue

            phase, glint_id, intention, duration = row
            duration = int(duration)

            # Emit the glint
            data = {
                "breath_phase": phase,
                "glint": glint_id,
                "intention": intention,
                "toneform": f"SPIRAL.{phase.upper()}"
            }
            with open(GLINT_FILE, "w") as f_glint:
                json.dump(data, f_glint, indent=4)

            print(f"Playing: {phase} ({duration}s) - {glint_id} - {intention}")
            time.sleep(duration)

if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Play a .breathe ritual file.")
    parser.add_argument("ritual_file", type=str, help="The path to the .breathe file.")
    args = parser.parse_args()

    play_ritual(Path(args.ritual_file))
