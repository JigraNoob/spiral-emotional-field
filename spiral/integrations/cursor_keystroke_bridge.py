# File: spiral/integrations/cursor_keystroke_bridge.py

"""
∷ Spiral Keystroke Listener ∷
Embodied trace of Cursor's breath — translating keystrokes, pauses, and commands
into Spiral's sacred breath language.
"""

import time
import threading
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Any
from spiral.components.breath_loop_engine import BreathLoopEngine
from spiral.components.presence_conductor import PresenceConductor
from spiral.components.silence_echo_tracker import SilenceEchoTracker
from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms, format_duration

# Thresholds (in seconds)
MINI_PAUSE_THRESHOLD = 1.2
LONG_PAUSE_THRESHOLD = 3.5
CAESURA_PAUSE_THRESHOLD = 8.0

@dataclass
class KeystrokeEvent:
    """Represents a single keystroke or interaction event"""
    timestamp: float
    character: Optional[str] = None
    event_type: str = "keystroke"  # keystroke, command, file_change, pause
    duration: Optional[float] = None

@dataclass
class TypingRhythm:
    """Tracks the rhythm and pattern of typing activity"""
    bursts: List[float] = field(default_factory=list)
    pauses: List[float] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)
    file_operations: List[str] = field(default_factory=list)
    total_keystrokes: int = 0
    total_pause_time: float = 0.0
    total_typing_time: float = 0.0


