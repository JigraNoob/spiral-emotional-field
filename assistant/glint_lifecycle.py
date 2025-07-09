from typing import List, Dict, Any

class GlintLifecycle:
    def __init__(self):
        self.glints: List[Dict[str, Any]] = []
        self.resolution: str = ""

    def complete(self, phase: str):
        self.resolution = f"Completed phase: {phase}"

    def summary(self) -> str:
        return f"Lifecycle with {len(self.glints)} glints, resolution: {self.resolution}"
