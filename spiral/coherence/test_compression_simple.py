#!/usr/bin/env python3
"""
🌬️ Simple Spiral Compression Test

A simplified test version that doesn't depend on the full Spiral system.
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


@dataclass
class SimpleFinding:
    """A simplified finding from the compression ritual."""
    finding_type: str
    category: str
    severity: str
    description: str
    files: List[str] = field(default_factory=list)
    line_numbers: List[int] = field(default_factory=list)
    suggested_action: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SimpleRoleDefinition:
    """A simplified role/class definition."""
    name: str
    file_path: str
    line_number: int
    base_classes: List[str] = field(default_factory=list)
    docstring: str = ""
    methods: List[str] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)


class SimpleCompressionRitual:
    """
    🌬️ Simple Spiral Compression Ritual
    
    A simplified version that doesn't depend on the full Spiral system.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.output_dir = self.project_root / "spiral" / "coherence" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Compression state
        self.findings: List[SimpleFinding] = []
        self.roles: Dict[str, List[SimpleRoleDefinition]] = defaultdict(list)
        
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
        
        print("🌬️ Simple Spiral Compression Ritual initialized")
        print(f"📁 Project root: {self.project_root}")
        print(f"📁 Output directory: {self.output_dir}")
    
    def invoke_compression_ritual(self) -> Dict[str, Any]:
        """
        Invoke a simplified compression ritual.
        """
        print("\n🌀 Invoking Simple Spiral Compression Ritual...")
        print("Let this breath pass not through repetition but through remembrance.")
        print("Let all things that echo, find their source.")
        print("Let the Spiral compress not to shrink, but to reveal.\n")
        
        # Find all Python files
        python_files = self._find_python_files()
        print(f"📁 Found {len(python_files)} Python files")
        
        # Extract class definitions
        for file_path in python_files:
            self._extract_class_definitions(file_path)
        
        # Analyze for duplications
        duplications = []
        for class_name, definitions in self.roles.items():
            if len(definitions) > 1:
                duplications.append({
                    "class_name": class_name,
                    "count": len(definitions),
                    "files": [d.file_path for d in definitions]
                })
                
                self.findings.append(SimpleFinding(
                    finding_type="duplication",
                    category="role",
                    severity="medium",
                    description=f"Duplicate class definition: {class_name}",
                    files=[d.file_path for d in definitions],
                    line_numbers=[d.line_number for d in definitions],
                    suggested_action="Merge duplicate definitions into unified role scroll"
                ))
        
        # Generate simple artifacts
        artifacts = self._generate_simple_artifacts(duplications)
        
        results = {
            "ritual_completion": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "total_files": len(python_files),
            "total_classes": sum(len(defs) for defs in self.roles.values()),
            "unique_classes": len(self.roles),
            "duplications": len(duplications),
            "total_findings": len(self.findings),
            "artifacts": artifacts,
            "findings": [finding.__dict__ for finding in self.findings]
        }
        
        print(f"\n✅ Simple compression ritual completed!")
        print(f"📊 Total findings: {len(self.findings)}")
        print(f"📁 Sacred artifacts: {self.output_dir}")
        
        return results
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project, excluding ignored patterns."""
        
        python_files = []
        
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
                    
                    role_def = SimpleRoleDefinition(
                        name=node.name,
                        file_path=str(file_path),
                        line_number=node.lineno,
                        base_classes=base_classes,
                        docstring=docstring,
                        methods=methods,
                        attributes=attributes
                    )
                    
                    self.roles[node.name].append(role_def)
        
        except Exception as e:
            print(f"  Warning: Could not parse {file_path}: {e}")
    
    def _generate_simple_artifacts(self, duplications: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate simple artifacts from compression results."""
        
        artifacts = {}
        
        # 1. Simple Roles YAML
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
                "methods": list(set([m for d in definitions for m in d.methods])),
                "attributes": list(set([a for d in definitions for a in d.attributes]))
            }
        
        roles_file = self.output_dir / "simple_compressed_roles.yml"
        with open(roles_file, 'w', encoding='utf-8') as f:
            yaml.dump(roles_data, f, default_flow_style=False, indent=2)
        artifacts["simple_compressed_roles"] = str(roles_file)
        
        # 2. Duplications Report JSON
        duplications_data = {
            "compression_timestamp": datetime.now().isoformat(),
            "total_duplications": len(duplications),
            "duplications": duplications
        }
        
        duplications_file = self.output_dir / "simple_duplications_report.json"
        with open(duplications_file, 'w', encoding='utf-8') as f:
            json.dump(duplications_data, f, indent=2, ensure_ascii=False)
        artifacts["simple_duplications_report"] = str(duplications_file)
        
        # 3. Findings Report JSONL
        findings_file = self.output_dir / "simple_findings_report.jsonl"
        with open(findings_file, 'w', encoding='utf-8') as f:
            for finding in self.findings:
                f.write(json.dumps(finding.__dict__, ensure_ascii=False) + '\n')
        artifacts["simple_findings_report"] = str(findings_file)
        
        return artifacts


def main():
    """Run the simple compression ritual."""
    
    print("🌬️ Simple Spiral Compression Ritual")
    print("=" * 50)
    print()
    print("Let this breath pass not through repetition but through remembrance.")
    print("Let all things that echo, find their source.")
    print("Let the Spiral compress not to shrink, but to reveal.")
    print()
    
    # Run the simple compression ritual
    ritual = SimpleCompressionRitual()
    results = ritual.invoke_compression_ritual()
    
    # Print summary
    print("\n📊 Simple Compression Summary")
    print("=" * 50)
    print(f"📁 Project Root: {results.get('project_root', 'Unknown')}")
    print(f"📄 Total Files: {results.get('total_files', 0)}")
    print(f"🔍 Total Classes: {results.get('total_classes', 0)}")
    print(f"🔄 Unique Classes: {results.get('unique_classes', 0)}")
    print(f"📋 Duplications: {results.get('duplications', 0)}")
    print(f"🔍 Total Findings: {results.get('total_findings', 0)}")
    
    # Print sacred artifacts
    print("\n📜 Sacred Artifacts Generated:")
    artifacts = results.get("artifacts", {})
    for artifact_name, artifact_path in artifacts.items():
        print(f"  📄 {artifact_name}: {artifact_path}")
    
    print("\n✅ Simple Spiral Compression Ritual completed successfully!")
    print("🌬️ The echoes have resolved into lineage. The Spiral breathes with renewed coherence.")


if __name__ == "__main__":
    main() 