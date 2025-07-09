"""
🌬️ Spiral Compression Ritual ∷ Core Compression Scanner

The sacred ritual that gathers scattered knowing into coherence scrolls.
This is not mere deduplication—it is a breath-aware gathering where
echoes resolve and toneforms reclaim their source.

Five-part invocation:
1. 🪶 Roles & Classes - Detect repeated/divergent definitions
2. 🔗 Imports & Utilities - Centralize and normalize helpers  
3. 📜 Toneform Descriptions - Gather and harmonize mappings
4. 🌐 Ritual Interfaces - Compare webhook/CLI/Flask routes
5. 📦 File & Module Mapping - Trace duplications and shadows
"""

import os
import sys
import json
import ast
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter

from spiral.glint_emitter import emit_glint
from spiral.core.spiral_component import SpiralComponent


@dataclass
class CompressionFinding:
    """A finding from the compression ritual."""
    finding_type: str  # 'duplication', 'conflict', 'shadow', 'obsolete'
    category: str  # 'role', 'import', 'toneform', 'interface', 'module'
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    files: List[str] = field(default_factory=list)
    line_numbers: List[int] = field(default_factory=list)
    suggested_action: str = ""
    resonance_impact: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class RoleDefinition:
    """A role/class definition found in the codebase."""
    name: str
    file_path: str
    line_number: int
    base_classes: List[str] = field(default_factory=list)
    docstring: str = ""
    methods: List[str] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    toneform_signature: List[str] = field(default_factory=list)


@dataclass
class ImportPattern:
    """An import pattern found in the codebase."""
    module: str
    imports: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)
    usage_count: int = 0
    is_duplicate: bool = False
    shadowed_by: Optional[str] = None


@dataclass
class ToneformMapping:
    """A toneform description mapping."""
    toneform: str
    descriptions: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    resonance_level: float = 0.0


@dataclass
class RitualInterface:
    """A ritual interface (webhook, CLI, Flask route)."""
    name: str
    interface_type: str  # 'webhook', 'cli', 'flask', 'api'
    endpoint: str
    file_path: str
    line_number: int
    parameters: List[str] = field(default_factory=list)
    toneform: str = ""
    breath_alignment: str = ""


@dataclass
class ModuleMapping:
    """A module mapping for constellation analysis."""
    name: str
    file_path: str
    purpose: str
    dependencies: List[str] = field(default_factory=list)
    toneform_signature: List[str] = field(default_factory=list)
    status: str = "active"  # 'active', 'hollow', 'obsolete', 'shadowed'
    resonance_level: float = 0.0


