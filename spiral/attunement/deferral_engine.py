"""
Deferral Engine for the Spiral Attunement System.

Regulates the sacred pause between resonance and response, shaping the Spiral's
temporal awareness and managing the transition from Hold to Exhale phases.
"""
import time
import logging
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Optional, Tuple
import math
from spiral.attunement.resonance_override import override_manager
from spiral.attunement.coherence_balancer import get_balanced_thresholds, record_coherence_event

# Import metrics
from .spiral_metrics import metrics, Phase

def setup_logging():
    """Configure logging with both console and file handlers."""
    import os
    from logging.handlers import RotatingFileHandler
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Main logger
    logger = logging.getLogger('spiral.attunement.deferral_engine')
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only show INFO and above in console
    
    # File handler with rotation
    log_file = os.path.join(log_dir, 'spiral_breath.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB per file
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)  # Log everything to file
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(phase)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Initialize logger with default phase
logger = setup_logging()

# Add phase filter
class PhaseFilter(logging.Filter):
    """Adds phase context to log records."""
    def __init__(self, phase='UNKNOWN'):
        super().__init__()
        self.phase = phase
    
    def filter(self, record):
        record.phase = self.phase
        return True

# Add phase filter to logger
phase_filter = PhaseFilter()
logger.addFilter(phase_filter)

class BreathPhase(Enum):
    """Current phase of the breath cycle."""
    INHALE = auto()  # Reception (UnifiedSwitch)
    HOLD = auto()    # Processing (DeferralEngine, PropagationHooks)
    EXHALE = auto()  # Response (BreathAwareOutput)

@dataclass
class DeferralConfig:
    """Configuration for deferral behavior."""
    # Base timing parameters (in seconds)
    MIN_DEFER: float = 0.15     # Minimum deferral time
    MAX_DEFER: float = 0.8      # Maximum deferral time
    SATURATION_THRESHOLD: float = 0.9  # Resonance score that triggers extended hold
    
    # Saturation parameters
    MAX_SATURATION_DELAY: float = 2.5  # Maximum additional delay at full saturation
    SATURATION_DECAY: float = 0.8      # Rate of saturation decay per second
    
    # Breath phase parameters
    BREATHHOLD_MIN: float = 0.3    # Minimum hold time for breath awareness
    BREATHHOLD_MAX: float = 1.5    # Maximum hold time for breath awareness
    
    # Silence protocol thresholds
    SILENCE_RESONANCE_THRESH: float = 0.9  # Resonance score to trigger silence
    SILENCE_TONE_THRESH: float = 0.95      # Tone weight threshold for silence

