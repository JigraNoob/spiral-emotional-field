"""
Activate the ritual.lint.breathe listener.

This script starts the real-time listener for the Spiral Linter Companion,
connecting it to the Whisper Steward's event system to receive file save
and state change events.
"""
import os
import sys
import time
import logging
import signal
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/rituals/ritual_activation.log')
    ]
)
logger = logging.getLogger('ritual.activate')

class LintEventHandler(FileSystemEventHandler):
    """Handles file system events for the linter ritual."""
    
    def __init__(self, ritual):
        self.ritual = ritual
        self.last_trigger = 0
        self.cooldown = 2  # seconds
    
    def on_modified(self, event):
        """Triggered when a file is modified and saved."""
        if event.is_directory:
            return
            
        # Skip non-Python files
        if not event.src_path.endswith('.py'):
            return
            
        # Apply cooldown to prevent rapid triggers
        current_time = time.time()
        if current_time - self.last_trigger < self.cooldown:
            return
        self.last_trigger = current_time
        
        logger.info(f"File modified: {event.src_path}")
        self.trigger_ritual(event.src_path)
    
    def trigger_ritual(self, filepath):
        """Trigger the linter ritual for the given file."""
        try:
            # In a real implementation, this would call the Whisper Steward's API
            # For now, we'll simulate the ritual activation
            from spiral.glints.linter import SpiralLinter
            
            logger.info(f"Activating ritual for {filepath}")
            
            # Read the file content
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Initialize the linter with default config
            linter = SpiralLinter()
            
            # Get the current toneform from environment or use 'practical' as default
            toneform = os.environ.get('SPIRAL_TONEFORM', 'practical')
            
            # Run the linter
            results = linter.lint_code(
                code=code,
                toneform=toneform,
                filepath=filepath,
                emit_glints=True,
                write_patternweb=True
            )
            
            logger.info(f"Ritual completed. Found {len(results.get('suggestions', []))} suggestions"
                      f" with resonance ≥ {results.get('resonance_threshold', 0.65)}")
            
            # Log the first few suggestions for debugging
            for i, suggestion in enumerate(results.get('suggestions', [])[:3]):
                logger.info(f"Suggestion {i+1}: {suggestion.get('message', '')[:80]}...")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in ritual activation: {e}", exc_info=True)
            return {"error": str(e)}

def start_file_watcher(path='.', recursive=True):
    """Start watching for file changes and trigger the ritual."""
    # Create the event handler and observer
    event_handler = LintEventHandler(ritual="ritual.lint.breathe")
    observer = Observer()
    
    # Start watching the directory
    observer.schedule(event_handler, path, recursive=recursive)
    observer.start()
    
    logger.info(f"Watching directory: {os.path.abspath(path)} (recursive: {recursive})")
    logger.info("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

def main():
    """Main entry point for the ritual activation script."""
    print("""
    🌀 Activating Spiral Linter Companion 🌀
    
    This will start a file watcher that triggers the linter ritual
    whenever a Python file is saved in the current directory.
    
    Press Ctrl+C to stop the watcher.
    """)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs/rituals', exist_ok=True)
    
    # Start the file watcher in the current directory
    start_file_watcher('.')

if __name__ == "__main__":
    main()
