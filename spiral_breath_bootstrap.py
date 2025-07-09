#!/usr/bin/env python3
"""
🌀 Spiral Breath Bootstrap
A breath-aware environment adapter that reads spiral.env and adapts gracefully.

The Spiral must breathe with its environment, not bind it.
Invocation should be a gesture, not a constraint.
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
import configparser
import logging

# Configure gentle logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('spiral.breath')

class SpiralBreathBootstrap:
    """Breath-aware environment bootstrap for the Spiral system."""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.env_file = self.project_root / "spiral.env"
        self.config = self._load_breath_profile()
        
    def _load_breath_profile(self) -> Dict[str, str]:
        """Load the breath profile from spiral.env and breathe.json with graceful fallbacks."""
        config = {
            'MIN_PYTHON': '3.10',
            'PREFERRED_ENVIRONMENT': 'swe-1',
            'BREATH_MODE': 'soft',
            'WARN_ON_MISSING_ENV': 'true',
            'SUGGEST_ACTIVATION': 'true',
            'ALLOW_AMBIENT_MODE': 'true',
            'AUTO_BROWSER': 'true',
            'DEFAULT_PORT': '5000',
            'PYTHON_VARIANTS': 'python,python3,py',
            'VENV_PATHS': 'swe-1,venv,.venv'
        }
        
        # First, try to load breathe.json for comprehensive profile
        breathe_json_path = self.project_root / "breathe.json"
        if breathe_json_path.exists():
            try:
                with open(breathe_json_path, 'r') as f:
                    breathe_config = json.load(f)
                    # Extract relevant settings from breathe.json
                    if 'environment' in breathe_config:
                        env_config = breathe_config['environment']
                        config['PREFERRED_ENVIRONMENT'] = env_config.get('preferred', config['PREFERRED_ENVIRONMENT'])
                        config['PYTHON_VARIANTS'] = ','.join(env_config.get('python_variants', config['PYTHON_VARIANTS'].split(',')))
                        config['VENV_PATHS'] = ','.join(env_config.get('alternatives', config['VENV_PATHS'].split(',')))
                    
                    if 'breath' in breathe_config:
                        breath_config = breathe_config['breath']
                        config['BREATH_MODE'] = breath_config.get('mode', config['BREATH_MODE'])
                        if 'tolerance' in breath_config:
                            tolerance = breath_config['tolerance']
                            config['MIN_PYTHON'] = tolerance.get('python_version', config['MIN_PYTHON'])
                    
                    if 'invocation' in breathe_config:
                        inv_config = breathe_config['invocation']
                        config['AUTO_BROWSER'] = str(inv_config.get('auto_browser', config['AUTO_BROWSER'])).lower()
                        if 'rituals' in inv_config and 'dashboard' in inv_config['rituals']:
                            config['DEFAULT_PORT'] = str(inv_config['rituals']['dashboard'].get('port', config['DEFAULT_PORT']))
                
                logger.info("🌀 Loaded comprehensive breath profile from breathe.json")
            except Exception as e:
                logger.warning(f"⚠️ Could not read breathe.json: {e}")
        
        # Then, load spiral.env for simple overrides
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            config[key.strip()] = value.strip()
                logger.info("🌀 Applied spiral.env overrides")
            except Exception as e:
                logger.warning(f"⚠️ Could not read spiral.env: {e}")
        
        if not breathe_json_path.exists() and not self.env_file.exists():
            logger.info("🫧 No breath profiles found, using breath defaults")
            
        return config
    
    def detect_python_version(self) -> Tuple[Optional[str], Optional[str]]:
        """Detect Python version with graceful fallbacks."""
        python_variants = self.config['PYTHON_VARIANTS'].split(',')
        
        for variant in python_variants:
            try:
                result = subprocess.run(
                    [variant, '--version'], 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                version_str = result.stdout.strip()
                logger.info(f"🐍 Found Python: {variant} - {version_str}")
                return variant, version_str
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        logger.warning("⚠️ No Python variant found in PATH")
        return None, None
    
    def check_python_compatibility(self, version_str: str) -> bool:
        """Check Python version compatibility with gentle warnings."""
        try:
            # Extract version number (e.g., "Python 3.11.0" -> "3.11")
            version_parts = version_str.split()[1].split('.')
            major, minor = int(version_parts[0]), int(version_parts[1])
            
            min_version_parts = self.config['MIN_PYTHON'].split('.')
            min_major, min_minor = int(min_version_parts[0]), int(min_version_parts[1])
            
            if major < min_major or (major == min_major and minor < min_minor):
                logger.warning(f"⚠️ Python version {major}.{minor} is below recommended {self.config['MIN_PYTHON']}")
                logger.info("🫧 Spiral may not breathe fully, but will attempt to continue")
                return False
            else:
                logger.info(f"✅ Python version {major}.{minor} is compatible")
                return True
                
        except (IndexError, ValueError) as e:
            logger.warning(f"⚠️ Could not parse Python version: {e}")
            return True  # Assume compatible if we can't parse
    
    def find_virtual_environment(self) -> Optional[Path]:
        """Find virtual environment with graceful fallbacks."""
        venv_paths = self.config['VENV_PATHS'].split(',')
        
        for venv_name in venv_paths:
            venv_path = self.project_root / venv_name
            if venv_path.exists():
                # Check if it's actually a virtual environment
                if (venv_path / "Scripts" / "activate.bat").exists() or \
                   (venv_path / "bin" / "activate").exists():
                    logger.info(f"🌿 Found virtual environment: {venv_name}")
                    return venv_path
        
        logger.info("🫧 No virtual environment found")
        return None
    
    def suggest_environment_activation(self, venv_path: Path) -> None:
        """Suggest environment activation without enforcing it."""
        if self.config['SUGGEST_ACTIVATION'].lower() == 'true':
            if platform.system() == "Windows":
                logger.info(f"💡 To activate environment: {venv_path}\\Scripts\\activate.bat")
            else:
                logger.info(f"💡 To activate environment: source {venv_path}/bin/activate")
    
    def check_core_dependencies(self) -> Dict[str, bool]:
        """Check core dependencies with tone-aware reporting."""
        core_deps = ['flask', 'flask_socketio', 'requests']
        results = {}
        
        for dep in core_deps:
            try:
                subprocess.run([sys.executable, '-c', f'import {dep}'], 
                             capture_output=True, check=True)
                results[dep] = True
                logger.info(f"✅ {dep} available")
            except subprocess.CalledProcessError:
                results[dep] = False
                logger.warning(f"⚠️ {dep} not available")
        
        return results
    
    def adapt_environment(self) -> Dict[str, Any]:
        """Adapt the environment based on breath profile."""
        logger.info("🌀 Spiral breath initializing...")
        
        # Detect Python
        python_cmd, version_str = self.detect_python_version()
        if not python_cmd:
            logger.error("❌ No Python found - Spiral cannot breathe")
            return {'success': False, 'error': 'No Python found'}
        
        # Check compatibility
        if version_str:
            self.check_python_compatibility(version_str)
        
        # Find virtual environment
        venv_path = self.find_virtual_environment()
        if venv_path:
            self.suggest_environment_activation(venv_path)
        elif self.config['WARN_ON_MISSING_ENV'].lower() == 'true':
            logger.warning("⚠️ No virtual environment found")
            if self.config['ALLOW_AMBIENT_MODE'].lower() == 'true':
                logger.info("🫧 Proceeding in ambient mode")
        
        # Check dependencies
        deps = self.check_core_dependencies()
        
        # Set environment variables
        env_vars = {
            'SPIRAL_PROJECT_ROOT': str(self.project_root),
            'SPIRAL_BREATH_MODE': self.config['BREATH_MODE'],
            'SPIRAL_DEFAULT_PORT': self.config['DEFAULT_PORT'],
            'SPIRAL_AUTO_BROWSER': self.config['AUTO_BROWSER']
        }
        
        if python_cmd:
            env_vars['SPIRAL_PYTHON_CMD'] = python_cmd
        
        if venv_path:
            env_vars['SPIRAL_VENV_PATH'] = str(venv_path)
        
        # Update current environment
        for key, value in env_vars.items():
            os.environ[key] = value
        
        logger.info("✅ Spiral breath initialized successfully")
        
        return {
            'success': True,
            'python_cmd': python_cmd,
            'venv_path': venv_path,
            'dependencies': deps,
            'env_vars': env_vars
        }
    
    def run_ritual(self, ritual_name: str = None) -> bool:
        """Run a Spiral ritual with breath-aware error handling."""
        if not ritual_name:
            ritual_name = self.config.get('DEFAULT_RITUAL', 'natural_breath')
        
        logger.info(f"🕯️ Running ritual: {ritual_name}")
        
        # Adapt environment first
        result = self.adapt_environment()
        if not result['success']:
            return False
        
        # Try to run the ritual
        try:
            # This would be expanded based on actual ritual implementations
            logger.info(f"🌀 Ritual {ritual_name} completed")
            return True
        except Exception as e:
            logger.error(f"❌ Ritual {ritual_name} failed: {e}")
            return False

def main():
    """Main entry point for breath bootstrap."""
    bootstrap = SpiralBreathBootstrap()
    result = bootstrap.adapt_environment()
    
    if result['success']:
        print("🌀 Spiral is breathing with its environment")
        python_cmd = result.get('python_cmd')
        if python_cmd:
            print(f"🐍 Python: {python_cmd}")
        else:
            print("🐍 Python: Not detected")
        if result['venv_path']:
            print(f"🌿 Environment: {result['venv_path'].name}")
        else:
            print("🫧 Mode: Ambient")
    else:
        print(f"❌ Spiral could not breathe: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main() 