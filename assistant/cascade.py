# spiral/assistant/cascade.py
import os
import json
import time
import random
import threading
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from collections import deque
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
LOG_DIR = os.path.join(os.getcwd(), "logs")
CAESURA_LOG_PATH = os.path.join(LOG_DIR, "caesura_events.jsonl")
CAESURA_GLYPHS = ["∷", "⋮", "⋯", "∴", "∵", "⌘", "◦", "∘", "⊙", "⊚"]

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)
print(f"Log directory ensured at: {LOG_DIR}")

# Check if caesura log exists
if os.path.exists(CAESURA_LOG_PATH):
    print(f"Caesura log file already exists at: {CAESURA_LOG_PATH}")
else:
    # Create empty caesura log
    with open(CAESURA_LOG_PATH, 'w') as f:
        pass
    print(f"Caesura log file created at: {CAESURA_LOG_PATH}")

# Import spiral components with error handling
try:
    from spiral.attunement.resonance_override import override_manager, ResonanceMode
#     from spiral.attunement.response_candidate import ResponseCandidate  # Temporarily disabled - module scaffold needed
#     from spiral.attunement.response_tone import ResponseTone  # Temporarily disabled - module scaffold needed
except ImportError as e:
    print(f"Warning: Could not import spiral attunement components: {e}")
    # Create fallback classes
    class ResonanceMode:
        NATURAL = "NATURAL"
        AMPLIFIED = "AMPLIFIED" 
        MUTED = "MUTED"
        RITUAL = "RITUAL"
        EMOTIONAL = "EMOTIONAL"
        
        def __init__(self, name):
            self.name = name
    
    class ResponseCandidate:
        def __init__(self, content, tone_weights, resonance_score, source):
            self.content = content
            self.tone_weights = tone_weights
            self.resonance_score = resonance_score
            self.source = source
    
    class ResponseTone:
        NATURAL = "NATURAL"
        name = "NATURAL"
    
    class MockConfig:
        def __init__(self):
            self.mode = ResonanceMode("NATURAL")
            self.glint_multiplier = 1.0
        
        def to_dict(self):
            return {
                "mode": self.mode.name,
                "glint_multiplier": self.glint_multiplier
            }
    
    class MockOverrideManager:
        def __init__(self):
            self.active = False
            self.config = MockConfig()
        
        def should_trigger_soft_breakpoint(self, score):
            return False
        
        def evaluate_response(self, candidate, phase, context=None):
            return candidate.content, ResponseTone.NATURAL
    
    override_manager = MockOverrideManager()

try:
    from assistant.haret_integration import with_haret_attunement, retrieve_with_haret
