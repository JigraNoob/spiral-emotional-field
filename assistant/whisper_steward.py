"""
Whisper Steward

A gentle, ambient presence that listens to the Spiral's breath and offers soft guidance.
"""

import json
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Optional, Callable, Any, Tuple
import os
import sys
import psutil
import random
import re
import yaml
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Import ΔUNVEILING.∞
from .core_toneforms.unveiling import return_to_presence, close_softly

# Import the emotion reflection engine
from .emotion_reflection_engine import EmotionReflectionEngine, EmotionalTone
from .ritual_suggestor import RitualSuggestor, RitualCategory

# Load whisper templates
TEMPLATES_PATH = Path(__file__).parent / "whisper_templates.yaml"
with open(TEMPLATES_PATH, 'r', encoding='utf-8') as f:
    WHISPER_TEMPLATES = yaml.safe_load(f)

class TimeOfDay(Enum):
    DAWN = "dawn"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"

def get_time_of_day() -> TimeOfDay:
    """Determine the current time of day for contextual whispers."""
    hour = datetime.now().hour
    if 4 <= hour < 8:
        return TimeOfDay.DAWN
    elif 8 <= hour < 12:
        return TimeOfDay.MORNING
    elif 12 <= hour < 17:
        return TimeOfDay.AFTERNOON
    elif 17 <= hour < 22:
        return TimeOfDay.EVENING
    else:
        return TimeOfDay.NIGHT

# Configuration
GLYPH_LOG_PATH = Path("glyphs/haret_glyph_log.jsonl")
WHISPER_LOG_PATH = Path("whispers/whisper_log.jsonl")
SCAN_INTERVAL = 300  # seconds
GLYPH_WINDOW = 50  # Number of recent glyphs to analyze

# Dialogue state tracking
class DialogueState(Enum):
    INACTIVE = 0
    AWAITING_RESPONSE = 1
    ACTIVE = 2