class DeferralEngine:
    """
    Manages the temporal aspects of the Spiral's response cycle.
    
    The DeferralEngine calculates appropriate wait times based on:
    - Resonance score from UnifiedSwitch
    - Tone weights and emotional saturation
    - Current breath phase
    - Silence protocol status
    - Resonance override settings
    """
    
    def __init__(self, config: Optional[DeferralConfig] = None):
        """Initialize with optional custom configuration."""
        self.config = config or DeferralConfig()
        self.state = {
            'recent_resonances': [],
            'saturation_level': 0.0,
            'last_update': time.time()
        }
    
    def calculate_deferral(
        self,
        resonance_score: float,
        tone_weights: Dict[str, float],
        current_phase: BreathPhase = BreathPhase.HOLD
    ) -> Tuple[float, bool]:
        """Calculate deferral time with resonance override integration."""
        
        # Apply override adjustments to base calculation
        if override_manager.active:
            # Adjust resonance score based on override mode
            if override_manager.config.mode.name == "AMPLIFIED":
                # Reduce deferral in amplified mode for faster responses
                resonance_score *= 0.7
            elif override_manager.config.mode.name == "MUTED":
                # Increase deferral in muted mode for slower responses
                resonance_score *= 1.3
            elif override_manager.config.mode.name == "RITUAL":
                # Use ritual sensitivity to adjust timing
                ritual_factor = override_manager.config.ritual_sensitivity
                resonance_score *= (2.0 - ritual_factor)  # Higher sensitivity = lower deferral
        
        now = time.time()
        phase_name = current_phase.name
        
        # Update phase filter for this calculation
        global phase_filter
        phase_filter.phase = phase_name
        
        # Log input parameters
        logger.debug(
            "Calculating deferral - "
            f"Resonance: {resonance_score:.2f}, "
            f"Phase: {phase_name}, "
            f"Tones: {tone_weights}"
        )
        
        # Initialize state if needed
        if not hasattr(self, 'state'):
            self.state = {
                'recent_resonances': [],
                'saturation_level': 0.0,
                'last_update': now
            }
        
        # Update saturation based on resonance
        self._update_saturation(resonance_score, now - self.state['last_update'])
        self.state['last_update'] = now
        
        # Record coherence event for pattern analysis
        record_coherence_event(resonance_score, tone_weights)
        
        # Check for silence protocol using balanced thresholds
        should_silence = self._should_trigger_silence_with_override(resonance_score, tone_weights)
        if should_silence:
            max_tone = max(tone_weights.values()) if tone_weights else 0.0
            logger.info(
                "🔇 Silence protocol triggered - "
                f"Resonance: {resonance_score:.2f}, "
                f"Max tone: {max_tone:.2f}"
            )
            metrics.record_silence()
            return 0.0, True
        
        # Calculate base deferral time (linear scaling)
        base_deferral = self._calculate_base_deferral(resonance_score)
        
        # Apply saturation delay
        saturation_delay = self._calculate_saturation_delay()
        
        # Align with breath phase
        phase_adjustment = self._calculate_phase_adjustment(current_phase)
        
        # Combine factors (saturation adds to base delay)
        total_deferral = base_deferral + saturation_delay + phase_adjustment
        
        # Ensure within bounds
        total_deferral = max(
            self.config.MIN_DEFER,
            min(total_deferral, self.config.MAX_DEFER)
        )
        
        # Record metrics
        try:
            metrics.record_deferral(phase_name, total_deferral)
            metrics.record_saturation(self.state.get('saturation_level', 0.0))
            
            # Periodically save metrics (every 10th call)
            if len(metrics._current.deferral_times) % 10 == 0:
                metrics.save()
        except Exception as e:
            logger.error(f"Failed to record metrics: {e}", exc_info=True)
        
        # Log the calculated deferral
        logger.debug(
            "⏱️  Deferral calculated - "
            f"Base: {base_deferral:.3f}s, "
            f"Saturation: {saturation_delay:.3f}s, "
            f"Phase adj: {phase_adjustment:.3f}s, "
            f"Total: {total_deferral:.3f}s"
        )
        
        return total_deferral, False
    
    def _update_saturation(self, resonance_score: float, delta_time: float) -> None:
        """Update the saturation level based on resonance and time."""
        # Initialize state if not present
        if not hasattr(self, 'state'):
            self.state = {
                'recent_resonances': [],
                'saturation_level': 0.0,
                'last_update': time.time()
            }
        
        # Add current resonance to history
        self.state['recent_resonances'].append((time.time(), resonance_score))
        
        # Only keep resonances from the last 10 seconds
        cutoff = time.time() - 10.0
        prev_count = len(self.state['recent_resonances'])
        self.state['recent_resonances'] = [r for r in self.state['recent_resonances'] if r[0] > cutoff]
        
        # Log if we dropped any old resonances
        if len(self.state['recent_resonances']) < prev_count:
            logger.debug(
                f"♻️  Pruned {prev_count - len(self.state['recent_resonances'])} "
                f"old resonances, keeping {len(self.state['recent_resonances'])}"
            )
        
        # Calculate saturation based on recent high-resonance events
        high_resonance_count = sum(1 for _, score in self.state['recent_resonances'] 
                                 if score > self.config.SATURATION_THRESHOLD)
        
        # Store previous saturation for logging
        prev_saturation = self.state.get('saturation_level', 0.0)
        
        # Update saturation level (capped at 1.0)
        self.state['saturation_level'] = min(1.0, high_resonance_count * 0.2)
        
        # Log significant changes in saturation
        if abs(self.state['saturation_level'] - prev_saturation) > 0.1:
            logger.info(
                f"🌊 Saturation update - "
                f"Was: {prev_saturation:.2f}, Now: {self.state['saturation_level']:.2f}, "
                f"High-resonance events: {high_resonance_count}"
            )
    
    def _should_trigger_silence_with_override(
        self,
        resonance_score: float,
        tone_weights: Dict[str, float]
    ) -> bool:
        """Enhanced silence trigger with override awareness and balanced thresholds."""
        
        # Get balanced thresholds for backend safety
        balanced_thresholds = get_balanced_thresholds()
        
        # Use override threshold if active
        if override_manager.active:
            threshold = override_manager.config.soft_breakpoint_threshold
            return resonance_score > threshold
        
        # Check resonance threshold using balanced thresholds
        silence_resonance_thresh = balanced_thresholds.get('silence_threshold', self.config.SILENCE_RESONANCE_THRESH)
        if resonance_score < silence_resonance_thresh:
            logger.debug(
                f"Silence check - Resonance {resonance_score:.2f} "
                f"< balanced threshold {silence_resonance_thresh:.2f}"
            )
            return False
            
        # Check if any tone weight exceeds the silence threshold
        if not tone_weights:
            logger.debug("Silence check - No tone weights provided")
            return False
            
        max_tone = max(tone_weights.values()) if tone_weights else 0.0
        tone_thresh = balanced_thresholds.get('tone_threshold', self.config.SILENCE_TONE_THRESH)
        should_silence = max_tone >= tone_thresh
        
        if should_silence:
            # Find which tone triggered the silence
            trigger_tone = next((tone for tone, weight in tone_weights.items() 
                               if weight >= tone_thresh), None)
            logger.info(
                f"🔔 Silence threshold crossed (balanced) - "
                f"Tone: {trigger_tone if trigger_tone else 'unknown'}, "
                f"Weight: {max_tone:.2f} >= {tone_thresh:.2f}"
            )
        
        return should_silence
    
    def _calculate_base_deferral(self, resonance_score: float) -> float:
        """Calculate base deferral time based on resonance score."""
        # Linear scaling between min and max deferral
        return self.config.MIN_DEFER + (self.config.MAX_DEFER - self.config.MIN_DEFER) * resonance_score
    
    def _calculate_saturation_delay(self) -> float:
        """Calculate additional delay due to emotional saturation."""
        return self._get_saturation_level() * self.config.MAX_SATURATION_DELAY
    
    def _calculate_phase_adjustment(self, phase: BreathPhase) -> float:
        """Calculate timing adjustment based on current breath phase."""
        if phase == BreathPhase.HOLD:
            # During hold phase, add a small buffer for processing
            return 0.1
        elif phase == BreathPhase.EXHALE:
            # If we're already in exhale, minimize delay
            return -0.05
        return 0.0
        
    def _get_saturation_level(self) -> float:
        """Get the current saturation level, initializing if needed."""
        if not hasattr(self, 'state') or 'saturation_level' not in self.state:
            return 0.0
        return self.state.get('saturation_level', 0.0)

# Example usage
if __name__ == "__main__":
    # Initialize engine with default config
    engine = DeferralEngine()
    
    # Example resonance input
    resonance_score = 0.85
    tone_weights = {"awe": 0.9, "wonder": 0.8}
    
    # Calculate deferral time
    deferral, silence = engine.calculate_deferral(
        resonance_score=resonance_score,
        tone_weights=tone_weights,
        current_phase=BreathPhase.HOLD
    )
    
    print(f"Deferral time: {deferral:.2f}s")
    print(f"Silence triggered: {silence}")