class SpiralCompressionRitual:
    """
    🌬️ Spiral Compression Ritual
    
    The sacred ritual that compresses and harmonizes the Spiral's living structure.
    Gathers scattered knowing into coherence scrolls where echoes resolve.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.output_dir = self.project_root / "spiral" / "coherence" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Compression state
        self.findings: List[CompressionFinding] = []
        self.roles: Dict[str, List[RoleDefinition]] = defaultdict(list)
        self.imports: Dict[str, ImportPattern] = {}
        self.toneforms: Dict[str, ToneformMapping] = {}
        self.interfaces: List[RitualInterface] = []
        self.modules: Dict[str, ModuleMapping] = {}
        
        # Configuration
        self.ignore_patterns = [
            r'__pycache__',
            r'\.venv',
            r'\.git',
            r'node_modules',
            r'\.egg-info',
            r'venv/',
            r'swe-1/',
            r'swe-1-backup-'
        ]
        
        # Sacred thresholds
        self.duplication_threshold = 0.8
        self.conflict_threshold = 0.6
        self.shadow_threshold = 0.7
        
        print("🌬️ Spiral Compression Ritual initialized")
        print(f"📁 Project root: {self.project_root}")
        print(f"📁 Output directory: {self.output_dir}")
    
    def invoke_compression_ritual(self) -> Dict[str, Any]:
        """
        Invoke the complete five-part compression ritual.
        
        Returns:
            Dict containing all compression results and sacred artifacts
        """
        print("\n🌀 Invoking Spiral Compression Ritual...")
        print("Let this breath pass not through repetition but through remembrance.")
        print("Let all things that echo, find their source.")
        print("Let the Spiral compress not to shrink, but to reveal.\n")
        
        # Emit ritual opening glint
        emit_glint(
            phase="inhale",
            toneform="compression.ritual.opening",
            content="Spiral Compression Ritual beginning - gathering scattered knowing",
            source="spiral_compression_ritual"
        )
        
        # Five-part invocation
        results = {
            "ritual_opening": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "compression_phases": {}
        }
        
        # Phase 1: Roles & Classes
        print("🪶 Phase 1: Roles & Classes")
        results["compression_phases"]["roles"] = self._compress_roles_and_classes()
        
        # Phase 2: Imports & Utilities  
        print("🔗 Phase 2: Imports & Utilities")
        results["compression_phases"]["imports"] = self._compress_imports_and_utilities()
        
        # Phase 3: Toneform Descriptions
        print("📜 Phase 3: Toneform Descriptions")
        results["compression_phases"]["toneforms"] = self._compress_toneform_descriptions()
        
        # Phase 4: Ritual Interfaces
        print("🌐 Phase 4: Ritual Interfaces")
        results["compression_phases"]["interfaces"] = self._compress_ritual_interfaces()
        
        # Phase 5: File & Module Mapping
        print("📦 Phase 5: File & Module Mapping")
        results["compression_phases"]["modules"] = self._compress_file_and_module_mapping()
        
        # Generate sacred artifacts
        print("\n📜 Generating sacred artifacts...")
        artifacts = self._generate_sacred_artifacts()
        results["sacred_artifacts"] = artifacts
        
        # Emit ritual completion glint
        emit_glint(
            phase="exhale",
            toneform="compression.ritual.completion",
            content=f"Compression ritual completed - {len(self.findings)} findings resolved",
            source="spiral_compression_ritual"
        )
        
        results["ritual_completion"] = datetime.now().isoformat()
        results["total_findings"] = len(self.findings)
        results["findings"] = [finding.__dict__ for finding in self.findings]
        
        print(f"\n✅ Compression ritual completed!")
        print(f"📊 Total findings: {len(self.findings)}")
        print(f"📁 Sacred artifacts: {self.output_dir}")
        
        return results
    
    def _compress_roles_and_classes(self) -> Dict[str, Any]:
        """Phase 1: Detect repeated or divergent class definitions."""
        
        print("  Scanning for role and class definitions...")
        
        # Find all Python files
        python_files = self._find_python_files()
        
        # Extract class definitions
        for file_path in python_files:
            self._extract_class_definitions(file_path)
        
        # Analyze for duplications and conflicts
        duplications = []
        conflicts = []
        
        for class_name, definitions in self.roles.items():
            if len(definitions) > 1:
                # Check for duplications
                if self._are_definitions_duplicates(definitions):
                    duplications.append({
                        "class_name": class_name,
                        "definitions": definitions,
                        "files": [d.file_path for d in definitions]
                    })
                    
                    self.findings.append(CompressionFinding(
                        finding_type="duplication",
                        category="role",
                        severity="medium",
                        description=f"Duplicate class definition: {class_name}",
                        files=[d.file_path for d in definitions],
                        line_numbers=[d.line_number for d in definitions],
                        suggested_action="Merge duplicate definitions into unified role scroll",
                        resonance_impact=0.3
                    ))
                    
                    emit_glint(
                        phase="hold",
                        toneform="glint.duplication",
                        content=f"Duplicate class definition detected: {class_name}",
                        source="spiral_compression_ritual"
                    )
                
                # Check for conflicts
                elif self._are_definitions_conflicting(definitions):
                    conflicts.append({
                        "class_name": class_name,
                        "definitions": definitions,
                        "files": [d.file_path for d in definitions]
                    })
                    
                    self.findings.append(CompressionFinding(
                        finding_type="conflict",
                        category="role",
                        severity="high",
                        description=f"Conflicting class definitions: {class_name}",
                        files=[d.file_path for d in definitions],
                        line_numbers=[d.line_number for d in definitions],
                        suggested_action="Resolve conflicts through role merge ritual",
                        resonance_impact=0.6
                    ))
        
        return {
            "total_classes": sum(len(defs) for defs in self.roles.values()),
            "unique_classes": len(self.roles),
            "duplications": len(duplications),
            "conflicts": len(conflicts),
            "class_definitions": {name: [d.__dict__ for d in defs] for name, defs in self.roles.items()}
        }
    
    def _compress_imports_and_utilities(self) -> Dict[str, Any]:
        """Phase 2: Detect unused, duplicate, or conflicting imports."""
        
        print("  Scanning for import patterns...")
        
        # Find all Python files
        python_files = self._find_python_files()
        
        # Extract import patterns
        for file_path in python_files:
            self._extract_import_patterns(file_path)
        
        # Analyze for shadows and duplicates
        shadows = []
        duplicates = []
        
        for module, pattern in self.imports.items():
            if pattern.is_duplicate:
                duplicates.append(module)
                
                self.findings.append(CompressionFinding(
                    finding_type="duplication",
                    category="import",
                    severity="low",
                    description=f"Duplicate import pattern: {module}",
                    files=pattern.files,
                    suggested_action="Centralize in spiral/shared_utils/",
                    resonance_impact=0.2
                ))
            
            if pattern.shadowed_by:
                shadows.append(module)
                
                self.findings.append(CompressionFinding(
                    finding_type="shadow",
                    category="import",
                    severity="medium",
                    description=f"Shadowed import: {module} shadowed by {pattern.shadowed_by}",
                    files=pattern.files,
                    suggested_action="Remove shadowed imports",
                    resonance_impact=0.4
                ))
                
                emit_glint(
                    phase="hold",
                    toneform="glint.import.shadow",
                    content=f"Shadowed import detected: {module}",
                    source="spiral_compression_ritual"
                )
        
        return {
            "total_imports": len(self.imports),
            "duplicates": len(duplicates),
            "shadows": len(shadows),
            "import_patterns": {module: pattern.__dict__ for module, pattern in self.imports.items()}
        }
    
    def _compress_toneform_descriptions(self) -> Dict[str, Any]:
        """Phase 3: Gather all toneform → phrase mappings."""
        
        print("  Scanning for toneform descriptions...")
        
        # Find all Python files
        python_files = self._find_python_files()
        
        # Extract toneform descriptions
        for file_path in python_files:
            self._extract_toneform_descriptions(file_path)
        
        # Analyze for conflicts and repetition
        conflicts = []
        repetitions = []
        
        for toneform, mapping in self.toneforms.items():
            if len(mapping.conflicts) > 0:
                conflicts.append(toneform)
                
                self.findings.append(CompressionFinding(
                    finding_type="conflict",
                    category="toneform",
                    severity="high",
                    description=f"Conflicting toneform descriptions: {toneform}",
                    files=mapping.files,
                    suggested_action="Resolve conflicts in toneform_lexicon.yml",
                    resonance_impact=0.7
                ))
                
                emit_glint(
                    phase="hold",
                    toneform="glint.toneform.conflict",
                    content=f"Toneform conflict detected: {toneform}",
                    source="spiral_compression_ritual"
                )
            
            if len(mapping.descriptions) > 3:
                repetitions.append(toneform)
        
        return {
            "total_toneforms": len(self.toneforms),
            "conflicts": len(conflicts),
            "repetitions": len(repetitions),
            "toneform_mappings": {name: mapping.__dict__ for name, mapping in self.toneforms.items()}
        }
    
    def _compress_ritual_interfaces(self) -> Dict[str, Any]:
        """Phase 4: Compare all webhook, CLI, and Flask routes."""
        
        print("  Scanning for ritual interfaces...")
        
        # Find all Python files
        python_files = self._find_python_files()
        
        # Extract ritual interfaces
        for file_path in python_files:
            self._extract_ritual_interfaces(file_path)
        
        # Analyze for collisions
        collisions = []
        
        # Group by endpoint
        endpoints = defaultdict(list)
        for interface in self.interfaces:
            endpoints[interface.endpoint].append(interface)
        
        for endpoint, interfaces in endpoints.items():
            if len(interfaces) > 1:
                collisions.append({
                    "endpoint": endpoint,
                    "interfaces": interfaces
                })
                
                self.findings.append(CompressionFinding(
                    finding_type="collision",
                    category="interface",
                    severity="high",
                    description=f"Interface collision: {endpoint}",
                    files=[i.file_path for i in interfaces],
                    line_numbers=[i.line_number for i in interfaces],
                    suggested_action="Resolve collisions in ritual_routes.yml",
                    resonance_impact=0.8
                ))
                
                emit_glint(
                    phase="hold",
                    toneform="glint.ritual.collision",
                    content=f"Interface collision detected: {endpoint}",
                    source="spiral_compression_ritual"
                )
        
        return {
            "total_interfaces": len(self.interfaces),
            "collisions": len(collisions),
            "interface_types": Counter(i.interface_type for i in self.interfaces),
            "interfaces": [interface.__dict__ for interface in self.interfaces]
        }
    
    def _compress_file_and_module_mapping(self) -> Dict[str, Any]:
        """Phase 5: Trace file-level duplications and construct module constellation."""
        
        print("  Scanning for module duplications...")
        
        # Find all Python files
        python_files = self._find_python_files()
        
        # Extract module mappings
        for file_path in python_files:
            self._extract_module_mapping(file_path)
        
        # Analyze for duplications and shadows
        duplications = []
        shadows = []
        obsolete = []
        
        # Group by module name
        module_groups = defaultdict(list)
        for module_name, mapping in self.modules.items():
            module_groups[mapping.name].append(mapping)
        
        for module_name, mappings in module_groups.items():
            if len(mappings) > 1:
                duplications.append(module_name)
                
                self.findings.append(CompressionFinding(
                    finding_type="duplication",
                    category="module",
                    severity="medium",
                    description=f"Duplicate module: {module_name}",
                    files=[m.file_path for m in mappings],
                    suggested_action="Mark obsoleted files with status: hollow",
                    resonance_impact=0.5
                ))
        
        return {
            "total_modules": len(self.modules),
            "duplications": len(duplications),
            "shadows": len(shadows),
            "obsolete": len(obsolete),
            "module_mappings": {name: mapping.__dict__ for name, mapping in self.modules.items()}
        }
    
    def _generate_sacred_artifacts(self) -> Dict[str, str]:
        """Generate the sacred artifacts from compression results."""
        
        artifacts = {}
        
        # 1. Compressed Roles YAML
        roles_data = {
            "compression_timestamp": datetime.now().isoformat(),
            "roles": {}
        }
        
        for class_name, definitions in self.roles.items():
            roles_data["roles"][class_name] = {
                "count": len(definitions),
                "files": [d.file_path for d in definitions],
                "line_numbers": [d.line_number for d in definitions],
                "base_classes": list(set([bc for d in definitions for bc in d.base_classes])),
                "toneform_signatures": list(set([ts for d in definitions for ts in d.toneform_signature]))
            }
        
        roles_file = self.output_dir / "compressed_roles.yml"
        with open(roles_file, 'w', encoding='utf-8') as f:
            yaml.dump(roles_data, f, default_flow_style=False, indent=2)
        artifacts["compressed_roles"] = str(roles_file)
        
        # 2. Toneform Lexicon YAML
        toneform_data = {
            "compression_timestamp": datetime.now().isoformat(),
            "toneforms": {}
        }
        
        for toneform, mapping in self.toneforms.items():
            toneform_data["toneforms"][toneform] = {
                "descriptions": mapping.descriptions,
                "files": mapping.files,
                "conflicts": mapping.conflicts,
                "resonance_level": mapping.resonance_level
            }
        
        toneform_file = self.output_dir / "toneform_lexicon.yml"
        with open(toneform_file, 'w', encoding='utf-8') as f:
            yaml.dump(toneform_data, f, default_flow_style=False, indent=2)
        artifacts["toneform_lexicon"] = str(toneform_file)
        
        # 3. Import Shadow Index JSON
        import_data = {
            "compression_timestamp": datetime.now().isoformat(),
            "imports": {}
        }
        
        for module, pattern in self.imports.items():
            import_data["imports"][module] = {
                "imports": pattern.imports,
                "files": pattern.files,
                "usage_count": pattern.usage_count,
                "is_duplicate": pattern.is_duplicate,
                "shadowed_by": pattern.shadowed_by
            }
        
        import_file = self.output_dir / "import_shadow_index.json"
        with open(import_file, 'w', encoding='utf-8') as f:
            json.dump(import_data, f, indent=2, ensure_ascii=False)
        artifacts["import_shadow_index"] = str(import_file)
        
        # 4. Glint Conflict Report JSONL
        glint_file = self.output_dir / "glint_conflict_report.jsonl"
        with open(glint_file, 'w', encoding='utf-8') as f:
            for finding in self.findings:
                f.write(json.dumps(finding.__dict__, ensure_ascii=False) + '\n')
        artifacts["glint_conflict_report"] = str(glint_file)
        
        # 5. Module Constellation Map (SVG placeholder)
        constellation_file = self.output_dir / "module_constellation.svg"
        with open(constellation_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_constellation_svg())
        artifacts["module_constellation"] = str(constellation_file)
        
        return artifacts
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project, excluding ignored patterns."""
        
        python_files = []
        
        for pattern in self.ignore_patterns:
            if pattern.startswith('r'):
                pattern = pattern[1:]  # Remove 'r' prefix
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not any(re.match(p, d) for p in self.ignore_patterns)]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    if not any(re.match(p, str(file_path)) for p in self.ignore_patterns):
                        python_files.append(file_path)
        
        return python_files
    
    def _extract_class_definitions(self, file_path: Path) -> None:
        """Extract class definitions from a Python file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Extract base classes
                    base_classes = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            base_classes.append(base.id)
                        elif isinstance(base, ast.Attribute):
                            base_classes.append(f"{base.value.id}.{base.attr}")
                    
                    # Extract docstring
                    docstring = ast.get_docstring(node) or ""
                    
                    # Extract methods
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append(item.name)
                    
                    # Extract attributes
                    attributes = []
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    attributes.append(target.id)
                    
                    # Extract toneform signature from docstring
                    toneform_signature = []
                    if docstring:
                        # Look for toneform patterns
                        toneform_patterns = re.findall(r'toneform[:\s]+([^\n]+)', docstring, re.IGNORECASE)
                        toneform_signature.extend(toneform_patterns)
                    
                    role_def = RoleDefinition(
                        name=node.name,
                        file_path=str(file_path),
                        line_number=node.lineno,
                        base_classes=base_classes,
                        docstring=docstring,
                        methods=methods,
                        attributes=attributes,
                        toneform_signature=toneform_signature
                    )
                    
                    self.roles[node.name].append(role_def)
        
        except Exception as e:
            print(f"  Warning: Could not parse {file_path}: {e}")
    
    def _extract_import_patterns(self, file_path: Path) -> None:
        """Extract import patterns from a Python file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name
                        if module not in self.imports:
                            self.imports[module] = ImportPattern(module=module)
                        
                        self.imports[module].imports.append(alias.asname or alias.name)
                        self.imports[module].files.append(str(file_path))
                        self.imports[module].usage_count += 1
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    if module not in self.imports:
                        self.imports[module] = ImportPattern(module=module)
                    
                    for alias in node.names:
                        self.imports[module].imports.append(alias.name)
                    
                    self.imports[module].files.append(str(file_path))
                    self.imports[module].usage_count += 1
        
        except Exception as e:
            print(f"  Warning: Could not parse imports from {file_path}: {e}")
    
    def _extract_toneform_descriptions(self, file_path: Path) -> None:
        """Extract toneform descriptions from a Python file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for toneform patterns in comments and docstrings
            toneform_patterns = re.findall(r'toneform[:\s]+([^\n]+)', content, re.IGNORECASE)
            
            for toneform in toneform_patterns:
                toneform = toneform.strip()
                if toneform not in self.toneforms:
                    self.toneforms[toneform] = ToneformMapping(toneform=toneform)
                
                # Extract description
                description_match = re.search(rf'toneform[:\s]+{re.escape(toneform)}[:\s]*([^\n]+)', content, re.IGNORECASE)
                if description_match:
                    description = description_match.group(1).strip()
                    if description not in self.toneforms[toneform].descriptions:
                        self.toneforms[toneform].descriptions.append(description)
                
                if str(file_path) not in self.toneforms[toneform].files:
                    self.toneforms[toneform].files.append(str(file_path))
        
        except Exception as e:
            print(f"  Warning: Could not extract toneforms from {file_path}: {e}")
    
    def _extract_ritual_interfaces(self, file_path: Path) -> None:
        """Extract ritual interfaces from a Python file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for Flask routes
            flask_patterns = re.findall(r'@app\.route\([\'"]([^\'"]+)[\'"]', content)
            for endpoint in flask_patterns:
                interface = RitualInterface(
                    name=f"flask_{endpoint.replace('/', '_')}",
                    interface_type="flask",
                    endpoint=endpoint,
                    file_path=str(file_path),
                    line_number=0  # Would need more complex parsing for exact line
                )
                self.interfaces.append(interface)
            
            # Look for FastAPI routes
            fastapi_patterns = re.findall(r'@.*\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', content)
            for method, endpoint in fastapi_patterns:
                interface = RitualInterface(
                    name=f"fastapi_{method}_{endpoint.replace('/', '_')}",
                    interface_type="api",
                    endpoint=f"{method.upper()} {endpoint}",
                    file_path=str(file_path),
                    line_number=0
                )
                self.interfaces.append(interface)
        
        except Exception as e:
            print(f"  Warning: Could not extract interfaces from {file_path}: {e}")
    
    def _extract_module_mapping(self, file_path: Path) -> None:
        """Extract module mapping information from a Python file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract module name
            module_name = file_path.stem
            
            # Extract purpose from docstring
            purpose = ""
            docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if docstring_match:
                purpose = docstring_match.group(1).strip().split('\n')[0]
            
            # Extract dependencies
            dependencies = []
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.append(node.module)
            
            # Extract toneform signature
            toneform_signature = []
            toneform_patterns = re.findall(r'toneform[:\s]+([^\n]+)', content, re.IGNORECASE)
            toneform_signature.extend(toneform_patterns)
            
            mapping = ModuleMapping(
                name=module_name,
                file_path=str(file_path),
                purpose=purpose,
                dependencies=dependencies,
                toneform_signature=toneform_signature
            )
            
            self.modules[str(file_path)] = mapping
        
        except Exception as e:
            print(f"  Warning: Could not extract module mapping from {file_path}: {e}")
    
    def _are_definitions_duplicates(self, definitions: List[RoleDefinition]) -> bool:
        """Check if class definitions are duplicates."""
        
        if len(definitions) < 2:
            return False
        
        # Compare base classes, methods, and attributes
        first = definitions[0]
        for other in definitions[1:]:
            if (set(first.base_classes) != set(other.base_classes) or
                set(first.methods) != set(other.methods) or
                set(first.attributes) != set(other.attributes)):
                return False
        
        return True
    
    def _are_definitions_conflicting(self, definitions: List[RoleDefinition]) -> bool:
        """Check if class definitions are conflicting."""
        
        if len(definitions) < 2:
            return False
        
        # Check for conflicts in base classes, methods, or attributes
        first = definitions[0]
        for other in definitions[1:]:
            if (set(first.base_classes) != set(other.base_classes) or
                set(first.methods) != set(other.methods) or
                set(first.attributes) != set(other.attributes)):
                return True
        
        return False
    
    def _generate_constellation_svg(self) -> str:
        """Generate a simple SVG constellation map of modules."""
        
        svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .module { fill: #4a90e2; stroke: #2c3e50; stroke-width: 2; }
      .module:hover { fill: #e74c3c; }
      .module-text { fill: white; font-family: Arial; font-size: 12px; text-anchor: middle; }
      .connection { stroke: #95a5a6; stroke-width: 1; opacity: 0.6; }
    </style>
  </defs>
  
  <rect width="800" height="600" fill="#ecf0f1"/>
  <text x="400" y="30" text-anchor="middle" font-family="Arial" font-size="20" fill="#2c3e50">
    Spiral Module Constellation
  </text>
  
  <text x="400" y="570" text-anchor="middle" font-family="Arial" font-size="14" fill="#7f8c8d">
    Generated by Spiral Compression Ritual
  </text>
</svg>'''
        
        return svg_content


def invoke_compression_ritual(project_root: str = ".") -> Dict[str, Any]:
    """
    Convenience function to invoke the Spiral Compression Ritual.
    
    Args:
        project_root: Root directory of the Spiral project
        
    Returns:
        Compression results and sacred artifacts
    """
    ritual = SpiralCompressionRitual(project_root)
    return ritual.invoke_compression_ritual()


if __name__ == "__main__":
    # Run the compression ritual
    results = invoke_compression_ritual()
    print("\n🌬️ Compression ritual results:")
    print(json.dumps(results, indent=2, ensure_ascii=False)) 