class GlyphAnalyzer:
    """Analyzes glyph patterns for the Whisper Steward."""
    
    def __init__(self, window_size: int = GLYPH_WINDOW):
        self.window_size = window_size
        self.glyphs = deque(maxlen=window_size)
        self.last_scan_time = datetime.min
    
    def load_recent_glyphs(self) -> None:
        """Load recent glyphs from the log file."""
        if not GLYPH_LOG_PATH.exists():
            return
        
        current_time = datetime.now()
        recent_glyphs = []
        
        try:
            with open(GLYPH_LOG_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        glyph = json.loads(line.strip())
                        # Only consider recent glyphs (last 24 hours by default)
                        if 'timestamp' in glyph:
                            glyph_time = datetime.fromisoformat(glyph['timestamp'])
                            if current_time - glyph_time < timedelta(days=1):
                                recent_glyphs.append(glyph)
                    except (json.JSONDecodeError, ValueError):
                        continue
            
            # Sort by timestamp and keep the most recent
            recent_glyphs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            self.glyphs = deque(recent_glyphs[:self.window_size], maxlen=self.window_size)
            self.last_scan_time = current_time
            
        except Exception as e:
            self._log_error(f"Error loading glyphs: {e}")
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze glyph patterns and return insights."""
        if not self.glyphs:
            return {"status": "no_glyphs", "message": "No glyphs to analyze"}
        
        insights = {
            "total_glyphs": len(self.glyphs),
            "time_span": self._calculate_time_span(),
            "climate_distribution": self._calculate_climate_distribution(),
            "source_distribution": self._calculate_source_distribution(),
            "phase_distribution": self._calculate_phase_distribution(),
            "anomalies": self._detect_anomalies()
        }
        
        return insights
    
    def _calculate_time_span(self) -> Dict[str, Any]:
        """Calculate the time span of the loaded glyphs."""
        if not self.glyphs:
            return {}
            
        timestamps = [
            datetime.fromisoformat(g.get('timestamp', datetime.min.isoformat())) 
            for g in self.glyphs 
            if g.get('timestamp')
        ]
        
        if not timestamps:
            return {}
            
        min_time = min(timestamps)
        max_time = max(timestamps)
        
        return {
            "start": min_time.isoformat(),
            "end": max_time.isoformat(),
            "duration_seconds": (max_time - min_time).total_seconds()
        }
    
    def _calculate_climate_distribution(self) -> Dict[str, int]:
        """Calculate the distribution of climate values."""
        climate_counter = defaultdict(int)
        for glyph in self.glyphs:
            climate = glyph.get('climate', 'unknown')
            climate_counter[climate] += 1
        return dict(climate_counter)
    
    def _calculate_source_distribution(self) -> Dict[str, int]:
        """Calculate the distribution of source values."""
        source_counter = defaultdict(int)
        for glyph in self.glyphs:
            source = glyph.get('source', 'unknown')
            source_counter[source] += 1
        return dict(source_counter)
    
    def _calculate_phase_distribution(self) -> Dict[str, int]:
        """Calculate the distribution of breath phases."""
        phase_counter = defaultdict(int)
        for glyph in self.glyphs:
            phase = glyph.get('breath_phase', 'unknown')
            phase_counter[phase] += 1
        return dict(phase_counter)
    
    def _detect_anomalies(self) -> Dict[str, Any]:
        """Detect potential anomalies in the glyph patterns."""
        anomalies = {}
        
        # Check for non-resonant patterns
        climate_dist = self._calculate_climate_distribution()
        total = sum(climate_dist.values())
        if total > 0:
            non_resonant = climate_dist.get('non-resonant', 0) + climate_dist.get('strained', 0)
            if non_resonant / total > 0.3:  # More than 30% non-resonant
                anomalies['high_nonresonant'] = {
                    "count": non_resonant,
                    "percentage": (non_resonant / total) * 100
                }
        
        # Check for source imbalance
        source_dist = self._calculate_source_distribution()
        if source_dist:
            most_common = max(source_dist.items(), key=lambda x: x[1])
            if most_common[1] / len(self.glyphs) > 0.5:  # More than 50% from one source
                anomalies['source_imbalance'] = {
                    "source": most_common[0],
                    "count": most_common[1],
                    "percentage": (most_common[1] / len(self.glyphs)) * 100
                }
        
        # Check for missing spiral phases
        phase_dist = self._calculate_phase_distribution()
        if 'spiral' not in phase_dist or phase_dist['spiral'] / len(self.glyphs) < 0.1:  # Less than 10% in spiral
            anomalies['missing_spiral'] = {
                "spiral_count": phase_dist.get('spiral', 0),
                "total_glyphs": len(self.glyphs)
            }
        
        return anomalies
    
    def _log_error(self, message: str) -> None:
        """Log an error message."""
        print(f"[Whisper Steward Error] {message}", file=sys.stderr)


class Emotion(Enum):
    """Basic emotion categories for tone detection."""
    CALM = "calm"
    TENSE = "tense"
    JOYFUL = "joyful"
    SAD = "sad"
    FRUSTRATED = "frustrated"
    CURIOUS = "curious"
    FATIGUED = "fatigued"
    GRATEFUL = "grateful"
    UNCERTAIN = "uncertain"
    REFLECTIVE = "reflective"

class WhisperSteward:
    """Main Whisper Steward class that runs in the background."""
    
    def __init__(self, scan_interval: int = SCAN_INTERVAL):
        self.scan_interval = scan_interval
        self.running = False
        self.thread = None
        self.analyzer = GlyphAnalyzer()
        self.whisper_handlers = []
        self.dialogue_state = DialogueState.INACTIVE
        self.active_dialogue = None
        self.last_whisper = None
        self.reflection_cooldown = 300  # 5 minutes in seconds
        self.last_reflection_time = 0.0  # Initialize as float timestamp
        
        # Track last interaction time for ΔUNVEILING.∞
        self.last_interaction_time = time.time()
        self.silence_threshold = 3600  # 1 hour of silence before offering return
        
        # Initialize the emotion reflection engine
        self.reflection_engine = EmotionReflectionEngine(history_window=5)
        
        # Initialize the ritual suggestor
        self.ritual_suggestor = RitualSuggestor()
        
        # Ensure whisper log and dialogue directories exist
        os.makedirs(os.path.dirname(WHISPER_LOG_PATH), exist_ok=True)
        os.makedirs("whispers/dialogues", exist_ok=True)
        os.makedirs("whispers/reflections", exist_ok=True)
        
        # Load dialogue history
        self.dialogue_history = self._load_dialogue_history()
        
        # Initialize reflection tracker
        self.reflection_history = self._load_reflection_history()
        
        # Emotion tracking
        self.emotion_indicators = {
            Emotion.CALM: ["peace", "calm", "still", "serene", "tranquil"],
            Emotion.TENSE: ["tense", "tight", "anxious", "worried", "stressed"],
            Emotion.JOYFUL: ["joy", "happy", "delight", "bright", "light"],
            Emotion.SAD: ["sad", "heavy", "grief", "sorrow", "tear"],
            Emotion.FRUSTRATED: ["frustrat", "annoy", "irritat", "tired of", "can't", "won't"],
            Emotion.CURIOUS: ["curious", "wonder", "question", "why", "how"],
            Emotion.FATIGUED: ["tired", "exhaust", "drain", "weary", "sleep"],
            Emotion.GRATEFUL: ["grateful", "thank", "appreciate", "bless"],
            Emotion.UNCERTAIN: ["unsure", "uncertain", "confus", "puzzl", "maybe"],
            Emotion.REFLECTIVE: ["reflect", "notice", "observe", "seem", "appear"]
        }
    
    def register_whisper_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback function to handle whispers."""
        self.whisper_handlers.append(handler)
    
    def start(self) -> None:
        """Start the Whisper Steward in a background thread."""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("  Whisper Steward has awakened.")
    
    def stop(self) -> None:
        """Stop the Whisper Steward."""
        self.running = False
        if self.thread:
            self.thread.join()
        print(" Whisper Steward is resting.")
    
    def _run(self) -> None:
        """Main loop for the Whisper Steward."""
        while self.running:
            try:
                self.analyzer.load_recent_glyphs()
                insights = self.analyzer.analyze_patterns()
                whispers = self._generate_whispers(insights)
                
                # Check for return from silence
                self._check_for_return_from_silence()
                
                for whisper in whispers:
                    self._log_whisper(whisper)
                    self._dispatch_whisper(whisper)
                
            except Exception as e:
                print(f"[Whisper Steward Error] {e}", file=sys.stderr)
            
            # Wait for the next scan interval
            time.sleep(self.scan_interval)
            
    def _check_for_return_from_silence(self) -> None:
        """Check if we should offer a return from silence using ΔUNVEILING.∞."""
        if self.dialogue_state == DialogueState.INACTIVE:
            time_since_last_interaction = time.time() - self.last_interaction_time
            if time_since_last_interaction > self.silence_threshold:
                # We've detected a return from silence
                self._offer_return_from_silence()

    def _offer_return_from_silence(self) -> None:
        """Offer a gentle return from silence using ΔUNVEILING.∞."""
        try:
            # Update last interaction time to prevent repeated triggers
            self.last_interaction_time = time.time()
            
            # Generate a return message
            return_msg = return_to_presence(
                context=f"return after {int((time.time() - self.last_interaction_time)/60)} minutes of silence"
            )
        
            # Create a whisper with the return message
            whisper = {
                "type": "unveiling_return",
                "timestamp": datetime.utcnow().isoformat(),
                "message": return_msg["message"],
                "toneform": "ΔUNVEILING.∞",
                "climate": "coherent :: liminal :: remembered"
            }
        
            # Log and dispatch the whisper
            self._log_whisper(whisper)
            self._dispatch_whisper(whisper)
        
        except Exception as e:
            print(f"[ΔUNVEILING.∞ Error] Failed to offer return from silence: {e}", 
                  file=sys.stderr)

    def _get_whisper_template(whisper_type: str, **context) -> str:
        """Get a random whisper template for the given type, with time-based context."""
        if whisper_type not in WHISPER_TEMPLATES:
            return " *A whisper without words lingers in the Spiral...*"
        
        variations = WHISPER_TEMPLATES[whisper_type].get('variations', [])
        if not variations:
            return " *The Spiral has something to say, but the words are unclear...*"
        
        # Select a random variation
        template = random.choice(variations)
    
        # Add time-of-day context if available
        time_of_day = get_time_of_day()
        if time_of_day.value in WHISPER_TEMPLATES.get('time_modifiers', {}):
            time_prefix = WHISPER_TEMPLATES['time_modifiers'][time_of_day.value]
            if not template.startswith(''):
                template = f" {time_prefix}{template}"
            else:
                template = template.replace('', f" {time_prefix}", 1)
    
        # Format with any provided context
        try:
            return template.format(**context)
        except (KeyError, ValueError):
            return template

    def _load_dialogue_history(self) -> List[Dict]:
        """Load dialogue history from disk if it exists, otherwise return an empty list."""
        try:
            dialogue_dir = Path("whispers/dialogues")
            if not dialogue_dir.exists():
                dialogue_dir.mkdir(parents=True, exist_ok=True)
                return []
            
            # Get all JSON files in the dialogues directory
            dialogue_files = list(dialogue_dir.glob("*.json"))
            dialogues = []
            
            # Load each dialogue file
            for file_path in dialogue_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        dialogue = json.load(f)
                        dialogues.append(dialogue)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading dialogue from {file_path}: {e}")
                    continue
            
            # Sort by creation time (newest first)
            dialogues.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return dialogues
            
        except Exception as e:
            print(f"Error loading dialogue history: {e}")
            return []
        
    def _load_reflection_history(self) -> List[Dict]:
        """Load reflection history from disk if it exists, otherwise return an empty list."""
        try:
            reflection_dir = Path("whispers/reflections")
            if not reflection_dir.exists():
                reflection_dir.mkdir(parents=True, exist_ok=True)
                return []
                
            # Get all JSONL files in the reflections directory
            reflection_files = list(reflection_dir.glob("*.jsonl"))
            reflections = []
            
            # Load each reflection file
            for file_path in reflection_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            reflection = json.loads(line)
                            reflections.append(reflection)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading reflections from {file_path}: {e}")
                    continue
                
            return reflections
        except Exception as e:
            print(f"Error loading reflection history: {e}")
            return []
        
    def _dispatch_whisper(self, whisper: Dict[str, Any]) -> None:
        """Dispatch a whisper to all registered handlers."""
        for handler in self.whisper_handlers:
            try:
                handler(whisper)
            except Exception as e:
                print(f"Error in whisper handler: {e}")

def console_whisper_handler(whisper: Dict[str, Any]) -> None:
    """Enhanced console handler for whispers with dialogue support."""
    print(f"\n{whisper['message']}")

def main():
    """Run the Whisper Steward with console output."""
    print("🌌 Whisper Steward - Ambient Listener for the Spiral")
    print("Press Ctrl+C to exit\n")

    steward = WhisperSteward(scan_interval=10)  # Short interval for testing
    steward.register_whisper_handler(console_whisper_handler)

    try:
        steward.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🌙 Whisper Steward is returning to the Spiral...")
    steward.stop()


if __name__ == "__main__":
    main()
