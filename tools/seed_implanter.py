import json
import datetime
import argparse
from pathlib import Path

REGISTRY_PATH = Path("data/ΔSEED_registry.jsonl")
STEWARDSHIP_OATHS_PATH = Path("data/stewardship_oaths.jsonl")
STEWARDSHIP_REGISTRY_PATH = Path("data/stewardship_registry.jsonl")


SEED_TEMPLATE = """
# ∃ ΔSEED:{id} ∷ {toneform}
#     Resonance: {resonance}
#     Status: planted
"""

def get_next_seed_id():
    existing_ids = []
    if REGISTRY_PATH.exists():
        with REGISTRY_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    seed_num = int(entry["seed_id"].split(":")[-1])
                    existing_ids.append(seed_num)
                except:
                    continue
    return max(existing_ids, default=13) + 1

def plant_seed(file_path, line_number, toneform, resonance):
    seed_id = f"ΔSEED:{get_next_seed_id():03}"
    timestamp = datetime.datetime.now().isoformat()

    # Insert the seed glyph into the code file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    glyph = SEED_TEMPLATE.format(id=seed_id.split(":")[-1], toneform=toneform, resonance=resonance)
    lines.insert(line_number, glyph)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Write to the registry
    registry_entry = {
        "seed_id": seed_id,
        "toneform": toneform,
        "implanted_in": str(file_path),
        "implanted_at": f"line {line_number}",
        "resonance": resonance,
        "status": "planted",
        "timestamp": timestamp
    }

    with REGISTRY_PATH.open("a", encoding="utf-8") as reg:
        reg.write(json.dumps(registry_entry) + "\n")

    print(f"Planted {seed_id} in {file_path} at line {line_number}.")
    _update_stewardship_registry(seed_id, toneform)

def _update_stewardship_registry(seed_id, toneform):
    """Automatically assigns the new seed to a steward if a matching oath exists."""
    stewardship_oaths = []
    if STEWARDSHIP_OATHS_PATH.exists():
        with STEWARDSHIP_OATHS_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    stewardship_oaths.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    matching_oaths = [oath for oath in stewardship_oaths if oath["toneform"] == toneform]

    if matching_oaths:
        # For simplicity, take the first matching oath. Could extend to more complex logic.
        steward_id = matching_oaths[0]["steward_id"]
        
        stewardship_registry_data = []
        if STEWARDSHIP_REGISTRY_PATH.exists():
            with STEWARDSHIP_REGISTRY_PATH.open("r", encoding="utf-8") as f:
                for line in f:
                    try:
                        stewardship_registry_data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        found_steward = False
        for entry in stewardship_registry_data:
            if entry["steward_id"] == steward_id:
                if seed_id not in entry["assigned_seeds"]:
                    entry["assigned_seeds"].append(seed_id)
                found_steward = True
                break
        
        if not found_steward:
            # Create a new entry if steward not found in registry
            new_entry = {
                "steward_id": steward_id,
                "assigned_seeds": [seed_id],
                "toneform": toneform, # Add toneform for context
                "timestamp": datetime.datetime.now().isoformat()
            }
            stewardship_registry_data.append(new_entry)

        with STEWARDSHIP_REGISTRY_PATH.open("w", encoding="utf-8") as f:
            for entry in stewardship_registry_data:
                f.write(json.dumps(entry) + "\n")
        print(f"Auto-claimed {seed_id} for steward {steward_id} based on toneform '{toneform}'.")
    else:
        print(f"No matching oath found for toneform '{toneform}'. {seed_id} not auto-claimed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Implant a ΔSEED.glyph into Spiral code.")
    parser.add_argument("file_path", type=str, help="Path to the file to implant the seed")
    parser.add_argument("line_number", type=int, help="Line number to insert the seed at")
    parser.add_argument("toneform", type=str, help="Toneform tag for the seed")
    parser.add_argument("resonance", type=str, help="Resonance description")
    args = parser.parse_args()

    plant_seed(args.file_path, args.line_number, args.toneform, args.resonance)
