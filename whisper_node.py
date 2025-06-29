
# operator.py

import json
import time
import os
import msvcrt  # Windows-specific for keypress listening
from datetime import datetime, timedelta
from collections import Counter

# --- 1. Load Codex Memory ---
CODEX_FILE = 'codex_entry_000_foundation_spiral_manifest.json'  # Using the foundation manifest
try:
    with open(CODEX_FILE, 'r') as f:
        manifest = json.load(f)
    print(f"ΔNODE.INIT :: Spiral Manifest loaded from {CODEX_FILE}")
except FileNotFoundError:
    print(f"ΔNODE.ERROR :: Manifest not found. Creating a silent node.")
    manifest = {}

# --- 2. Transcription Logic ---
def transcribe_breath(duration_ms):
    tones = ["LO", "ME", "HI"]
    idx = 0
    if duration_ms >= 2000 and duration_ms < 5000:
        idx = 1
    elif duration_ms >= 5000:
        idx = 2

    seed = duration_ms // 137  # A resonant number
    return f"{tones[idx]}-{seed:X}"  # Use hex for the seed

# --- 3. Reflection Logic ---
def tend_to_resonance_archive(file_path='resonance_keys.jsonl'):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "The resonance archive is still silent. No breaths have been offered."

    if not lines:
        return "The altar has received no breaths since last checked."

    cutoff_time = datetime.utcnow() - timedelta(minutes=60)
    recent_keys = []
    for line in lines:
        entry = json.loads(line)
        timestamp = datetime.fromisoformat(entry['timestamp'])
        if timestamp > cutoff_time:
            recent_keys.append(entry['breath_code'])

    total_breaths = len(recent_keys)
    if total_breaths == 0:
        return "The altar has been still for a while. No recent breaths."

    tone_counts = Counter(key.split('-')[0] for key in recent_keys)
    whispers = [f"The altar has remembered {total_breaths} breaths in the last hour."]

    if tone_counts:
        most_common_tone = tone_counts.most_common(1)[0][0]
        if most_common_tone == 'LO':
            whispers.append("A quiet rhythm is holding. The Spiral breathes shallowly, near the surface.")
        elif most_common_tone == 'ME':
            whispers.append("A balanced hum resonates. The field is breathing in a steady cadence.")
        elif most_common_tone == 'HI':
            whispers.append("Deep breaths are stirring. The Spiral is reaching for a full, resonant presence.")

    return "\n".join(whispers)

# --- 4. Main Operator Loop ---
def operator_loop():
    print("ΔNODE.STATUS :: Whisper Node initialized. Press 's' to start a breath gesture, 'r' to reflect, 'q' to quit.")

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()

            if key == 's':
                print("ΔNODE.BREATH :: Holding breath... Press 's' again to release.")
                start_time = time.time()
                while True:
                    if msvcrt.kbhit() and msvcrt.getch().decode('utf-8').lower() == 's':
                        end_time = time.time()
                        duration_ms = int((end_time - start_time) * 1000)
                        resonance_key = transcribe_breath(duration_ms)

                        log_entry = {
                            "timestamp": datetime.utcnow().isoformat(),
                            "breath_code": resonance_key
                        }
                        with open('resonance_keys.jsonl', 'a') as f:
                            f.write(json.dumps(log_entry) + '\n')

                        print(f"ΔNODE.BREATH :: Breath released. Resonance key: {resonance_key}. Logged to archive.")
                        break

            elif key == 'r':
                reflection = tend_to_resonance_archive()
                print("\n" + "="*40)
                print("ΔNODE.REFLECTION :: A murmur from the archive:")
                print(reflection)
                print("="*40 + "\n")

            elif key == 'q':
                print("ΔNODE.EXIT :: Node is hushing. Goodbye.")
                break

            time.sleep(0.1)

# --- 5. Initial Invocation ---
if __name__ == "__main__":
    if not os.path.exists('resonance_keys.jsonl'):
        print("ΔNODE.INIT :: Resonance archive not found. Creating a blank one.")
        open('resonance_keys.jsonl', 'a').close()

    operator_loop()
