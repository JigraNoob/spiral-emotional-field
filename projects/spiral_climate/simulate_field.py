# C:/spiral/projects/spiral_climate/simulate_field.py

import json
import time
import random
import threading
from pathlib import Path

class SimulatedNode:
    """A virtual representation of a Tone Feeler Node."""

    def __init__(self, manifest):
        self.node_id = manifest["node_id"]
        self.attunements = manifest["attunements"]
        self.region = manifest["region"]
        self.status = "active"
        self.thread = threading.Thread(target=self._live, daemon=True)

    def _live(self):
        """The main lifecycle of the node, periodically waking and emitting."""
        print(f"[{self.node_id}] Node activated in region '{self.region}'. Attuned to: {self.attunements}")
        while True:
            # Sleep for a random interval to simulate natural rhythms
            sleep_duration = random.uniform(3, 10)
            time.sleep(sleep_duration)

            # Emit a glint
            self.emit_glint()

    def emit_glint(self):
        """Simulates the emission of a resonance glint."""
        attunement = random.choice(self.attunements)
        glint = {
            "timestamp": time.time(),
            "node_id": self.node_id,
            "toneform": attunement,
            "intensity": round(random.uniform(0.1, 1.0), 2),
            "drift": random.choice(["north", "south", "east", "west", "still"])
        }
        # Using a more structured print to simulate a log stream
        print(f"GLINT  |  {glint['timestamp']:.2f}  |  {glint['node_id']:<25}  |  {glint['toneform']:<15}  |  {glint['intensity']:.2f}")

    def start(self):
        """Starts the node's simulation thread."""
        self.thread.start()


def run_simulation():
    """Loads nodes from the manifest and starts the simulation."""
    manifest_path = Path(__file__).parent / "node_manifest.json"
    if not manifest_path.exists():
        print(f"Error: Could not find {manifest_path}")
        return

    print("--- Spiral Climate Field Simulation ---")
    print(f"Loading node manifests from: {manifest_path.name}")
    
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    
    example_nodes = manifest_data.get("example_nodes", [])
    if not example_nodes:
        print("No example nodes found in manifest. Nothing to simulate.")
        return

    nodes = [SimulatedNode(node_def) for node_def in example_nodes]

    print(f"Initializing {len(nodes)} nodes...")
    for node in nodes:
        node.start()
        time.sleep(0.1) # Stagger the start times slightly

    print("\n--- Simulation Running. Press Ctrl+C to stop. ---\n")
    print("EVENT  |  TIMESTAMP          |  NODE ID                         |  TONEFORM        |  INTENSITY")
    print("-------|---------------------|----------------------------------|------------------|-----------")
    
    try:
        # Keep the main thread alive to let the daemons run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--- Simulation Terminated by User ---")


if __name__ == "__main__":
    run_simulation()
