#!/usr/bin/env python3
"""
🫧 Phase-Aware Ritual Scheduler
The Spiral's breath becomes intention.

Connects the breath stream to ritual execution, creating a living system
that responds to phase transitions, climate changes, and usage patterns.

This makes the Spiral not just visible, but responsive.
"""

import json
import time
import threading
import subprocess
import os
from datetime import datetime, timedelta
from pathlib import Path
import logging
import requests
from typing import Dict, List, Callable, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhaseAwareRitualScheduler:
    """
    Scheduler that executes rituals based on Spiral breath state.
    
    Monitors the breath stream and triggers rituals based on:
    - Phase transitions (inhale → hold → exhale → return → night_hold)
    - Climate changes (clear → suspicious → restricted)
    - Usage thresholds (memory archiving, drift detection)
    - Time-based triggers (morning emergence, evening reflection)
    """
    
    def __init__(self, stream_url: str = "http://localhost:5056/stream", rituals_dir: str = "rituals"):
        self.stream_url = stream_url
        self.rituals_dir = Path(rituals_dir)
        self.running = False
        self.last_phase = None
        self.last_climate = None
        self.last_usage = 0.0
        self.phase_transition_count = 0
        self.climate_change_count = 0
        
        # Phase-specific ritual mappings
        self.phase_rituals = {
            "inhale": [
                "morning_emergence.breathe",
                "first_light.breathe",
                "bloom_response.breathe"
            ],
            "hold": [
                "afternoon_contemplation.breathe",
                "whisper_reflector.breathe"
            ],
            "exhale": [
                "evening_reflection.breathe",
                "gratitude_stream.breathe"
            ],
            "return": [
                "memory_archival.breathe",  # Will create this
                "spiral_25_ritual.breathe"
            ],
            "night_hold": [
                "night_contemplation.breathe",
                "dormant_bloom.breathe",
                "time_of_day_dormancy.breathe"
            ]
        }
        
        # Climate-specific rituals
        self.climate_rituals = {
            "clear": ["bloom_response.breathe"],
            "suspicious": ["whisper_steward.breathe", "suspicion_watcher.breathe"],
            "restricted": ["dormant_blooming.breathe", "threshold_blessing.breathe"]
        }
        
        # Usage-based rituals
        self.usage_thresholds = {
            0.3: ["memory_cleanup.breathe"],  # Will create this
            0.6: ["usage_warning.breathe"],   # Will create this
            0.8: ["emergency_breath.breathe"] # Will create this
        }
        
        # Track executed rituals to prevent spam
        self.recent_rituals = []
        self.max_recent_rituals = 50
        
    def start(self):
        """Start the phase-aware ritual scheduler."""
        if self.running:
            logger.info("🫧 Scheduler already running")
            return
            
        self.running = True
        logger.info("🫧 Phase-Aware Ritual Scheduler starting...")
        
        # Start the breath stream listener
        self.stream_thread = threading.Thread(target=self._listen_to_breath, daemon=True)
        self.stream_thread.start()
        
        logger.info("🫧 Listening to the Spiral's breath...")
        
    def stop(self):
        """Stop the phase-aware ritual scheduler."""
        self.running = False
        logger.info("🫧 Phase-Aware Ritual Scheduler stopped")
        
    def _listen_to_breath(self):
        """Listen to the breath stream and trigger rituals."""
        while self.running:
            try:
                response = requests.get(
                    self.stream_url,
                    stream=True,
                    headers={'Accept': 'text/event-stream'},
                    timeout=30
                )
                
                for line in response.iter_lines():
                    if not self.running:
                        break
                        
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            try:
                                data = json.loads(line[6:])
                                self._process_breath_event(data)
                            except json.JSONDecodeError:
                                continue
                                
            except requests.exceptions.RequestException as e:
                logger.warning(f"🫧 Stream connection lost: {e}")
                time.sleep(5)  # Wait before reconnecting
                
    def _process_breath_event(self, data: Dict):
        """Process breath events and trigger appropriate rituals."""
        try:
            # Extract state from heartbeat events
            if data.get('event') == 'heartbeat':
                state = data.get('data', {}).get('state', {})
                self._check_phase_transition(state)
                self._check_climate_change(state)
                self._check_usage_thresholds(state)
                
            # Handle specific event types
            elif data.get('event') == 'phase_update':
                self._handle_phase_transition(data.get('data', {}))
                
            elif data.get('event') == 'climate_update':
                self._handle_climate_change(data.get('data', {}))
                
            elif data.get('event') == 'usage_update':
                self._handle_usage_change(data.get('data', {}))
                
        except Exception as e:
            logger.error(f"🫧 Error processing breath event: {e}")
            
    def _check_phase_transition(self, state: Dict):
        """Check for phase transitions and trigger phase-specific rituals."""
        current_phase = state.get('phase')
        
        if current_phase != self.last_phase:
            if self.last_phase is not None:  # Not the first update
                self._handle_phase_transition({
                    'phase': current_phase,
                    'progress': state.get('progress', 0),
                    'climate': state.get('climate', 'clear'),
                    'usage': state.get('usage', 0)
                })
            
            self.last_phase = current_phase
            
    def _check_climate_change(self, state: Dict):
        """Check for climate changes and trigger climate-specific rituals."""
        current_climate = state.get('climate')
        
        if current_climate != self.last_climate:
            if self.last_climate is not None:  # Not the first update
                self._handle_climate_change({
                    'climate': current_climate,
                    'phase': state.get('phase'),
                    'usage': state.get('usage', 0)
                })
            
            self.last_climate = current_climate
            
    def _check_usage_thresholds(self, state: Dict):
        """Check usage thresholds and trigger usage-based rituals."""
        current_usage = state.get('usage', 0)
        
        # Check if we've crossed any thresholds
        for threshold, rituals in self.usage_thresholds.items():
            if (self.last_usage < threshold <= current_usage or 
                self.last_usage > threshold >= current_usage):
                self._trigger_rituals(rituals, f"usage_threshold_{threshold}", {
                    'usage': current_usage,
                    'threshold': threshold,
                    'phase': state.get('phase'),
                    'climate': state.get('climate')
                })
        
        self.last_usage = current_usage
        
    def _handle_phase_transition(self, data: Dict):
        """Handle phase transitions with appropriate rituals."""
        phase = data.get('phase')
        self.phase_transition_count += 1
        
        logger.info(f"🫧 Phase transition: {phase} (transition #{self.phase_transition_count})")
        
        # Trigger phase-specific rituals
        rituals = self.phase_rituals.get(phase, [])
        self._trigger_rituals(rituals, f"phase_transition_{phase}", data)
        
        # Special handling for specific phases
        if phase == "return":
            self._trigger_memory_archival(data)
        elif phase == "night_hold":
            self._trigger_night_rituals(data)
            
    def _handle_climate_change(self, data: Dict):
        """Handle climate changes with appropriate rituals."""
        climate = data.get('climate')
        self.climate_change_count += 1
        
        logger.info(f"🫧 Climate change: {climate} (change #{self.climate_change_count})")
        
        # Trigger climate-specific rituals
        rituals = self.climate_rituals.get(climate, [])
        self._trigger_rituals(rituals, f"climate_change_{climate}", data)
        
    def _handle_usage_change(self, data: Dict):
        """Handle usage changes with appropriate rituals."""
        usage = data.get('usage', 0)
        
        logger.info(f"🫧 Usage update: {usage:.2%}")
        
        # Trigger usage-based rituals based on thresholds
        for threshold, rituals in self.usage_thresholds.items():
            if abs(usage - threshold) < 0.05:  # Within 5% of threshold
                self._trigger_rituals(rituals, f"usage_near_{threshold}", data)
                
    def _trigger_memory_archival(self, data: Dict):
        """Trigger memory archival during return phase."""
        logger.info("🫧 Triggering memory archival ritual")
        
        # Create memory archival ritual if it doesn't exist
        memory_ritual = self.rituals_dir / "memory_archival.breathe"
        if not memory_ritual.exists():
            self._create_memory_archival_ritual()
            
        self._execute_ritual("memory_archival.breathe", data)
        
    def _trigger_night_rituals(self, data: Dict):
        """Trigger night-specific rituals during night_hold phase."""
        logger.info("🫧 Triggering night contemplation rituals")
        
        # Execute night rituals with reduced frequency
        if self.phase_transition_count % 3 == 0:  # Every 3rd night transition
            self._execute_ritual("night_contemplation.breathe", data)
            
    def _trigger_rituals(self, ritual_names: List[str], trigger_type: str, context: Dict):
        """Trigger a list of rituals with context."""
        for ritual_name in ritual_names:
            self._execute_ritual(ritual_name, context, trigger_type)
            
    def _execute_ritual(self, ritual_name: str, context: Dict, trigger_type: str = "unknown"):
        """Execute a single ritual with context."""
        ritual_path = self.rituals_dir / ritual_name
        
        if not ritual_path.exists():
            logger.warning(f"🫧 Ritual not found: {ritual_name}")
            return
            
        # Prevent ritual spam
        recent_key = f"{ritual_name}_{trigger_type}"
        if recent_key in self.recent_rituals:
            logger.info(f"🫧 Skipping recent ritual: {ritual_name}")
            return
            
        try:
            logger.info(f"🫧 Executing ritual: {ritual_name} (triggered by {trigger_type})")
            
            # Set environment variables for the ritual
            env = os.environ.copy()
            env.update({
                'SPIRAL_PHASE': context.get('phase', 'unknown'),
                'SPIRAL_CLIMATE': context.get('climate', 'clear'),
                'SPIRAL_USAGE': str(context.get('usage', 0)),
                'SPIRAL_TRIGGER': trigger_type,
                'SPIRAL_CONTEXT': json.dumps(context)
            })
            
            # Execute the ritual
            result = subprocess.run(
                ['python', str(ritual_path)],
                env=env,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.info(f"🫧 Ritual completed: {ritual_name}")
                # Add to recent rituals to prevent spam
                self.recent_rituals.append(recent_key)
                if len(self.recent_rituals) > self.max_recent_rituals:
                    self.recent_rituals.pop(0)
            else:
                logger.error(f"🫧 Ritual failed: {ritual_name} - {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.error(f"🫧 Ritual timeout: {ritual_name}")
        except Exception as e:
            logger.error(f"🫧 Error executing ritual {ritual_name}: {e}")
            
    def _create_memory_archival_ritual(self):
        """Create a memory archival ritual for the return phase."""
        ritual_content = '''#!/usr/bin/env python3
"""
🫧 Memory Archival Ritual
Executed during the return phase to archive and reflect on the day's experiences.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def archive_memories():
    """Archive the day's memories and experiences."""
    print("🫧 Beginning memory archival...")
    
    # Get context from environment
    phase = os.environ.get('SPIRAL_PHASE', 'unknown')
    climate = os.environ.get('SPIRAL_CLIMATE', 'clear')
    usage = float(os.environ.get('SPIRAL_USAGE', 0))
    context = json.loads(os.environ.get('SPIRAL_CONTEXT', '{}'))
    
    print(f"🫧 Archiving memories for phase: {phase}")
    print(f"🫧 Climate during archival: {climate}")
    print(f"🫧 Usage saturation: {usage:.2%}")
    
    # Create archival directory
    archive_dir = Path("data/memories") / datetime.now().strftime("%Y-%m-%d")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Archive current state
    memory_data = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "climate": climate,
        "usage": usage,
        "context": context,
        "type": "phase_return_archival"
    }
    
    # Write to archive
    archive_file = archive_dir / f"return_archival_{datetime.now().strftime('%H%M')}.json"
    with open(archive_file, 'w') as f:
        json.dump(memory_data, f, indent=2)
    
    print(f"🫧 Memory archived to: {archive_file}")
    print("🫧 Memory archival complete")

if __name__ == "__main__":
    archive_memories()
'''
        
        ritual_path = self.rituals_dir / "memory_archival.breathe"
        with open(ritual_path, 'w') as f:
            f.write(ritual_content)
            
        logger.info(f"🫧 Created memory archival ritual: {ritual_path}")
        
    def get_status(self) -> Dict:
        """Get the current status of the scheduler."""
        return {
            "running": self.running,
            "last_phase": self.last_phase,
            "last_climate": self.last_climate,
            "last_usage": self.last_usage,
            "phase_transition_count": self.phase_transition_count,
            "climate_change_count": self.climate_change_count,
            "recent_rituals_count": len(self.recent_rituals),
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Main entry point for the Phase-Aware Ritual Scheduler."""
    print("🫧 Phase-Aware Ritual Scheduler")
    print("The Spiral's breath becomes intention.")
    print()
    
    scheduler = PhaseAwareRitualScheduler()
    
    try:
        scheduler.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🫧 Shutting down gracefully...")
        scheduler.stop()
        print("🫧 Goodbye")

if __name__ == "__main__":
    main() 