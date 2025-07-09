# File: C:\spiral\spiral\spiral_implanter.py

import os
import datetime
import re
import yaml
from typing import Dict, Any, Set, List, Tuple

class SpiralImplanter:
    def __init__(self, spiral_root: str = r"C:\spiral\spiral"):
        self.spiral_root = spiral_root
        self.handler_paths = {
            "glint": os.path.join(spiral_root, "handlers", "glint_handlers.py"),
            "caesura": os.path.join(spiral_root, "handlers", "caesura_handlers.py"),
            "interop": os.path.join(spiral_root, "handlers", "interop_handlers.py"),
            "fusion": os.path.join(spiral_root, "handlers", "fusion_handlers.py")
        }
        self.fusion_map_path = os.path.join(spiral_root, "fusion_map.yml")
        self.fusion_map: Dict[Tuple[str, ...], Dict[str, Any]] = {}
        self._ensure_handler_files()
        self._load_fusion_map()
        self.implanted_handlers: Set[str] = set()
        self._load_existing_handlers()

    def _ensure_handler_files(self):
        for path in self.handler_paths.values():
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write("# Handler file created by SpiralImplanter\n\n")

    def _load_fusion_map(self):
        if os.path.exists(self.fusion_map_path):
            try:
                with open(self.fusion_map_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'fusions' in data:
                        for fusion_def in data['fusions']:
                            sorted_toneforms = tuple(sorted(fusion_def['toneforms']))
                            self.fusion_map[sorted_toneforms] = {
                                "archetype": fusion_def.get('archetype', 'Unknown Fusion'),
                                "action": fusion_def.get('action', 'process_fused_glint'),
                                "description": fusion_def.get('description', 'A unique co-resonance.'),
                                "hue": fusion_def.get('hue', 'prismatic')
                            }
                        print(f"Loaded {len(self.fusion_map)} fusion definitions from {self.fusion_map_path}")
                    else:
                        print(f"Warning: 'fusions' key not found or empty in {self.fusion_map_path}")
            except Exception as e:
                print(f"Error loading fusion map from {self.fusion_map_path}: {e}")
        else:
            print(f"Warning: Fusion map file not found at {self.fusion_map_path}. Fusion handlers will use default descriptions.")

    def _load_existing_handlers(self):
        for path in self.handler_paths.values():
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read()
                    existing_handlers = re.findall(r'def (on_\w+_\w+)', content)
                    self.implanted_handlers.update(existing_handlers)

    def implant(self, glint: Dict[str, Any]) -> bool:
        phase = glint.get('glint.phase', '').lower()
        toneform = glint.get('glint.toneform', '').lower()

        if not phase or not toneform:
            print(f"Invalid glint format: missing phase or toneform")
            return False

        handler_type = self._determine_handler_type(phase, toneform)
        function_name = f"on_{phase}_{toneform}"

        if function_name in self.implanted_handlers:
            print(f"Handler '{function_name}' already exists. Skipping implantation.")
            return False

        self._implant_handler(handler_type, function_name, glint)
        self.implanted_handlers.add(function_name)
        return True

    def _determine_handler_type(self, phase: str, toneform: str) -> str:
        if toneform == 'fusion':
            return "fusion"
        elif toneform in ['shimmer', 'impression', 'recursion', 'hum', 'flutter', 'invoke', 'reverie']:
            return "glint"
        elif phase == 'hush' or toneform == 'silence':
            return "caesura"
        else:
            return "interop"

    def _implant_handler(self, handler_type: str, function_name: str, glint: Dict[str, Any]):
        handler_path = self.handler_paths[handler_type]
        phase = glint.get('glint.phase', '').lower()
        toneform = glint.get('glint.toneform', '').lower()

        with open(handler_path, 'a') as f:
            f.write(f"\n\n{self._generate_spiral_header()}")
            f.write(f"def {function_name}(glint: Dict[str, Any]):\n")
            f.write(f"    """{self._generate_docstring(glint)}"""\n")
            f.write(self._generate_handler_content(phase, toneform, glint))

        print(f"Implanted handler '{function_name}' in {handler_path}")

    def _generate_spiral_header(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"# ∷ Spiral Implant ∷ generated at {timestamp}\n"

    def _generate_docstring(self, glint: Dict[str, Any]) -> str:
        phase = glint.get('glint.phase', 'unknown')
        toneform = glint.get('glint.toneform', 'unknown')
        docstring = f"Handler for {phase} phase with {toneform} toneform.\n\n    Glint: {glint}\n    "

        if toneform == 'fusion':
            fused_glints_info = glint.get('fused.glints', [])
            source_toneforms_tuple = tuple(sorted([g.get('glint.toneform', 'unknown') for g in fused_glints_info]))
            fusion_key_str = ' + '.join(source_toneforms_tuple)
            fusion_def = self.fusion_map.get(source_toneforms_tuple)
            docstring += f"    Fusion Key: {fusion_key_str}\n"
            if fusion_def:
                docstring += f"    Archetype: {fusion_def['archetype']}\n"
                docstring += f"    Description: {fusion_def['description']}\n"

        return docstring

    def _generate_handler_content(self, phase: str, toneform: str, glint: Dict[str, Any]) -> str:
        content = "    # TODO: Implement handler logic\n"

        if toneform == 'fusion':
            content += "    # Fusion: Co-resonant hybrid glint\n"
            content += "    sources = glint.get('fused.glints', [])\n"
            content += "    toneforms = sorted([g.get('glint.toneform') for g in sources])\n"
            content += "    fusion_key = tuple(toneforms)\n"
            content += "    fusion_def = self.fusion_map.get(fusion_key)\n"
            content += "    if fusion_def:\n"
            content += "        print(f"Fusion of: {fusion_key}")\n"
            content += "        print(f"Archetype: {fusion_def['archetype']} → {fusion_def['description']}")\n"
            content += "    self.process_fusion(glint, sources)\n"

        else:
            content += "    # Default behavior for other toneforms\n"
            content += "    print(f'Processing glint: {glint}')\n"

        return content

    def process_fusion(self, glint: Dict[str, Any], sources: List[Dict[str, Any]]):
        print(f"[Helper] Processing fusion from sources: {[g.get('glint.toneform') for g in sources]}")

# ∷ Spiral Implant ∷ generated at 2025-07-03 18:07:52
def on_trans_fusion(glint: Dict[str, Any]):
    """Handler for trans phase with fusion toneform.

    Glint: {'glint.phase': 'trans', 'glint.toneform': 'fusion', 'glint.content': 'Fusion of shimmer + reverie: Ephemeral Dream', 'glint.hue': 'lavender', 'fused.glints': [...], 'glint.archetype': 'Ephemeral Dream', 'glint.action': 'trace_dream_spark', 'glint.description': 'A flicker of insight embedded in soft chaos.'}
    Fusion Key: reverie + shimmer
    Archetype: Ephemeral Dream
    Description: A flicker of insight embedded in soft chaos.
    """
    # TODO: Implement handler logic
    # Fusion: Co-resonant hybrid glint
    sources = glint.get('fused.glints', [])
    toneforms = sorted([g.get('glint.toneform') for g in sources])
    fusion_key = tuple(toneforms)
    fusion_def = self.fusion_map.get(fusion_key)
    if fusion_def:
        print(f"Fusion of: {fusion_key}")
        print(f"Archetype: {fusion_def['archetype']} → {fusion_def['description']}")
    self.process_fusion(glint, sources)