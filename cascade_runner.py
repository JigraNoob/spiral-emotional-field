"""
Runner script to launch Spiral Cascade as a background listener with logging and agent throttle active.
"""

import logging
import time
from pathlib import Path
from cascade import SpiralCascade, get_cascade

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("spiral.cascade_runner")

def run_cascade():
    """Run the Spiral Cascade system in the background."""
    logger.info("🌀 Initializing Spiral Cascade as background listener...")
    
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Initialize BreathloopEngine first to ensure ritual_start_time is set
    try:
        from assistant.breathloop_engine import BreathloopEngine, get_breathloop
        breath_engine = get_breathloop()
        if not breath_engine.running:
            breath_engine.start()
        logger.info("🌬️ BreathloopEngine initialized with ritual start time")
    except ImportError as e:
        logger.warning(f"⚠️ Could not initialize BreathloopEngine: {e}")
    
    # Get or initialize cascade instance
    cascade = get_cascade()
    
    # Start the cascade system
    cascade.start()
    
    logger.info("✨ Spiral Cascade running with Breath Throttle Monitor active")
    
    # Keep the runner alive to listen in the background
    try:
        while True:
            # Placeholder for potential future event listening or periodic checks
            time.sleep(60)  # Sleep for a minute before next check
            logger.debug("🌀 Cascade heartbeat - system active")
    except KeyboardInterrupt:
        logger.info("🛑 Received shutdown signal. Stopping Cascade...")
        cascade.stop()
        logger.info("✨ Cascade system stopped")

if __name__ == "__main__":
    run_cascade()
