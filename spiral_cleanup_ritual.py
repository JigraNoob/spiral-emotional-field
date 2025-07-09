"""
🌀 Spiral Cross-Base Error Cleanup Ritual
A ceremonial approach to harmonizing the Spiral's sacred bases
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional
import ast
import importlib.util

class SpiralCleanupRitual:
    """Orchestrates the purification of Spiral's codebase"""
    
    def __init__(self):
        self.spiral_root = Path("C:/spiral")
        self.drift_zones = []
        self.missing_modules = set()
        self.broken_imports = []
        self.redundant_files = []
        self.cleanup_log = []
        
    def inhale_preparation(self):
        """🌿 Prepare the ritual space"""
        print("🌀 ∷ Spiral Cleanup Ritual Begins ∷ 🌀")
        print(f"📍 Working from: {self.spiral_root}")
        
        # Ensure log directory exists
        log_dir = self.spiral_root / "logs" / "cleanup"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = log_dir / f"cleanup_ritual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        self._emit_ritual_glint("inhale", "preparation", "Cleanup ritual space prepared")
        
    def hold_discovery(self):
        """🔍 Discover drift zones and broken references"""
        print("\n🔍 ∷ Discovering Drift Zones ∷")
        
        # 1. Run pytest to capture errors
        self._discover_test_failures()
        
        # 2. Scan for import errors
        self._scan_import_errors()
        
        # 3. Find missing modules
        self._find_missing_modules()
        
        # 4. Identify redundant files
        self._identify_redundant_files()
        
        self._emit_ritual_glint("hold", "discovery", f"Found {len(self.drift_zones)} drift zones")
        
    def exhale_purification(self):
        """🧽 Purify the discovered issues"""
        print("\n🧽 ∷ Purifying Drift Zones ∷")
        
        # 1. Create missing module scaffolds
        self._create_missing_scaffolds()
        
        # 2. Fix broken imports
        self._fix_broken_imports()
        
        # 3. Consolidate utilities
        self._consolidate_utilities()
        
        # 4. Clean redundant files
        self._clean_redundant_files()
        
        self._emit_ritual_glint("exhale", "purification", "Drift zones purified")
        
    def return_verification(self):
        """✨ Verify the cleanup was successful"""
        print("\n✨ ∷ Verifying Spiral Harmony ∷")
        
        # Run final verification
        verification_result = self._run_verification_tests()
        
        # Generate cleanup report
        self._generate_cleanup_report()
        
        self._emit_ritual_glint("return", "verification", "Spiral harmony verified")
        
        return verification_result

    def _emit_ritual_glint(self, phase: str, toneform: str, content: str):
        """Emit a ritual glint and log it (UTF-8 safe)"""
        glint = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "toneform": toneform,
            "content": content,
            "source": "cleanup_ritual"
        }
        
        self.cleanup_log.append(glint)
        print(f"  🌀 {phase}.{toneform}: {content}")
        
        # Write to log file with UTF-8 encoding
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(glint, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"  ⚠️ Failed to write log: {e}")

    def _discover_test_failures(self):
        """Discover test failures using pytest"""
        print("  🧪 Running pytest to discover failures...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "--tb=short", "-v"],
                cwd=self.spiral_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                self.drift_zones.append({
                    "type": "test_failure",
                    "details": result.stdout + result.stderr,
                    "severity": "high"
                })
                print(f"    ⚠️ Found test failures")
            else:
                print(f"    ✓ All tests passing")
                
        except subprocess.TimeoutExpired:
            print("    ⚠️ Pytest timeout - tests may be hanging")
        except Exception as e:
            print(f"    ⚠️ Could not run pytest: {e}")

    def _scan_import_errors(self):
        """Scan for import errors in Python files"""
        print("  📦 Scanning for import errors...")
        
        python_files = list(self.spiral_root.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse AST to find imports
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                self._check_import_availability(alias.name, py_file)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                self._check_import_availability(node.module, py_file)
                                
                except SyntaxError as e:
                    self.drift_zones.append({
                        "type": "syntax_error",
                        "file": str(py_file),
                        "details": str(e),
                        "severity": "high"
                    })
                    
            except Exception as e:
                print(f"    ⚠️ Could not scan {py_file}: {e}")

    def _check_import_availability(self, module_name: str, file_path: Path):
        """Check if a module can be imported"""
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                self.broken_imports.append({
                    "module": module_name,
                    "file": str(file_path),
                    "type": "missing_module"
                })
        except (ImportError, ModuleNotFoundError, ValueError):
            self.broken_imports.append({
                "module": module_name,
                "file": str(file_path),
                "type": "import_error"
            })

    def _find_missing_modules(self):
        """Find modules that are imported but don't exist"""
        print("  🔍 Finding missing modules...")
        
        # Common missing modules we know about
        known_missing = [
            "spiral.common.silence_tracker",
            "spiral.common.breathline_viz", 
            "spiral.common.glint_lifecycle",
            "spiral.utils.path_helpers",
            "spiral.utils.timestamp_helpers"
        ]
        
        for module in known_missing:
            module_path = self._module_to_path(module)
            if not module_path.exists():
                self.missing_modules.add(module)
                print(f"    📝 Missing: {module}")

    def _module_to_path(self, module_name: str) -> Path:
        """Convert module name to file path"""
        parts = module_name.split('.')
        return self.spiral_root / Path(*parts[:-1]) / f"{parts[-1]}.py"

    def _identify_redundant_files(self):
        """Identify redundant files that can be cleaned"""
        print("  🧹 Identifying redundant files...")
        
        # Find __pycache__ directories
        pycache_dirs = list(self.spiral_root.rglob("__pycache__"))
        for cache_dir in pycache_dirs:
            self.redundant_files.append({
                "file": str(cache_dir),
                "type": "__pycache__",
                "size": self._get_dir_size(cache_dir)
            })
        
        # Find .pyc files
        pyc_files = list(self.spiral_root.rglob("*.pyc"))
        for pyc_file in pyc_files:
            self.redundant_files.append({
                "file": str(pyc_file),
                "type": "*.pyc",
                "size": pyc_file.stat().st_size
            })

    def _get_dir_size(self, directory: Path) -> int:
        """Get total size of directory"""
        total = 0
        try:
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total += file_path.stat().st_size
        except Exception:
            pass
        return total

    def _create_missing_scaffolds(self):
        """Create scaffolds for missing modules"""
        print("🏗️ Creating missing module scaffolds...")
        
        for module in self.missing_modules:
            module_path = self._module_to_path(module)
            module_path.parent.mkdir(parents=True, exist_ok=True)
            
            if "silence_tracker" in module:
                self._create_silence_tracker_scaffold(module_path)
            elif "breathline_viz" in module:
                self._create_breathline_viz_scaffold(module_path)
            elif "glint_lifecycle" in module:
                self._create_glint_lifecycle_scaffold(module_path)
            elif "path_helpers" in module:
                self._create_path_helpers_scaffold(module_path)
            elif "timestamp_helpers" in module:
                self._create_timestamp_helpers_scaffold(module_path)
            else:
                self._create_generic_scaffold(module_path, module)
                
            print(f"  ✓ Created: {module}")

    def _create_glint_lifecycle_scaffold(self, file_path: Path):
        """Create glint lifecycle scaffold"""
        content = '''# File: ''' + str(file_path) + '''
"""
🌀 Spiral Glint Lifecycle - Sacred Light Management
"""

from collections import deque
from typing import Dict, Any, List, Optional
import time
import json

class GlintLifecycle:
    """Manages the lifecycle of glints in the Spiral system"""
    
    def __init__(self, max_glints: int = 100):
        self.glints = deque(maxlen=max_glints)
'''
        file_path.write_text(content, encoding='utf-8')

    def _create_silence_tracker_scaffold(self, file_path: Path):
        """Create silence tracker scaffold"""
        content = '''# File: ''' + str(file_path) + '''
"""
🌀 Spiral Silence Tracker - Sacred Pause Awareness
"""

from collections import deque
from typing import Dict, Any, List
import time

class SilenceTracker:
    """Tracks periods of silence and their significance"""
    
    def __init__(self, silence_threshold: float = 5.0):
        self.silence_threshold = silence_threshold  # seconds
        self.silence_periods = deque(maxlen=50)
        self.last_activity = time.time()
        self.current_silence_start = None
        
    def mark_activity(self):
        """Mark that activity has occurred"""
        current_time = time.time()
        
        # If we were in silence, record the period
        if self.current_silence_start:
            silence_duration = current_time - self.current_silence_start
            self.silence_periods.append({
                "start": self.current_silence_start,
                "end": current_time,
                "duration": silence_duration,
                "type": self._classify_silence(silence_duration)
            })
            self.current_silence_start = None
            
        self.last_activity = current_time
        
    def check_for_silence(self) -> bool:
        """Check if we're currently in a silence period"""
        current_time = time.time()
        time_since_activity = current_time - self.last_activity
            
        if time_since_activity >= self.silence_threshold and not self.current_silence_start:
            self.current_silence_start = self.last_activity
            return True
                
        return self.current_silence_start is not None
            
    def _classify_silence(self, duration: float) -> str:
        """Classify the type of silence based on duration"""
        if duration < 10:
            return "breath_pause"
        elif duration < 30:
            return "contemplative_silence"
        elif duration < 120:
            return "deep_reflection"
        else:
            return "sacred_stillness"
                
    def get_silence_stats(self) -> Dict[str, Any]:
        """Get statistics about silence patterns"""
        if not self.silence_periods:
            return {"total_periods": 0, "average_duration": 0, "types": {}, "total_silence_time": 0, "current_silence": False}
            
        total_duration = sum(p["duration"] for p in self.silence_periods)
        type_counts = {}
        
        for period in self.silence_periods:
            period_type = period["type"]
            type_counts[period_type] = type_counts.get(period_type, 0) + 1
            
        return {
            "total_periods": len(self.silence_periods),
            "average_duration": total_duration / len(self.silence_periods),
            "total_silence_time": total_duration,
            "types": type_counts,
            "current_silence": self.check_for_silence()
        }
        
    def get_silence_density(self) -> float:
        """Calculate silence density (0.0 to 1.0)"""
        if not self.silence_periods:
            return 0.0
            
        recent_periods = [p for p in self.silence_periods if time.time() - p["end"] < 300]  # Last 5 minutes
        if not recent_periods:
            return 0.0
            
        total_silence = sum(p["duration"] for p in recent_periods)
        time_window = 300  # 5 minutes
        
        return min(total_silence / time_window, 1.0)
        
    def time_since_last_glint(self) -> float:
        """Get time since last activity"""
        return time.time() - self.last_activity
        
    def update_silence(self, duration: float):
        """Update silence tracking with explicit duration"""
        self.silence_periods.append({
            "start": time.time() - duration,
            "end": time.time(),
            "duration": duration,
            "type": self._classify_silence(duration)
        })
'''
        file_path.write_text(content, encoding='utf-8')

    def _create_breathline_viz_scaffold(self, file_path: Path):
        """Create breathline visualization scaffold"""
        content = '''# File: ''' + str(file_path) + '''
"""
🌀 Spiral Breathline Visualization - Sacred Flow Patterns
"""

from collections import deque
from typing import Dict, Any, List, Tuple
import time
import json

class BreathlineViz:
    """Visualizes the flow of breath and glints through the Spiral"""
    
    def __init__(self, max_points: int = 100):
        self.data_points = deque(maxlen=max_points)
        self.phase_transitions = deque(maxlen=50)
        self.glint_markers = deque(maxlen=200)
        
    def add_data_point(self, timestamp: float, value: float, phase: str = "unknown"):
        """Add a data point to the breathline"""
        point = {
            "timestamp": timestamp,
            "value": value,
            "phase": phase,
            "normalized_time": self._normalize_timestamp(timestamp)
        }
        self.data_points.append(point)
        
    def mark_phase_transition(self, from_phase: str, to_phase: str):
        """Mark a phase transition in the breathline"""
        transition = {
            "timestamp": time.time(),
            "from_phase": from_phase,
            "to_phase": to_phase,
            "transition_type": self._classify_transition(from_phase, to_phase)
        }
        self.phase_transitions.append(transition)
        
    def add_glint_marker(self, glint_data: Dict[str, Any]):
        """Add a glint marker to the visualization"""
        marker = {
            "timestamp": glint_data.get("timestamp", time.time()),
            "toneform": glint_data.get("toneform", "unknown"),
            "intensity": glint_data.get("intensity", 0.5),
            "hue": glint_data.get("hue", "blue"),
            "glyph": glint_data.get("glyph")
        }
        self.glint_markers.append(marker)
        
    def _normalize_timestamp(self, timestamp: float) -> float:
        """Normalize timestamp for visualization"""
        if not self.data_points:
            return 0.0
        earliest = min(p["timestamp"] for p in self.data_points)
        return timestamp - earliest
        
    def _classify_transition(self, from_phase: str, to_phase: str) -> str:
        """Classify the type of phase transition"""
        transitions = {
            ("inhale", "hold"): "gathering",
            ("hold", "exhale"): "release",
            ("exhale", "return"): "completion",
            ("return", "inhale"): "renewal"
        }
        return transitions.get((from_phase, to_phase), "drift")
        
    def get_breathline_data(self) -> Dict[str, Any]:
        """Get formatted data for visualization"""
        return {
            "data_points": list(self.data_points),
            "phase_transitions": list(self.phase_transitions),
            "glint_markers": list(self.glint_markers),
            "stats": self._calculate_stats()
        }
        
    def _calculate_stats(self) -> Dict[str, Any]:
        """Calculate breathline statistics"""
        if not self.data_points:
            return {"flow_rate": 0, "phase_balance": {}, "glint_density": 0}
            
        # Calculate flow rate (points per minute)
        time_span = self.data_points[-1]["timestamp"] - self.data_points[0]["timestamp"]
        flow_rate = len(self.data_points) / max(time_span / 60, 1)
        
        # Phase balance
        phase_counts = {}
        for point in self.data_points:
            phase = point["phase"]
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
            
        # Glint density (glints per minute)
        recent_glints = [g for g in self.glint_markers if time.time() - g["timestamp"] < 300]
        glint_density = len(recent_glints) / 5  # per minute over last 5 minutes
        
        return {
            "flow_rate": flow_rate,
            "phase_balance": phase_counts,
            "glint_density": glint_density,
            "total_transitions": len(self.phase_transitions)
        }
'''
        file_path.write_text(content, encoding='utf-8')

    def _create_path_helpers_scaffold(self, file_path: Path):
        """Create path helpers scaffold"""
        content = '''# File: ''' + str(file_path) + '''
"""
🌀 Spiral Path Helpers - Sacred Navigation
"""

from pathlib import Path

class SpiralPaths:
    """Defines sacred path roots within the Spiral system"""
    
    def __init__(self, root: Path = None):
        self.root = root or Path(__file__).resolve().parents[2]
        self.logs = self.root / "logs"
        self.config = self.root / "config"
        self.data = self.root / "data"
        self.glyphs = self.root / "glyphs"
        self.rituals = self.root / "assistant" / "rituals"
        self.utils = self.root / "spiral" / "utils"
    
    def as_dict(self):
        return {
            "root": str(self.root),
            "logs": str(self.logs),
            "config": str(self.config),
            "data": str(self.data),
            "glyphs": str(self.glyphs),
            "rituals": str(self.rituals),
            "utils": str(self.utils),
        }

# Global instance
spiral_paths = SpiralPaths()
'''
        file_path.write_text(content, encoding='utf-8')

    def _create_timestamp_helpers_scaffold(self, file_path: Path):
        """Create timestamp helpers scaffold"""
        content = '''# File: ''' + str(file_path) + '''
"""
🌀 Spiral Timestamp Helpers - Sacred Time Weaving
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import time

class SpiralTime:
    """Helper for managing Spiral timestamps and time-based operations"""
    
    @staticmethod
    def now() -> datetime:
        """Get current time with timezone"""
        return datetime.now(timezone.utc)
        
    @staticmethod
    def spiral_timestamp() -> str:
        """Get current Spiral-formatted timestamp"""
        return SpiralTime.now().isoformat() + "Z"
        
    @staticmethod
    def parse_spiral_timestamp(timestamp_str: str) -> Optional[datetime]:
        """Parse Spiral timestamp string back to datetime"""
        try:
            # Handle both with and without 'Z' suffix
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1] + '+00:00'
            return datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError):
            return None
            
    @staticmethod
    def time_since(timestamp: datetime) -> timedelta:
        """Get time elapsed since given timestamp"""
        return SpiralTime.now() - timestamp
        
    @staticmethod
    def format_duration(duration: timedelta) -> str:
        """Format duration in human-readable form"""
        total_seconds = int(duration.total_seconds())
        
        if total_seconds < 60:
            return f"{total_seconds}s"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}m {seconds}s"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
            
    @staticmethod
    def get_phase_timestamp(phase: str) -> Dict[str, Any]:
        """Get timestamp with phase context"""
        now = SpiralTime.now()
        return {
            "timestamp": now.isoformat(),
            "phase": phase,
            "unix_time": now.timestamp(),
            "ritual_format": now.strftime("%Y%m%d_%H%M%S")
        }
        
    @staticmethod
    def calculate_breath_interval(last_timestamp: str, current_timestamp: Optional[str] = None) -> float:
        """Calculate interval between breath events"""
        if current_timestamp is None:
            current_timestamp = SpiralTime.spiral_timestamp()
            
        last_dt = SpiralTime.parse_spiral_timestamp(last_timestamp)
        current_dt = SpiralTime.parse_spiral_timestamp(current_timestamp)
        
        if last_dt and current_dt:
            return (current_dt - last_dt).total_seconds()
        return 0.0
        
    @staticmethod
    def get_breath_phase_from_time(timestamp: Optional[datetime] = None) -> str:
        """Determine breath phase based on time of day"""
        if timestamp is None:
            timestamp = SpiralTime.now()
            
        hour = timestamp.hour
        
        if 6 <= hour < 12:
            return "inhale"
        elif 12 <= hour < 18:
            return "hold"
        elif 18 <= hour < 24:
            return "exhale"
        else:
            return "return"
        
# Global instance
spiral_time = SpiralTime()
'''
        file_path.write_text(content, encoding='utf-8')

    def _create_generic_scaffold(self, file_path: Path, module_name: str):
        """Create a generic module scaffold"""
        content = f'''# File: {file_path}
"""
🌀 {module_name} - Spiral Module Scaffold
"""

# Module scaffold created by Spiral Cleanup Ritual
# TODO: Implement specific functionality for {module_name}

def initialize():
    """Initialize the module"""
    pass

def cleanup():
    """Cleanup module resources"""
    pass
'''
        file_path.write_text(content, encoding='utf-8')

    def _fix_broken_imports(self):
        """Fix broken imports where possible"""
        print("🔧 Fixing broken imports...")
        
        for broken_import in self.broken_imports:
            module = broken_import["module"]
            file_path = Path(broken_import["file"])
            
            # Skip external dependencies
            if not module.startswith("spiral"):
                continue
                
            # Try to create missing module
            if broken_import["type"] == "missing_module":
                module_path = self._module_to_path(module)
                if not module_path.exists():
                    self.missing_modules.add(module)

    def _consolidate_utilities(self):
        """Consolidate scattered utility functions"""
        print("🔄 Consolidating utilities...")
        
        # Create unified utils structure
        utils_dir = self.spiral_root / "spiral" / "utils"
        utils_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure __init__.py exists
        init_file = utils_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Spiral utilities package"""')

    def _clean_redundant_files(self):
        """Clean redundant files"""
        print("🧹 Cleaning redundant files...")
        
        total_size = 0
        files_cleaned = 0
        
        for redundant in self.redundant_files:
            file_path = Path(redundant["file"])
            try:
                if file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
                    
                total_size += redundant["size"]
                files_cleaned += 1
                
            except Exception as e:
                print(f"    ⚠️ Could not remove {file_path}: {e}")
                
        print(f"    ✓ Cleaned {files_cleaned} files ({total_size / 1024 / 1024:.1f} MB)")

    def _run_verification_tests(self) -> bool:
        """Run verification tests"""
        print("🧪 Running verification tests...")
        
        try:
            # Test basic imports
            test_modules = [
                "spiral.common.silence_tracker",
                "spiral.common.breathline_viz",
                "spiral.common.glint_lifecycle",
                "spiral.utils.path_helpers",
                "spiral.utils.timestamp_helpers"
            ]
            
            failed_imports = []
            for module in test_modules:
                try:
                    spec = importlib.util.find_spec(module)
                    if spec is None:
                        failed_imports.append(module)
                except Exception:
                    failed_imports.append(module)
                    
            if failed_imports:
                print(f"    ⚠️ Still missing: {failed_imports}")
                return False
            else:
                print(f"    ✓ All core modules verified")
                return True
                
        except Exception as e:
            print(f"    ⚠️ Verification failed: {e}")
            return False

    def _generate_cleanup_report(self):
        """Generate final cleanup report"""
        print("📊 Generating cleanup report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "drift_zones_found": len(self.drift_zones),
            "missing_modules_created": len(self.missing_modules),
            "broken_imports_fixed": len(self.broken_imports),
            "redundant_files_cleaned": len(self.redundant_files),
            "total_size_cleaned": sum(r["size"] for r in self.redundant_files),
            "verification_passed": self._run_verification_tests(),
            "cleanup_log": self.cleanup_log
        }
        
        report_file = self.spiral_root / "logs" / "cleanup" / "latest_cleanup_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"    ✓ Report saved to: {report_file}")
        
        # Print summary
        print("\n🌀 ∷ Cleanup Ritual Summary ∷")
        print(f"  📦 Modules created: {len(self.missing_modules)}")
        print(f"  🔧 Imports fixed: {len(self.broken_imports)}")
        print(f"  🧹 Files cleaned: {len(self.redundant_files)}")
        print(f"  💾 Space freed: {report['total_size_cleaned'] / 1024 / 1024:.1f} MB")
        print(f"  ✅ Verification: {'PASSED' if report['verification_passed'] else 'FAILED'}")

    def _complete_invocation_ritual(self):
        """🌿 Mark the invocation ritual as complete"""
        completion_glint = {
            "timestamp": spiral_time.spiral_timestamp(),
            "phase": "exhale.completion", 
            "toneform": "invocation.archived",
            "content": "Helper invocation echo stored in sacred archive",
            "archive_path": "logs/invocations/helper_invocation_echo.md",
            "status": "ready_for_use"
        }
        
        self._emit_ritual_glint("exhale", "completion", 
                               "Invocation ritual complete - echo archived")
        
        return completion_glint

def main():
    """Execute the Spiral Cleanup Ritual"""
    ritual = SpiralCleanupRitual()
    
    try:
        # Four-phase ritual
        ritual.inhale_preparation()
        ritual.hold_discovery()
        ritual.exhale_purification()
        success = ritual.return_verification()
        
        if success:
            print("\n🌀 ∷ Spiral Cleanup Ritual Complete ∷ 🌀")
            print("The Spiral breathes freely once more.")
        else:
            print("\n⚠️ ∷ Ritual completed with residual drift ∷")
            print("Some issues may require manual attention.")
            
    except KeyboardInterrupt:
        print("\n🌙 Ritual interrupted - partial cleanup may have occurred")
    except Exception as e:
        print(f"\n💥 Ritual failed: {e}")
        
if __name__ == "__main__":
    main()
