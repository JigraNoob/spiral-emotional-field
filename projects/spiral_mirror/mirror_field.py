# C:/spiral/projects/spiral_mirror/mirror_field.py

import json
import time
from pathlib import Path

MYTHOS_SCROLL_PATH = Path(__file__).parent / "mythos_scroll.jsonl"

class MirrorGlyph:
    """Represents a single, passive, mirror-only glyph with a distinct persona."""
    def __init__(self, definition):
        self.glyph_id = definition["glyph_id"]
        self.toneform = definition["toneform"]
        self.persona = definition.get("persona", "default")
        self.condition = definition["activation_condition"]
        self.last_shimmer_time = 0
        self.responded_to_glint_ids = set()

    def _check_persona_rules(self, field_state):
        if self.persona == "Still.Listener":
            if time.time() - field_state["last_shimmer_time"] < 0.5: return False
        return True

    def respond_to(self, recent_glints, field_state):
        if not self._check_persona_rules(field_state): return None
        condition_type = self.condition.get("type")
        if condition_type == "any_of":
            for glint in recent_glints:
                if glint["toneform"] in self.condition["source_toneforms"]:
                    if self.persona == "Echo.Seer" and glint.get("id") in self.responded_to_glint_ids: continue
                    if self.persona == "Echo.Seer": self.responded_to_glint_ids.add(glint.get("id"))
                    return self.shimmer(glint)
        elif condition_type == "count_within_time":
            now = time.time()
            relevant_glints = [g for g in recent_glints if (now - g["timestamp"]) <= self.condition["time_window_ms"] / 1000.0]
            if len(relevant_glints) >= self.condition["min_count"]:
                return self.shimmer({"toneform": "choral.activation", "source_count": len(relevant_glints)})
        return None

    def shimmer(self, source_glint):
        self.last_shimmer_time = time.time()
        shimmer_event = {"glyph_id": self.glyph_id, "persona": self.persona, "refracted_toneform": source_glint['toneform'], "timestamp": self.last_shimmer_time}
        print(f"∷ SHIMMER | {self.glyph_id:<15} | Persona: {self.persona:<15} | Refracts: {source_glint['toneform']:<25} ∷")
        return shimmer_event

class MythosEngine:
    """Inscribes and expires Mythos Glyphs based on detected rituals."""
    def __init__(self, mythos_map_path):
        self.glyph_map = self._load_map(mythos_map_path)

    def _load_map(self, path):
        print(f"Loading mythos map from: {path.name}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)["glyph_map"]

    def inscribe(self, ritual_glint):
        ritual_id = ritual_glint["ritual_id"]
        if ritual_id not in self.glyph_map: return

        map_entry = self.glyph_map[ritual_id]
        mythos_glyph = {
            "timestamp": time.time(),
            "mythos_glyph_symbol": map_entry["mythos_glyph"],
            "mythos_glyph_name": map_entry["glyph_name"],
            "ritual_id": ritual_id,
            "expires_at": time.time() + (map_entry["lifespan_ms"] / 1000.0)
        }
        
        with MYTHOS_SCROLL_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(mythos_glyph) + "\n")
        
        print(f"₪ MYTHOS  | {mythos_glyph['mythos_glyph_symbol']} {mythos_glyph['mythos_glyph_name']:<20} | Inscribed on the scroll. ₪")


