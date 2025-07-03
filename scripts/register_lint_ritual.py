"""
Register the lint.breathe ritual with the Whisper Steward.

This script:
1. Validates the ritual configuration
2. Registers the ritual with the Whisper Steward
3. Sets up file watchers and event hooks
4. Verifies the installation
"""
import os
import sys
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/rituals/ritual_registration.log')
    ]
)
logger = logging.getLogger('ritual.register')

class RitualInstaller:
    """Handles the installation and registration of the lint.breathe ritual."""
    
    def __init__(self, config_path: Path):
        """Initialize with path to ritual configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.steward_config_dir = Path('config/whisper_steward')
        self.steward_config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load and validate the ritual configuration."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Basic validation
            required_sections = ['ritual', 'trigger', 'action']
            for section in required_sections:
                if section not in config.get('ritual', {}):
                    raise ValueError(f"Missing required section: {section}")
            
            return config
        except Exception as e:
            logger.error(f"Failed to load ritual config: {e}")
            raise
    
    def register_with_steward(self) -> bool:
        """Register the ritual with the Whisper Steward."""
        try:
            # Create the rituals directory if it doesn't exist
            rituals_dir = self.steward_config_dir / 'rituals'
            rituals_dir.mkdir(exist_ok=True)
            
            # Copy the ritual config to the steward's config directory
            target_path = rituals_dir / 'ritual_lint_breathe.yml'
            with open(target_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            logger.info(f"Registered ritual: {self.config['ritual']['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register ritual: {e}")
            return False
    
    def setup_file_watcher(self) -> bool:
        """Set up file watchers for the ritual."""
        try:
            # In a real implementation, this would set up system-level file watchers
            # For now, we'll just log the configuration
            triggers = self.config['ritual']['trigger']
            patterns = triggers.get('match', [])
            
            logger.info(f"Setting up file watcher for patterns: {patterns}")
            logger.info("File watcher will trigger on: %s", 
                       ", ".join(triggers.get('on', [])))
            
            # Create a simple watcher config that the steward will read
            watcher_config = {
                'watch': [{
                    'patterns': patterns if isinstance(patterns, list) else [patterns],
                    'handler': 'ritual.lint.breathe',
                    'events': triggers.get('on', [])
                }]
            }
            
            # Write the watcher config
            watcher_config_path = self.steward_config_dir / 'watchers' / 'lint_watcher.yml'
            watcher_config_path.parent.mkdir(exist_ok=True)
            
            with open(watcher_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(watcher_config, f)
            
            logger.info("File watcher configuration saved")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set up file watcher: {e}")
            return False
    
    def verify_installation(self) -> bool:
        """Verify that the ritual was installed correctly."""
        try:
            # Check if the ritual config exists in the steward's directory
            ritual_path = self.steward_config_dir / 'rituals' / 'ritual_lint_breathe.yml'
            if not ritual_path.exists():
                logger.error("Ritual config not found in steward directory")
                return False
            
            # Check if the watcher config exists
            watcher_path = self.steward_config_dir / 'watchers' / 'lint_watcher.yml'
            if not watcher_path.exists():
                logger.warning("Watcher config not found, but ritual is registered")
            
            logger.info("Installation verified successfully")
            return True
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False

def main():
    """Main entry point for the ritual registration script."""
    # Path to the ritual config file
    ritual_config_path = Path('spiral/rituals/ritual_lint_breathe.yml')
    
    if not ritual_config_path.exists():
        logger.error(f"Ritual config not found at {ritual_config_path}")
        return 1
    
    logger.info(f"Registering ritual from {ritual_config_path}")
    
    try:
        installer = RitualInstaller(ritual_config_path)
        
        # Register the ritual
        if not installer.register_with_steward():
            logger.error("Failed to register ritual with steward")
            return 1
        
        # Set up file watchers
        if not installer.setup_file_watcher():
            logger.error("Failed to set up file watcher")
            return 1
        
        # Verify installation
        if not installer.verify_installation():
            logger.error("Installation verification failed")
            return 1
        
        logger.info("Ritual registration completed successfully!")
        print("\n✨ Ritual 'ritual.lint.breathe' has been registered with the Whisper Steward.")
        print("   The Spiral will now watch for Python file changes and provide")
        print("   toneform-aware linting suggestions as you work.")
        print("\n   Next steps:")
        print("   1. Restart the Whisper Steward to activate the new ritual")
        print("   2. Try editing a Python file to see the linter in action")
        print("   3. Check PatternWeb for real-time glint visualization")
        
        return 0
        
    except Exception as e:
        logger.exception("An error occurred during ritual registration")
        return 1

if __name__ == "__main__":
    sys.exit(main())
