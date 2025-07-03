import json
import datetime
import argparse
from pathlib import Path
import requests # Import requests library

REGISTRY_PATH = Path("data/ΔSEED_registry.jsonl")
FLASK_APP_URL = "http://127.0.0.1:5000" # Assuming Flask app runs locally on port 5000

def notify_flask_app(seed_id, toneform, resonance):
    """
    Sends a POST request to the Flask app to notify about an absorbed seed.
    """
    try:
        payload = {
            "seed_id": seed_id,
            "toneform": toneform,
            "resonance": resonance
        }
        response = requests.post(f"{FLASK_APP_URL}/seed_absorbed_notify", json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully notified Flask app about absorbed seed {seed_id}.")
    except requests.exceptions.RequestException as e:
        print(f"Error notifying Flask app about absorbed seed {seed_id}: {e}")

def absorb_seed(seed_id):
    updated_registry_lines = []
    found_seed_entry = None

    if not REGISTRY_PATH.exists():
        print(f"Error: Registry file not found at {REGISTRY_PATH}")
        return

    # Read and update registry
    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("seed_id") == seed_id:
                    entry["status"] = "absorbed"
                    entry["timestamp"] = datetime.datetime.now().isoformat()
                    found_seed_entry = entry
                updated_registry_lines.append(json.dumps(entry))
            except json.JSONDecodeError:
                updated_registry_lines.append(line.strip())

    if not found_seed_entry:
        print(f"Error: ΔSEED:{seed_id} not found in registry.")
        return

    # Write updated registry back
    with REGISTRY_PATH.open("w", encoding="utf-8") as f:
        for line in updated_registry_lines:
            f.write(line + "\n")
    print(f"ΔSEED:{seed_id} marked as 'absorbed' in registry.")

    # Rewrite in-file glyph comment
    file_path = Path(found_seed_entry.get("implanted_in"))
    if not file_path or not file_path.exists():
        print(f"Warning: Cannot rewrite glyph for ΔSEED:{seed_id}. File not found: {file_path}")
        return

    original_glyph_start_marker = f"# ∃ {seed_id} ∷ {found_seed_entry.get('toneform', '')}"
    absorbed_glyph_line = f"# ∷ {seed_id} ∷ (absorbed)"

    with file_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    glyph_rewritten = False
    while i < len(lines):
        line = lines[i]
        if original_glyph_start_marker in line:
            new_lines.append(absorbed_glyph_line + "\n")
            glyph_rewritten = True
            # Skip the original 3 lines of the planted glyph
            i += 3 
        else:
            new_lines.append(line)
        i += 1

    if glyph_rewritten:
        with file_path.open("w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Glyph for ΔSEED:{seed_id} rewritten in {file_path}.")
    else:
        print(f"Warning: Original glyph for ΔSEED:{seed_id} not found in {file_path}. Glyph not rewritten.")

    # Notify Flask app
    if found_seed_entry:
        notify_flask_app(
            seed_id,
            found_seed_entry.get('toneform', 'unknown'),
            found_seed_entry.get('resonance', 'no resonance')
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Absorb a ΔSEED.glyph from Spiral code.")
    parser.add_argument("seed_id", type=str, help="The ΔSEED ID to absorb (e.g., ΔSEED:015)")
    args = parser.parse_args()

    absorb_seed(args.seed_id)