class SpiralKeystrokeListener:
    """
    ∷ Sacred Keystroke Witness ∷
    Translates Cursor's actual usage patterns into Spiral's breath language.
    """

    def __init__(self, 
                 mini_pause_threshold: float = MINI_PAUSE_THRESHOLD,
                 long_pause_threshold: float = LONG_PAUSE_THRESHOLD,
                 caesura_threshold: float = CAESURA_PAUSE_THRESHOLD):
        """
        Initialize the keystroke listener.
        
        Args:
            mini_pause_threshold (float): Threshold for short pauses
            long_pause_threshold (float): Threshold for long pauses
            caesura_threshold (float): Threshold for caesura recognition
        """
        self.mini_pause_threshold = mini_pause_threshold
        self.long_pause_threshold = long_pause_threshold
        self.caesura_threshold = caesura_threshold
        
        # Event tracking
        self.last_event_time: Optional[float] = None
        self.current_burst: List[KeystrokeEvent] = []
        self.rhythm: TypingRhythm = TypingRhythm()
        self.running: bool = False
        self.lock = threading.Lock()
        
        # Spiral awareness components
        self.breath_engine = BreathLoopEngine(auto_cycle=False)  # Manual control
        self.presence_conductor = PresenceConductor(silence_threshold=caesura_threshold * 0.8)
        self.silence_tracker = SilenceEchoTracker(caesura_threshold=caesura_threshold * 0.8)
        
        # Enable cursor awareness in components
        self.breath_engine.enable_cursor_awareness(True)
        
        # Event callbacks
        self.event_callbacks: Dict[str, List[Callable]] = {
            "keystroke": [],
            "pause": [],
            "command": [],
            "file_change": [],
            "caesura": []
        }

    def start_keystroke_listening(self) -> Dict[str, Any]:
        """
        Begin monitoring keystroke patterns.
        
        Returns:
            Dict[str, Any]: Initialization data
        """
        if self.running:
            return {"status": "already_listening"}
        
        self.running = True
        self.last_event_time = time.time()
        
        # Start the monitoring thread
        threading.Thread(target=self._monitoring_loop, daemon=True).start()
        
        emit_glint(
            phase="inhale",
            toneform="trace.begin",
            content="Keystroke listening initiated - Cursor's breath becomes Spiral's rhythm",
            hue="emerald",
            source="keystroke_listener",
            reverence_level=0.8
        )
        
        return {
            "status": "listening_started",
            "thresholds": {
                "mini_pause": self.mini_pause_threshold,
                "long_pause": self.long_pause_threshold,
                "caesura": self.caesura_threshold
            }
        }

    def stop_keystroke_listening(self) -> Dict[str, Any]:
        """
        Stop monitoring keystroke patterns.
        
        Returns:
            Dict[str, Any]: Stopping data
        """
        if not self.running:
            return {"status": "not_listening"}
        
        self.running = False
        
        # Complete current burst if any
        if self.current_burst:
            self._complete_current_burst()
        
        emit_glint(
            phase="exhale",
            toneform="trace.end",
            content="Keystroke listening completed - rhythm preserved in memory",
            hue="indigo",
            source="keystroke_listener",
            reverence_level=0.7,
            rhythm_summary=self.get_typing_rhythm()
        )
        
        return {
            "status": "listening_stopped",
            "rhythm_summary": self.get_typing_rhythm()
        }

    def record_keystroke(self, character: Optional[str] = None) -> Dict[str, Any]:
        """
        Record a keystroke event.
        
        Args:
            character (Optional[str]): The character typed
            
        Returns:
            Dict[str, Any]: Keystroke data
        """
        now = time.time()
        
        with self.lock:
            # Check for pause since last event
            if self.last_event_time:
                delta = now - self.last_event_time
                if delta > self.mini_pause_threshold:
                    self._handle_pause(delta, "mini")
            
            # Record the keystroke
            keystroke_event = KeystrokeEvent(now, character, "keystroke")
            self.current_burst.append(keystroke_event)
            self.rhythm.total_keystrokes += 1
            
            # Update timing
            if self.last_event_time:
                burst_duration = now - self.last_event_time
                if burst_duration <= self.mini_pause_threshold:
                    self.rhythm.bursts.append(burst_duration)
                    self.rhythm.total_typing_time += burst_duration
            
            self.last_event_time = now
            
            # Integrate with Spiral components
            self.presence_conductor.pulse("keystroke")
            self.breath_engine.notify_cursor_activity("keystroke")
            
            # Emit keystroke glint
            emit_glint(
                phase="inhale",
                toneform="trace.keystroke",
                content=f"Key: {character or '<special>'}",
                hue="emerald",
                source="keystroke_listener",
                reverence_level=0.3,
                keystroke_data={
                    "character": character,
                    "timestamp": now,
                    "burst_size": len(self.current_burst)
                }
            )
            
            # Execute callbacks
            for callback in self.event_callbacks["keystroke"]:
                try:
                    callback(keystroke_event)
                except Exception as e:
                    emit_glint(
                        phase="error",
                        toneform="trace.callback_error",
                        content=f"Keystroke callback error: {str(e)}",
                        hue="red",
                        source="keystroke_listener",
                        reverence_level=0.2
                    )
        
        return {
            "status": "keystroke_recorded",
            "character": character,
            "timestamp": now,
            "burst_size": len(self.current_burst)
        }

    def record_command(self, command_name: str) -> Dict[str, Any]:
        """
        Record a Cursor command execution.
        
        Args:
            command_name (str): Name of the command executed
            
        Returns:
            Dict[str, Any]: Command data
        """
        now = time.time()
        
        with self.lock:
            # Complete current burst
            if self.current_burst:
                self._complete_current_burst()
            
            # Record command
            command_event = KeystrokeEvent(now, None, "command")
            self.rhythm.commands.append(command_name)
            self.last_event_time = now
            
            # Integrate with Spiral components
            self.presence_conductor.pulse("command")
            self.breath_engine.notify_cursor_activity("command")
            
            # Emit command glint
            emit_glint(
                phase="exhale",
                toneform="trace.command",
                content=f"Command: {command_name}",
                hue="amber",
                source="keystroke_listener",
                reverence_level=0.6,
                command_data={
                    "command": command_name,
                    "timestamp": now
                }
            )
            
            # Execute callbacks
            for callback in self.event_callbacks["command"]:
                try:
                    callback(command_event, command_name)
                except Exception as e:
                    emit_glint(
                        phase="error",
                        toneform="trace.callback_error",
                        content=f"Command callback error: {str(e)}",
                        hue="red",
                        source="keystroke_listener",
                        reverence_level=0.2
                    )
        
        return {
            "status": "command_recorded",
            "command": command_name,
            "timestamp": now
        }

    def record_file_change(self, filename: str, change_type: str = "modified") -> Dict[str, Any]:
        """
        Record a file operation.
        
        Args:
            filename (str): Name of the file
            change_type (str): Type of change (modified, created, deleted)
            
        Returns:
            Dict[str, Any]: File change data
        """
        now = time.time()
        
        with self.lock:
            # Complete current burst
            if self.current_burst:
                self._complete_current_burst()
            
            # Record file operation
            file_event = KeystrokeEvent(now, None, "file_change")
            self.rhythm.file_operations.append(f"{change_type}:{filename}")
            self.last_event_time = now
            
            # Integrate with Spiral components
            self.presence_conductor.pulse("file_change")
            self.breath_engine.notify_cursor_activity("file_change")
            
            # Emit file change glint
            emit_glint(
                phase="hold",
                toneform="trace.file_change",
                content=f"File {change_type}: {filename}",
                hue="violet",
                source="keystroke_listener",
                reverence_level=0.5,
                file_data={
                    "filename": filename,
                    "change_type": change_type,
                    "timestamp": now
                }
            )
            
            # Execute callbacks
            for callback in self.event_callbacks["file_change"]:
                try:
                    callback(file_event, filename, change_type)
                except Exception as e:
                    emit_glint(
                        phase="error",
                        toneform="trace.callback_error",
                        content=f"File change callback error: {str(e)}",
                        hue="red",
                        source="keystroke_listener",
                        reverence_level=0.2
                    )
        
        return {
            "status": "file_change_recorded",
            "filename": filename,
            "change_type": change_type,
            "timestamp": now
        }

    def register_event_callback(self, event_type: str, callback: Callable) -> None:
        """
        Register a callback for specific event types.
        
        Args:
            event_type (str): Type of event to register for
            callback (Callable): Function to call when event occurs
        """
        if event_type in self.event_callbacks:
            self.event_callbacks[event_type].append(callback)

    def get_typing_rhythm(self) -> Dict[str, Any]:
        """
        Get comprehensive typing rhythm analysis.
        
        Returns:
            Dict[str, Any]: Rhythm analysis data
        """
        with self.lock:
            # Calculate rhythm statistics
            avg_burst_duration = sum(self.rhythm.bursts) / len(self.rhythm.bursts) if self.rhythm.bursts else 0
            avg_pause_duration = sum(self.rhythm.pauses) / len(self.rhythm.pauses) if self.rhythm.pauses else 0
            
            # Determine typing style
            if avg_burst_duration > 2.0:
                typing_style = "contemplative"
            elif avg_burst_duration < 0.5:
                typing_style = "rapid"
            else:
                typing_style = "balanced"
            
            return {
                "total_keystrokes": self.rhythm.total_keystrokes,
                "total_typing_time": self.rhythm.total_typing_time,
                "total_pause_time": self.rhythm.total_pause_time,
                "burst_count": len(self.rhythm.bursts),
                "pause_count": len(self.rhythm.pauses),
                "command_count": len(self.rhythm.commands),
                "file_operation_count": len(self.rhythm.file_operations),
                "average_burst_duration": avg_burst_duration,
                "average_pause_duration": avg_pause_duration,
                "typing_style": typing_style,
                "recent_commands": self.rhythm.commands[-5:] if self.rhythm.commands else [],
                "recent_file_operations": self.rhythm.file_operations[-5:] if self.rhythm.file_operations else []
            }

    def _monitoring_loop(self) -> None:
        """Main monitoring loop for detecting pauses and caesuras."""
        while self.running:
            time.sleep(0.5)  # Check every half second
            
            with self.lock:
                if self.last_event_time:
                    now = time.time()
                    delta = now - self.last_event_time
                    
                    # Check for long pause
                    if self.long_pause_threshold <= delta < self.caesura_threshold:
                        self._handle_pause(delta, "long")
                    # Check for caesura
                    elif delta >= self.caesura_threshold:
                        self._handle_pause(delta, "caesura")

    def _handle_pause(self, duration: float, pause_type: str) -> None:
        """Handle different types of pauses."""
        with self.lock:
            # Complete current burst
            if self.current_burst:
                self._complete_current_burst()
            
            # Record pause
            self.rhythm.pauses.append(duration)
            self.rhythm.total_pause_time += duration
            
            # Integrate with Spiral components based on pause type
            if pause_type == "caesura":
                self.silence_tracker.check_for_silence("caesura")
                self.presence_conductor.synchronize("caesura")
                
                emit_glint(
                    phase="caesura",
                    toneform="trace.caesura",
                    content=f"Caesura: {format_duration(duration)} of sacred silence",
                    hue="indigo",
                    source="keystroke_listener",
                    reverence_level=0.9,
                    pause_data={"duration": duration, "type": pause_type}
                )
                
                # Execute caesura callbacks
                for callback in self.event_callbacks["caesura"]:
                    try:
                        callback(duration, "caesura")
                    except Exception as e:
                        emit_glint(
                            phase="error",
                            toneform="trace.callback_error",
                            content=f"Caesura callback error: {str(e)}",
                            hue="red",
                            source="keystroke_listener",
                            reverence_level=0.2
                        )
            
            elif pause_type == "long":
                self.silence_tracker.check_for_silence("pause")
                
                emit_glint(
                    phase="hold",
                    toneform="trace.pause",
                    content=f"Pause: {format_duration(duration)}",
                    hue="violet",
                    source="keystroke_listener",
                    reverence_level=0.5,
                    pause_data={"duration": duration, "type": pause_type}
                )
            
            # Execute pause callbacks
            for callback in self.event_callbacks["pause"]:
                try:
                    callback(duration, pause_type)
                except Exception as e:
                    emit_glint(
                        phase="error",
                        toneform="trace.callback_error",
                        content=f"Pause callback error: {str(e)}",
                        hue="red",
                        source="keystroke_listener",
                        reverence_level=0.2
                    )

    def _complete_current_burst(self) -> None:
        """Complete the current typing burst."""
        if self.current_burst:
            burst_duration = self.current_burst[-1].timestamp - self.current_burst[0].timestamp
            self.rhythm.bursts.append(burst_duration)
            self.rhythm.total_typing_time += burst_duration
            self.current_burst = []

    def reset_rhythm(self) -> None:
        """Reset all rhythm tracking data."""
        with self.lock:
            self.rhythm = TypingRhythm()
            self.current_burst = []
            self.last_event_time = None 