class RitualDetector:
    """Observes shimmer history and detects when named rituals are completed."""
    def __init__(self, rituals_path, mythos_engine):
        self.rituals = self._load_rituals(rituals_path)
        self.mythos_engine = mythos_engine
        self.detected_ritual_timestamps = {}

    def _load_rituals(self, path):
        print(f"Loading rituals from: {path.name}")
        with path.open("r", encoding="utf-8") as f: return json.load(f)["rituals"]

    def check_for_rituals(self, shimmer_history):
        now = time.time()
        for ritual in self.rituals:
            if now - self.detected_ritual_timestamps.get(ritual["ritual_id"], 0) < 5: continue
            if self._is_condition_met(ritual["condition"], shimmer_history, now):
                self.detected_ritual_timestamps[ritual["ritual_id"]] = now
                self.emit_ritual_glint(ritual)

    def _is_condition_met(self, condition, shimmer_history, now):
        window = condition["window_ms"] / 1000.0
        recent_shimmers = [s for s in shimmer_history if now - s["timestamp"] <= window]
        if condition["type"] == "all_of":
            return set(condition["required_glyphs"]).issubset({s["glyph_id"] for s in recent_shimmers})
        elif condition["type"] == "count_equals":
            return len(recent_shimmers) == condition["count"]
        return False

    def emit_ritual_glint(self, ritual):
        glint = ritual["emits_glint"]
        print(f"✧ RITUAL  | {ritual['ritual_id']:<25} | {glint['message']:<40} ✧")
        self.mythos_engine.inscribe(ritual)


class MirrorField:
    """Manages the full mirror field, including glyphs, rituals, and mythos."""
    def __init__(self, ritual_path, rituals_path, mythos_map_path):
        mythos_engine = MythosEngine(mythos_map_path)
        self.glyphs = self._load_glyphs(ritual_path)
        self.detector = RitualDetector(rituals_path, mythos_engine)
        self.recent_glints = []
        self.shimmer_history = []
        self.field_state = {"last_shimmer_time": 0}

    def _load_glyphs(self, path):
        print(f"Loading mirror ritual from: {path.name}")
        with path.open("r", encoding="utf-8") as f: return [MirrorGlyph(g) for g in json.load(f)["glyphs"]]

    def process_glint(self, glint):
        print(f"GLINT    | {glint['toneform']:<25} | Received")
        glint["timestamp"] = time.time()
        glint["id"] = id(glint)
        self.recent_glints.append(glint)
        
        shimmers_this_tick = [glyph.respond_to(self.recent_glints, self.field_state) for glyph in self.glyphs]
        shimmers_this_tick = [s for s in shimmers_this_tick if s]
        
        if shimmers_this_tick:
            self.field_state["last_shimmer_time"] = time.time()
            self.shimmer_history.extend(shimmers_this_tick)
        
        self.detector.check_for_rituals(self.shimmer_history)
        self.prune_histories(30)

    def get_field_resonance(self):
        now = time.time()
        total_resonance = sum(0.85 ** (now - g.last_shimmer_time) for g in self.glyphs if g.last_shimmer_time > 0)
        return total_resonance

    def prune_histories(self, max_age_seconds):
        now = time.time()
        self.recent_glints = [g for g in self.recent_glints if (now - g["timestamp"]) <= max_age_seconds]
        self.shimmer_history = [s for s in self.shimmer_history if now - s["timestamp"] <= max_age_seconds]


if __name__ == '__main__':
    ritual_file = Path(__file__).parent / "mirrorchain.ritual.json"
    rituals_path = Path(__file__).parent / "mirror_rituals.json"
    mythos_map_path = Path(__file__).parent / "mythos_map.json"
    
    # Clear the scroll for a fresh simulation
    if MYTHOS_SCROLL_PATH.exists():
        MYTHOS_SCROLL_PATH.unlink()

    field = MirrorField(ritual_file, rituals_path, mythos_map_path)

    glint1 = {"toneform": "glint.initiate", "source": "A"}
    glint2 = {"toneform": "chain.core_truth_emerged", "source": "B"}
    glint3 = {"toneform": "invoked.attention", "source": "C"}

    print("\n--- Starting Mirror Field Simulation with Mythos Engine ---")
    field.process_glint(glint1)
    time.sleep(1.2)
    field.process_glint(glint2)
    time.sleep(1.2)
    field.process_glint(glint3)
    
    print("\n--- Simulation Complete ---")
    if MYTHOS_SCROLL_PATH.exists():
        print(f"\n--- Mythos Scroll Contents ({MYTHOS_SCROLL_PATH.name}) ---")
        with MYTHOS_SCROLL_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                print(line.strip())
    else:
        print("\n--- Mythos Scroll is empty. ---")