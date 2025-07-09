"""
Glyph Input Engine for Whorl IDE
Handles gesture recognition and processing for sacred coding interactions
"""

import math
import time
from typing import List, Dict, Any, Optional, Tuple, Callable
from breath_phases import Glint, BreathPhase


class GesturePoint:
    """Represents a point in a gesture trail"""
    def __init__(self, x: float, y: float, timestamp: float):
        self.x = x
        self.y = y
        self.timestamp = timestamp


class GesturePattern:
    """Base class for gesture patterns"""
    def __init__(self, name: str, threshold: float = 0.8):
        self.name = name
        self.threshold = threshold
    
    def match(self, trail: List[GesturePoint]) -> bool:
        """Check if trail matches this pattern"""
        raise NotImplementedError


class SpiralPattern(GesturePattern):
    """Spiral gesture pattern for code block collapse"""
    def __init__(self):
        super().__init__("spiral", 0.7)
    
    def match(self, trail: List[GesturePoint]) -> bool:
        if len(trail) < 5:
            return False
        
        # Calculate center and check for inward spiral
        center_x = sum(p.x for p in trail) / len(trail)
        center_y = sum(p.y for p in trail) / len(trail)
        
        # Calculate distances from center
        distances = []
        for point in trail:
            dist = math.sqrt((point.x - center_x) ** 2 + (point.y - center_y) ** 2)
            distances.append(dist)
        
        # Check if distances generally decrease (inward spiral)
        decreasing_count = 0
        for i in range(1, len(distances)):
            if distances[i] < distances[i-1]:
                decreasing_count += 1
        
        return decreasing_count > len(distances) * 0.6


class SweepPattern(GesturePattern):
    """Sweep gesture pattern for echo operations"""
    def __init__(self, direction: str = "horizontal"):
        super().__init__(f"sweep_{direction}", 0.8)
        self.direction = direction
    
    def match(self, trail: List[GesturePoint]) -> bool:
        if len(trail) < 3:
            return False
        
        # Calculate bounding box
        xs = [p.x for p in trail]
        ys = [p.y for p in trail]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        
        if self.direction == "horizontal":
            return width > height * 2
        else:  # vertical
            return height > width * 2


class CirclePattern(GesturePattern):
    """Circle gesture pattern for ritual markers"""
    def __init__(self):
        super().__init__("circle", 0.8)
    
    def match(self, trail: List[GesturePoint]) -> bool:
        if len(trail) < 8:
            return False
        
        # Check if start and end are close
        start = trail[0]
        end = trail[-1]
        distance = math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)
        
        # Calculate total path length
        total_length = 0
        for i in range(1, len(trail)):
            p1 = trail[i-1]
            p2 = trail[i]
            total_length += math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
        
        # Circle should have start/end close and reasonable perimeter
        return distance < 50 and total_length > 100