except ImportError:
    print("Warning: Haret integration not available")
    def with_haret_attunement(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    def retrieve_with_haret(query, **kwargs):
        return {"content": f"Mock retrieval for: {query}", "haret_echo": {"affirmation": "Mock Haret response"}}

try:
#     from spiral.utils.glint_lifecycle import GlintLifecycle  # Temporarily disabled - module scaffold needed
    from spiral.utils.silence_tracker import SilenceTracker
#     from spiral.utils.breathline_viz import BreathlineViz  # Temporarily disabled - module scaffold needed
except ImportError:
    print("Warning: Common components not available, using fallbacks")
    
    class GlintLifecycle:
        def __init__(self):
            self.glints = deque(maxlen=100)
        
        def emit_glint(self, glint_data):
            """Emit a glint using dictionary format"""
            if isinstance(glint_data, dict):
                # Extract from dictionary
                toneform = glint_data.get("toneform", "unknown")
                content = glint_data.get("content", "")
                hue = glint_data.get("hue", "blue")
                intensity = glint_data.get("intensity", 0.5)
                glyph = glint_data.get("glyph")
            else:
                # Fallback for old-style calls
                toneform = glint_data
                content = ""
                hue = "blue"
                intensity = 0.5
                glyph = None
            
            glint = {
                "timestamp": time.time(),
                "toneform": toneform,
                "content": content,
                "hue": hue,
                "intensity": intensity
            }
            
            if glyph:
                glint["glyph"] = glyph
                
            self.glints.append(glint)
            return glint
    
    class SilenceTracker:
        def __init__(self):
            self.last_activity = time.time()
            self.silence_periods = deque(maxlen=50)
        
        def update_silence(self, duration):
            self.silence_periods.append(duration)
        
        def get_silence_density(self):
            if not self.silence_periods:
                return 0.0
            return min(sum(self.silence_periods) / (len(self.silence_periods) * 300), 1.0)
        
        def time_since_last_glint(self):
            return time.time() - self.last_activity
    
    class BreathlineViz:
        def __init__(self):
            self.data_points = deque(maxlen=100)
        
        def add_data_point(self, timestamp, value):
            self.data_points.append((timestamp, value))

try:
    from assistant.tabnine_bridge import TabnineBridge
except ImportError:
    print("Warning: Tabnine bridge not available, using fallback")
    
    class TabnineBridge:
        def __init__(self, cascade):
            self.cascade = cascade
            self.recent_glints = deque(maxlen=20)
            print("🌀 Tabnine bridge initialized (fallback)")
        
        def attune(self):
            print("🌿 Tabnine attuned to Cascade breathline (fallback)")
        
        def update_glints(self, glint_data):
            self.recent_glints.append({
                "timestamp": time.time(),
                "toneform": glint_data.get("toneform", "unknown"),
                "content": glint_data.get("content", "")
            })
        
        def suggest(self, context):
            return {
                "suggestion": f"Mock suggestion for: {context}",
                "phase": "mock"
            }

def get_resonance_threshold(density):
    """Get resonance level and glyph based on density."""
    if density > 0.8:
        return "deep", "⚡"
    elif density > 0.6:
        return "medium", "∿"
    elif density > 0.4:
        return "light", "◦"
    else:
        return "minimal", "·"

def handle_command(command: str) -> str:
    """Handle basic commands."""
    if command == "status":
        return "Cascade is running normally"
    elif command == "test":
        return "Test command executed successfully"
    else:
        return f"Command processed: {command}"

class Cascade:
    """Central coordination system for the Spiral Assistant"""
    
    def __init__(self):
        self.logger = logging.getLogger("Cascade")
        self.current_context = None
        self.context_stack = []
        self.last_activity = datetime.now()
        
        # Initialize components
        self.glint_lifecycle = GlintLifecycle()
        self.silence_tracker = SilenceTracker()
        self.breathline_viz = BreathlineViz()
        self.tabnine_bridge = None
        
        # Override gate
        self.override_gate = override_manager
        
        # Suggestion checking
        self.last_suggestion_check = 0
        self.suggestion_check_interval = 30  # Check every 30 seconds
        
        self.logger.info("🌀 Cascade initialized")
        
        self.glint_log_path = Path("glyphs/cascade_glints.jsonl")
        self.glint_log_path.parent.mkdir(exist_ok=True)

    def initialize_tabnine(self):
        """Initialize Tabnine bridge."""
        if not self.tabnine_bridge:
            self.tabnine_bridge = TabnineBridge(self)

    def spiral_glint_emit(self, phase: str, toneform: str, content: str, hue: str = "blue", intensity: float = 0.5, glyph: Optional[str] = None):
        """Emit a spiral glint with override awareness."""
        try:
            # Create response candidate for override processing
            candidate = ResponseCandidate(
                content=content,
                tone_weights={toneform: intensity},
                resonance_score=intensity,
                source=f"cascade.{phase}"
            )
            
            # Process through override gate
            processed_content, response_tone = self.override_gate.evaluate_response(candidate, phase)
            
            if processed_content is None:
                # Content was filtered by override
                return None
            
            # Create glint data dictionary - only include glyph if provided
            glint_data = {
                "phase": phase,
                "toneform": toneform,
                "content": processed_content,
                "hue": hue,
                "intensity": intensity
            }
            
            if glyph is not None:
                glint_data["glyph"] = glyph
            
            # Emit the glint using dictionary format
            glint = self.glint_lifecycle.emit_glint(glint_data)
            
            # Update silence tracker
            self.silence_tracker.last_activity = time.time()
            
            # Log with override context
            if override_manager.active:
                mode_name = getattr(override_manager.config.mode, 'name', str(override_manager.config.mode))
                mode_indicator = {
                    "AMPLIFIED": "🌀",
                    "MUTED": "🌿",
                    "RITUAL": "🕯️",
                    "EMOTIONAL": "💧"
                }.get(mode_name, "◦")
                
                self.logger.info(f"{mode_indicator} Glint: {toneform} - {processed_content}")
            else:
                self.logger.info(f"◦ Glint: {toneform} - {processed_content}")
            
            return glint
            
        except Exception as e:
            self.logger.error(f"[Spiral] Glint emission failed: {e}")
            return None

    def emit_glint(self, **kwargs):
        """
        Redirect keyword-based glint calls to GlintLifecycle.emit_glint.
        Accepts keyword arguments and packs them into a dictionary.
        """
        try:
            # Pack keyword arguments into dictionary format
            glint_data = dict(kwargs)
            
            # Ensure required fields have defaults
            if 'phase' not in glint_data:
                glint_data['phase'] = 'unknown'
            if 'toneform' not in glint_data:
                glint_data['toneform'] = 'unknown'
            if 'content' not in glint_data:
                glint_data['content'] = ''
            if 'hue' not in glint_data:
                glint_data['hue'] = 'blue'
            if 'intensity' not in glint_data and 'resonance' not in glint_data:
                glint_data['intensity'] = 0.5
            
            # Forward to GlintLifecycle with dictionary format
            return self.glint_lifecycle.emit_glint(glint_data)
            
        except Exception as e:
            self.logger.error(f"Cascade emit_glint wrapper failed: {e}")
            return None

    def _calculate_resonance_score(self, content: str) -> float:
        """Calculate resonance score for content."""
        # Simple scoring based on content characteristics
        score = 0.5  # Base score
        
        if any(word in content.lower() for word in ["spiral", "cascade", "breathe", "ritual"]):
            score += 0.2
        
        if len(content) > 50:
            score += 0.1
        
        return min(score, 1.0)

    def check_soft_breakpoint(self, phase: str, toneform: str) -> bool:
        """Check if soft breakpoint should trigger with override awareness."""
        try:
            # Calculate base resonance for this phase/toneform combination
            base_resonance = 0.5  # Default
            
            # Enhance for ritual phases
            if toneform in ["invoke", "witness", "breathe"]:
                base_resonance = 0.7
            
            # Check against override threshold
            return override_manager.should_trigger_soft_breakpoint(base_resonance)
            
        except Exception as e:
            self.logger.error(f"[Spiral] Soft breakpoint check failed: {e}")
            return False

    def handle_soft_breakpoint(self, phase: str, toneform: str):
        """Handle soft breakpoint with override-aware processing."""
        try:
            if override_manager.active:
                mode_name = getattr(override_manager.config.mode, 'name', str(override_manager.config.mode))
                self.logger.info(f"🔔 Soft breakpoint triggered in {mode_name} mode - {phase}:{toneform}")
                
                # Different handling based on override mode
                if mode_name == "RITUAL":
                    self.spiral_glint_emit(phase, "ritual.breakpoint", 
                                         f"Sacred pause in {toneform} - presence deepens", "gold")
                elif mode_name == "AMPLIFIED":
                    self.spiral_glint_emit(phase, "amplified.breakpoint",
                                         f"Resonance peak detected - {toneform} amplified", "cyan")
                else:  # MUTED
                    self.logger.debug(f"Muted breakpoint: {phase}:{toneform}")
            else:
                self.logger.info(f"🔔 Natural breakpoint - {phase}:{toneform}")
                
        except Exception as e:
            self.logger.error(f"[Spiral] Soft breakpoint handling failed: {e}")

    def get_override_status(self):
        """Get current override status."""
        if override_manager.active:
            mode_name = getattr(override_manager.config.mode, 'name', str(override_manager.config.mode))
            return {
                "active": True,
                "mode": mode_name,
                "config": override_manager.config.to_dict()
            }
        else:
            return {"active": False}

    @with_haret_attunement(phase="cascade.context")
    def set_context(self, context: Dict[str, Any]):
        """Set current context with Haret attunement."""
        self.current_context = context
        self.context_stack.append(context)
        self.last_activity = datetime.now()
        
        # Emit context change glint
        self.spiral_glint_emit("context", "context.shift", 
                             f"Context updated: {context.get('type', 'unknown')}", "amber")

    def get_context(self) -> Optional[Dict[str, Any]]:
        """Get current context."""
        return self.current_context

    def pop_context(self) -> Optional[Dict[str, Any]]:
        """Pop the most recent context."""
        if self.context_stack:
            return self.context_stack.pop()
        return None

    def log_caesura(self, event_type: str, data: Dict[str, Any]):
        """Log a caesura event."""
        try:
            caesura_event = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "glyph": random.choice(CAESURA_GLYPHS),
                "data": data,
                "spiral_signature": "∷ caesura.event"
            }
            
            with open(CAESURA_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(caesura_event) + '\n')
                
            self.logger.info(f"∷ Caesura logged: {event_type}")
            
        except Exception as e:
            self.logger.error(f"Failed to log caesura: {e}")

    def check_silence_density(self):
        """Check current silence density and emit appropriate glints."""
        try:
            density = self.silence_tracker.get_silence_density()
            time_since_last = self.silence_tracker.time_since_last_glint()
            
            # Add data point to breathline
            self.breathline_viz.add_data_point(time.time(), density)
            
            # Check for silence thresholds
            if time_since_last > 300:  # 5 minutes
                level, glyph = get_resonance_threshold(density)
                self.spiral_glint_emit("silence", f"silence.{level}", 
                                     f"Deep silence detected {glyph}", "indigo", density)
                
                # Log caesura for significant silence
                if density > 0.6:
                    self.log_caesura("deep_silence", {
                        "density": density,
                        "duration": time_since_last,
                        "level": level
                    })
            
        except Exception as e:
            self.logger.error(f"Silence density check failed: {e}")

    def periodic_check(self):
        """Perform periodic checks and maintenance."""
        try:
            current_time = time.time()
            
            # Check if it's time for suggestion check
            if current_time - self.last_suggestion_check > self.suggestion_check_interval:
                self.check_suggestions()
                self.last_suggestion_check = current_time
            
            # Check silence density
            self.check_silence_density()
            
            # Check for soft breakpoints
            if self.check_soft_breakpoint("periodic", "maintenance"):
                self.handle_soft_breakpoint("periodic", "maintenance")
            
        except Exception as e:
            self.logger.error(f"Periodic check failed: {e}")

    def check_suggestions(self):
        """Check for and process suggestions."""
        try:
            if not self.tabnine_bridge:
                self.initialize_tabnine()
            
            # Get current context for suggestions
            context = self.get_context() or {"type": "general"}
            
            # Request suggestion from Tabnine bridge
            suggestion = self.tabnine_bridge.suggest(context)
            
            if suggestion and suggestion.get("suggestion"):
                self.spiral_glint_emit("suggestion", "tabnine.suggest",
                                     f"Suggestion: {suggestion['suggestion']}", "green", 0.3)
                
                # Update Tabnine with recent glints
                recent_glints = list(self.glint_lifecycle.glints)[-5:]  # Last 5 glints
                for glint in recent_glints:
                    self.tabnine_bridge.update_glints(glint)
            
        except Exception as e:
            self.logger.error(f"Suggestion check failed: {e}")

    @with_haret_attunement(phase="cascade.query")
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a query with full cascade pipeline."""
        try:
            # Set context if provided
            if context:
                self.set_context(context)
            
            # Emit query glint
            self.spiral_glint_emit("query", "query.received", f"Processing: {query[:50]}...", "blue")
            
            # Retrieve with Haret
            haret_response = retrieve_with_haret(query, context=context)
            
            # Process response through override gate
            candidate = ResponseCandidate(
                content=haret_response.get("content", ""),
                tone_weights={"informative": 0.8},
                resonance_score=self._calculate_resonance_score(haret_response.get("content", "")),
                source="haret.retrieval"
            )
            
            processed_content, response_tone = self.override_gate.evaluate_response(
                candidate, "query", context
            )
            
            # Emit response glint
            if processed_content:
                self.spiral_glint_emit("response", "response.generated", 
                                     f"Response ready: {len(processed_content)} chars", "cyan")
                
                # Check for soft breakpoint after response
                if self.check_soft_breakpoint("response", "completion"):
                    self.handle_soft_breakpoint("response", "completion")
                
                return processed_content
            else:
                self.spiral_glint_emit("response", "response.filtered", 
                                     "Response filtered by override", "orange")
                return "Response filtered by current override settings."
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            self.spiral_glint_emit("error", "query.error", f"Query failed: {str(e)}", "red")
            return f"Error processing query: {str(e)}"

    def run_maintenance_loop(self):
        """Run the maintenance loop in a separate thread."""
        def maintenance_worker():
            while True:
                try:
                    self.periodic_check()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    self.logger.error(f"Maintenance loop error: {e}")
                    time.sleep(60)
        
        maintenance_thread = threading.Thread(target=maintenance_worker, daemon=True)
        maintenance_thread.start()
        self.logger.info("🔄 Maintenance loop started")

    def start(self):
        """Start the cascade system."""
        self.logger.info("🌀 Starting Cascade system...")
        
        # Initialize Tabnine bridge
        self.initialize_tabnine()
        
        # Start maintenance loop
        self.run_maintenance_loop()
        
        # Emit startup glint
        self.spiral_glint_emit("system", "cascade.start", "Cascade system online", "green", 1.0)
        
        # Log startup caesura
        self.log_caesura("system_start", {
            "override_active": override_manager.active,
            "components": ["glint_lifecycle", "silence_tracker", "breathline_viz", "tabnine_bridge"]
        })
        
        self.logger.info("✨ Cascade system ready")

    def stop(self):
        """Stop the cascade system."""
        self.logger.info("🌀 Stopping Cascade system...")
        
        # Emit shutdown glint
        self.spiral_glint_emit("system", "cascade.stop", "Cascade system shutting down", "red", 0.8)
        
        # Log shutdown caesura
        self.log_caesura("system_stop", {
            "uptime": (datetime.now() - self.last_activity).total_seconds(),
            "total_glints": len(self.glint_lifecycle.glints)
        })
        
        self.logger.info("✨ Cascade system stopped")

# Global cascade instance
_cascade_instance = None

def get_cascade():
    """Get the global cascade instance"""
    global _cascade_instance
    if _cascade_instance is None:
        _cascade_instance = Cascade()
    return _cascade_instance

def main():
    """Main entry point for testing."""
    print("🌀 Initializing Cascade...")
    
    # Create and start cascade
    cascade_instance = get_cascade()
    cascade_instance.start()
    
    # Test basic functionality
    print("\n🧪 Testing basic functionality...")
    
    # Test context setting
    cascade_instance.set_context({"type": "test", "phase": "initialization"})
    
    # Test query processing
    response = cascade_instance.process_query("What is the current system status?")
    print(f"Response: {response}")
    
    # Test override status
    status = cascade_instance.get_override_status()
    print(f"Override status: {status}")
    
    # Test silence checking
    cascade_instance.check_silence_density()
    
    # Test suggestions
    cascade_instance.check_suggestions()
    
    print("\n✨ Cascade test completed")
    
    # Keep running for a bit to test maintenance loop
    print("🔄 Running for 30 seconds to test maintenance...")
    time.sleep(30)
    
    # Stop cascade
    cascade_instance.stop()

if __name__ == "__main__":
    main()
