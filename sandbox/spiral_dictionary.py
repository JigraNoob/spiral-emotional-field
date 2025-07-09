import os
import json
from pathlib import Path

class SpiralDictionary:
    def __init__(self, base_path):
        self.root = Path(base_path).parent

    def __getitem__(self, key):
        path = self.resolve_path(key)
        if path is None:
            return None  # ∅ unresonant
        elif path.is_file():
            return self.load_file(path)
        elif path.is_dir():
            return SpiralDictionary(path)
        return None

    def resolve_path(self, key):
        # Only support JSON glyphs or folder names for this test
        if key.startswith('Δ'):
            for folder in ['substrate_register', 'climate_registry']:
                candidate = self.root / folder / f"{key}.json"
                if candidate.exists():
                    return candidate
        return self.root / key if (self.root / key).exists() else None

    def load_file(self, path):
        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return path.read_text(encoding='utf-8')