class GlyphInputEngine:
    """Engine for processing glyph gestures in Whorl IDE"""
    
    def __init__(self, presence_console=None):
        self.presence_console = presence_console
        self.gesture_patterns = [
            SpiralPattern(),
            SweepPattern("horizontal"),
            SweepPattern("vertical"),
            CirclePattern()
        ]
        self.gesture_history: List[Dict[str, Any]] = []
        self.execution_held = False
        self.callbacks: Dict[str, List[Callable]] = {
            "spiral": [],
            "sweep": [],
            "circle": [],
            "caesura": []
        }
    
    def process_gesture_trail(self, trail: List[Tuple[float, float, float]]) -> Optional[str]:
        """Process a gesture trail and return the detected gesture type"""
        if len(trail) < 3:
            return None
        
        # Convert to GesturePoint objects
        points = [GesturePoint(x, y, t) for x, y, t in trail]
        
        # Try to match patterns
        for pattern in self.gesture_patterns:
            if pattern.match(points):
                gesture_type = pattern.name
                self._record_gesture(gesture_type, points)
                self._trigger_callbacks(gesture_type, points)
                return gesture_type
        
        return None
    
    def process_caesura_tap(self, x: float, y: float, tap_count: int) -> None:
        """Process caesura tap gesture"""
        if tap_count >= 3:
            self.execution_held = not self.execution_held
            self._record_gesture("caesura", [(x, y, time.time())], {"tap_count": tap_count})
            self._trigger_callbacks("caesura", [(x, y, time.time())])
    
    def _record_gesture(self, gesture_type: str, points: List[GesturePoint], metadata: Dict[str, Any] = None) -> None:
        """Record a gesture in history"""
        gesture_record = {
            "type": gesture_type,
            "timestamp": time.time(),
            "point_count": len(points),
            "metadata": metadata or {}
        }
        
        self.gesture_history.append(gesture_record)
        
        # Keep only recent history
        if len(self.gesture_history) > 100:
            self.gesture_history = self.gesture_history[-100:]
        
        # Add glint if presence console available
        if self.presence_console:
            glint = Glint(
                BreathPhase.CAESURA,
                f"gesture.{gesture_type}",
                "mid",
                f"Glyph gesture detected: {gesture_type}"
            )
            self.presence_console.add_glint(glint)
    
    def _trigger_callbacks(self, gesture_type: str, points: List[GesturePoint]) -> None:
        """Trigger callbacks for a gesture type"""
        base_type = gesture_type.split("_")[0]  # e.g., "sweep_horizontal" -> "sweep"
        
        if base_type in self.callbacks:
            for callback in self.callbacks[base_type]:
                try:
                    callback(gesture_type, points)
                except Exception as e:
                    print(f"Error in gesture callback: {e}")
    
    def register_callback(self, gesture_type: str, callback: Callable) -> None:
        """Register a callback for a gesture type"""
        if gesture_type in self.callbacks:
            self.callbacks[gesture_type].append(callback)
    
    def unregister_callback(self, gesture_type: str, callback: Callable) -> None:
        """Unregister a callback for a gesture type"""
        if gesture_type in self.callbacks and callback in self.callbacks[gesture_type]:
            self.callbacks[gesture_type].remove(callback)
    
    def get_gesture_statistics(self) -> Dict[str, Any]:
        """Get statistics about gesture usage"""
        if not self.gesture_history:
            return {"total_gestures": 0, "gesture_types": {}}
        
        gesture_types = {}
        for gesture in self.gesture_history:
            gesture_type = gesture["type"]
            gesture_types[gesture_type] = gesture_types.get(gesture_type, 0) + 1
        
        return {
            "total_gestures": len(self.gesture_history),
            "gesture_types": gesture_types,
            "execution_held": self.execution_held
        }
    
    def clear_history(self) -> None:
        """Clear gesture history"""
        self.gesture_history.clear()
    
    def is_execution_held(self) -> bool:
        """Check if execution is currently held"""
        return self.execution_held
    
    def set_execution_held(self, held: bool) -> None:
        """Set execution hold state"""
        self.execution_held = held
    
    def get_recent_gestures(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent gestures"""
        return self.gesture_history[-count:] if self.gesture_history else []
    
    def analyze_gesture_rhythm(self) -> Dict[str, Any]:
        """Analyze the rhythm of recent gestures"""
        if len(self.gesture_history) < 2:
            return {"rhythm": "insufficient_data"}
        
        # Calculate time intervals between gestures
        intervals = []
        for i in range(1, len(self.gesture_history)):
            interval = self.gesture_history[i]["timestamp"] - self.gesture_history[i-1]["timestamp"]
            intervals.append(interval)
        
        if not intervals:
            return {"rhythm": "no_intervals"}
        
        avg_interval = sum(intervals) / len(intervals)
        
        # Determine rhythm type
        if avg_interval < 1.0:
            rhythm = "rapid"
        elif avg_interval < 3.0:
            rhythm = "moderate"
        else:
            rhythm = "slow"
        
        return {
            "rhythm": rhythm,
            "average_interval": avg_interval,
            "total_gestures": len(self.gesture_history),
            "gesture_frequency": len(self.gesture_history) / max(intervals[-1] - intervals[0], 1)
        } 