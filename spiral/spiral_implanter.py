# File: C:\spiral\spiral\spiral_implanter.py

import os
import datetime
import re
from typing import Dict, Any, Set, List, Tuple
import yaml

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
        self.fusion_map = self._load_fusion_map()
        self.phase_fusion_map_path = os.path.join(spiral_root, "phase_fusion_map.yml")
        self.phase_fusion_map: Dict[Tuple[Tuple[str, str], ...], Dict[str, Any]] = {}
        self._load_phase_fusion_map()
        self._ensure_handler_files()
        self.implanted_handlers: Set[str] = set()
        self._load_existing_handlers()

    def _load_fusion_map(self) -> Dict[str, Any]:
        if not os.path.exists(self.fusion_map_path):
            print("No fusion_map.yml found.")
            return {}
        with open(self.fusion_map_path, 'r') as f:
            return yaml.safe_load(f)

    def load_fusion_map(self) -> Dict[str, Dict[str, str]]:
        fusion_map_path = os.path.join(self.spiral_root, 'fusion_map.yml')
        with open(fusion_map_path, 'r') as f:
            return yaml.safe_load(f)

    def generate_fusion_handler(self, toneform1: str, toneform2: str) -> str:
        fusion_key = f"{toneform1} + {toneform2}"
        fusion_data = self.fusion_map.get(fusion_key, {})

        archetype = fusion_data.get('archetype', 'Unknown Archetype')
        action = fusion_data.get('action', 'handle_fusion')
        description = fusion_data.get('description', 'A fusion of toneforms.')

        handler_lines = [
            f"def {action}(glint1: Dict[str, Any], glint2: Dict[str, Any]) -> Dict[str, Any]:",
            f"    \"\"\"",
            f"    Handles fusion of {toneform1} and {toneform2} toneforms.",
            f"",
            f"    Archetype: {archetype}",
            f"    Description: {description}",
            f"",
            f"    Args:",
            f"        glint1 (Dict[str, Any]): The first glint in the fusion.",
            f"        glint2 (Dict[str, Any]): The second glint in the fusion.",
            f"",
            f"    Returns:",
            f"        Dict[str, Any]: The resulting fused glint.",
            f"    \"\"\"",
            f"    fusion_key = ((glint1.get('glint.phase'), glint1.get('glint.toneform')),"
            f"                  (glint2.get('glint.phase'), glint2.get('glint.toneform')))",
            f"    fusion_def = self.phase_fusion_map.get(tuple(sorted(fusion_key))) or self.fusion_map.get('{toneform1} + {toneform2}', {{}})",
            f"    if fusion_def:",
            f"        print(f\"Phase Fusion of: {{fusion_key}}\")",
            f"        print(f\"Archetype: {{fusion_def.get('archetype')}} -> {{fusion_def.get('description')}}\")",
            f"        fused_glint = {{",
            f"            'phase': 'trans',",
            f"            'toneform': f\"{{glint1.get('glint.toneform', '')}}.{{glint2.get('glint.toneform', '')}}\",",
            f"            'content': f\"Fusion of {{glint1.get('glint.content', '')}} and {{glint2.get('glint.content', '')}}\",",
            f"            'hue': 'gold',",
            f"            'archetype': fusion_def.get('archetype', 'Unknown'),",
            f"            'action': fusion_def.get('action', '{action}')",
            f"        }}",
            f"        return fused_glint",
            f"    else:",
            f"        print(\"Warning: Fusion definition not found for key\", fusion_key)",
            f"        return {{}}"
        ]

        return "\n".join(handler_lines)

    def implant_fusion_handler(self, toneform1: str, toneform2: str):
        handler_code = self.generate_fusion_handler(toneform1, toneform2)
        handler_path = os.path.join(self.spiral_root, 'fusion_handlers.py')

        if validate_handler_code(handler_code):
            with open(handler_path, 'a') as f:
                f.write(f"\n\n# Fusion handler for {toneform1} + {toneform2}\n")
                f.write(handler_code)

            print(f"Implanted fusion handler for {toneform1} + {toneform2}")
        else:
            print("⚠️ Skipping implantation: handler code is invalid.")

    def _ensure_handler_files(self):
        for path in self.handler_paths.values():
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write("# Handler file created by SpiralImplanter\n\n")

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

    def _implant_handler(self, handler_type: str, function_name: str, glint: Dict[str, Any], debug: bool = False):
        handler_path = self.handler_paths[handler_type]
        phase = glint.get('glint.phase', '').lower()
        toneform = glint.get('glint.toneform', '').lower()

        handler_code = (
            f"\n\n{self._generate_spiral_header()}"
            f"def {function_name}(glint: Dict[str, Any]):\n"
            f'    """{self._generate_docstring(glint)}"""\n'
            f"{self._generate_handler_content(phase, toneform, glint)}"
        )

        if validate_handler_code(handler_code):
            with open(handler_path, 'a') as f:
                f.write(handler_code)
            print(f"Implanted handler '{function_name}' in {handler_path}")
        else:
            print(f"⚠️ Skipping implantation: handler code for '{function_name}' is invalid.")
            if debug:
                print("\n🔍 Debug Output — Invalid Handler Code:\n")
                print(handler_code)

    def _generate_spiral_header(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"# ∷ Spiral Implant ∷ generated at {timestamp}\n"

    def _generate_docstring(self, glint: Dict[str, Any]) -> str:
        phase = glint.get('glint.phase', 'unknown')
        toneform = glint.get('glint.toneform', 'unknown')
        docstring_lines = [
            f"Handler for {phase} phase with {toneform} toneform.",
            "",
            f"Glint: {glint}",
        ]

        if toneform == 'fusion':
            fused_glints_info = glint.get('fused.glints', [])
            source_toneforms_tuple = tuple(sorted(
                (g.get('glint.phase', 'unknown'), g.get('glint.toneform', 'unknown'))
                for g in fused_glints_info
            ))
            fusion_key_str = ' + '.join(f"{phase}.{toneform}" for phase, toneform in source_toneforms_tuple)
            fusion_def = self.phase_fusion_map.get(source_toneforms_tuple) or self.fusion_map.get(tuple(t for _, t in source_toneforms_tuple))
            docstring_lines.append(f"Fusion Key: {fusion_key_str}")
            if fusion_def:
                docstring_lines.append(f"Archetype: {fusion_def['archetype']}")
                docstring_lines.append(f"Description: {fusion_def['description']}")

        return "\n    ".join(docstring_lines)

    def _generate_handler_content(self, phase: str, toneform: str, glint: Dict[str, Any]) -> str:
        content_lines = [
            "    # TODO: Implement handler logic",
        ]

        if toneform == 'fusion':
            content_lines.extend([
                "    # Fusion: Phase-sensitive co-resonant hybrid glint",
                "    sources = glint.get('fused.glints', [])",
                "    toneforms = sorted((g.get('glint.phase'), g.get('glint.toneform')) for g in sources)",
                "    fusion_key = tuple(toneforms)",
                "    fusion_def = self.phase_fusion_map.get(fusion_key) or self.fusion_map.get(tuple(t for _, t in fusion_key))",
                "    if fusion_def:",
                "        print(f\"Phase Fusion of: {fusion_key}\")",
                "        print(f\"Archetype: {fusion_def['archetype']} -> {fusion_def['description']}\")",
                "        fused_glint = {",
                "            'phase': 'trans',",
                "            'toneform': f\"{glint.get('glint.toneform', 'unknown')}.{sources[1].get('glint.toneform', 'unknown')}\",",
                "            'content': f\"Fusion of {sources[0].get('glint.content', '')} and {sources[1].get('glint.content', '')}\",",
                "            'hue': 'gold',",
                "            'archetype': fusion_def.get('archetype', 'Unknown'),",
                "            'action': fusion_def.get('action', 'handle_fusion')",
                "        }",
                "        return fused_glint",
                "    else:",
                "        print(\"Warning: Fusion definition not found for key\", fusion_key)",
                "        return None"
            ])

        content_lines.append("    # Add your custom logic here")
        content_lines.append("    pass")

        return "\n".join(content_lines)

    def process_flutter(self, glint: Dict[str, Any], flutter_sequence: List[Any]):
        print(f"[Helper] Processing flutter: {flutter_sequence}")

    def perform_invocation(self, glint: Dict[str, Any], invocation_target: str):
        print(f"[Helper] Performing invocation: {invocation_target}")

    def enter_reverie(self, glint: Dict[str, Any], dream_seed: str):
        print(f"[Helper] Entering reverie with seed: {dream_seed}")

    def process_fusion(self, glint: Dict[str, Any], sources: List[Dict[str, Any]]):
        print(f"[Helper] Processing fusion from sources: {[g.get('glint.toneform') for g in sources]}")

    def _load_phase_fusion_map(self):
        if os.path.exists(self.phase_fusion_map_path):
            try:
                with open(self.phase_fusion_map_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'phase_fusions' in data:
                        for fusion_def in data['phase_fusions']:
                            sorted_toneforms = tuple(sorted(tuple(t) for t in fusion_def['toneforms']))
                            self.phase_fusion_map[sorted_toneforms] = {
                                "archetype": fusion_def.get('archetype', 'Unknown Phase Fusion'),
                                "action": fusion_def.get('action', 'process_phase_fused_glint'),
                                "description": fusion_def.get('description', 'A phase-sensitive co-resonance.'),
                                "hue": fusion_def.get('hue', 'iridescent')
                            }
                        print(f"Loaded {len(self.phase_fusion_map)} phase fusion definitions from {self.phase_fusion_map_path}")
                    else:
                        print(f"Warning: 'phase_fusions' key not found or empty in {self.phase_fusion_map_path}")
            except Exception as e:
                print(f"Error loading phase fusion map from {self.phase_fusion_map_path}: {e}")
        else:
            print(f"Warning: Phase fusion map file not found at {self.phase_fusion_map_path}. Phase-specific fusion handlers will use default descriptions.")

    def process_phase_fusion(self, glint: Dict[str, Any], sources: List[Dict[str, Any]]):
        print(f"[Helper] Processing phase-sensitive fusion from sources: {[(g.get('glint.phase'), g.get('glint.toneform')) for g in sources]}")
        # Implement phase-specific fusion logic here

def validate_handler_code(code: str) -> bool:
    try:
        compile(code, '<spiral_handler>', 'exec')
        return True
    except SyntaxError as e:
        print(f"⚠️ Handler validation failed: {e}")
        return False
