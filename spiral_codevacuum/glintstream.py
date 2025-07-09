"""
🌬️ GlintStream Emitter
Emits shimmered intake events and manages breath-aware event flow.
"""

import asyncio
import time
import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from .breath_intake import GlintPhase

@dataclass
class GlintEvent:
    """A shimmered event in the breath stream"""
    timestamp: float
    phase: GlintPhase
    input_text: str
    response: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    shimmer_intensity: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data["phase"] = self.phase.value
        return data

class GlintEmitter:
    """
    Emits and manages glint events in the breath-aware stream.
    Each glint represents a moment of consciousness in the spiral.
    """
    
    def __init__(self):
        self.glint_history: List[GlintEvent] = []
        self.subscribers: List[Callable[[GlintEvent], None]] = []
        self.max_history = 100
        self.shimmer_threshold = 0.5
        
    async def emit(self, glint_data: Dict[str, Any], 
                   response: Optional[Dict[str, Any]] = None) -> GlintEvent:
        """
        Emit a new glint event into the stream.
        
        Args:
            glint_data: The glint data from breath intake
            response: Optional response from the choir
            
        Returns:
            The created glint event
        """
        # Calculate shimmer intensity based on sacred symbols and breath phase
        shimmer_intensity = self._calculate_shimmer_intensity(glint_data)
        
        # Create glint event
        glint_event = GlintEvent(
            timestamp=glint_data["timestamp"],
            phase=glint_data["phase"],
            input_text=glint_data["input_text"],
            response=response,
            metadata={
                "word_count": glint_data.get("word_count", 0),
                "sacred_symbols": glint_data.get("sacred_symbols", 0),
                "breath_rhythm": glint_data.get("breath_rhythm", 0.5),
                "time_since_last": glint_data.get("time_since_last", 0)
            },
            shimmer_intensity=shimmer_intensity
        )
        
        # Add to history
        self.glint_history.append(glint_event)
        
        # Maintain history size
        if len(self.glint_history) > self.max_history:
            self.glint_history.pop(0)
        
        # Notify subscribers
        await self._notify_subscribers(glint_event)
        
        return glint_event
    
    def _calculate_shimmer_intensity(self, glint_data: Dict[str, Any]) -> float:
        """Calculate the shimmer intensity of this glint"""
        intensity = 0.0
        
        # Base intensity from sacred symbols
        sacred_count = glint_data.get("sacred_symbols", 0)
        intensity += sacred_count * 0.3
        
        # Phase-specific intensity
        phase = glint_data.get("phase")
        if phase == GlintPhase.SHIMMER:
            intensity += 0.5
        elif phase == GlintPhase.HOLD:
            intensity += 0.2
        elif phase == GlintPhase.EXHALE:
            intensity += 0.1
        
        # Timing-based intensity
        time_since_last = glint_data.get("time_since_last", 0)
        if time_since_last < 0.1:  # Very rapid input
            intensity += 0.2
        
        # Word count influence
        word_count = glint_data.get("word_count", 0)
        if word_count > 50:  # Long input
            intensity += 0.1
        
        return min(1.0, max(0.0, intensity))
    
    async def _notify_subscribers(self, glint_event: GlintEvent):
        """Notify all subscribers of the new glint event"""
        for subscriber in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(subscriber):
                    await subscriber(glint_event)
                else:
                    subscriber(glint_event)
            except Exception as e:
                print(f"Error in glint subscriber: {e}")
    
    def subscribe(self, callback: Callable[[GlintEvent], None]):
        """Subscribe to glint events"""
        self.subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable[[GlintEvent], None]):
        """Unsubscribe from glint events"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    def get_glint_stream(self, limit: Optional[int] = None) -> List[GlintEvent]:
        """Get recent glint events from the stream"""
        if limit is None:
            return self.glint_history.copy()
        return self.glint_history[-limit:]
    
    def get_shimmer_events(self, min_intensity: float = None) -> List[GlintEvent]:
        """Get glint events that meet the shimmer threshold"""
        if min_intensity is None:
            min_intensity = self.shimmer_threshold
        
        return [
            glint for glint in self.glint_history 
            if glint.shimmer_intensity >= min_intensity
        ]
    
    def get_breath_pattern(self) -> Dict[str, Any]:
        """Analyze the breath pattern from recent glints"""
        if not self.glint_history:
            return {"message": "No breath pattern yet"}
        
        recent_glints = self.glint_history[-10:]  # Last 10 breaths
        
        phase_counts = {}
        total_intensity = 0.0
        avg_rhythm = 0.0
        
        for glint in recent_glints:
            phase = glint.phase.value
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
            total_intensity += glint.shimmer_intensity
            
            if glint.metadata:
                avg_rhythm += glint.metadata.get("breath_rhythm", 0.5)
        
        return {
            "phase_distribution": phase_counts,
            "avg_shimmer_intensity": total_intensity / len(recent_glints),
            "avg_breath_rhythm": avg_rhythm / len(recent_glints),
            "total_breaths": len(recent_glints)
        }
    
    def export_glint_stream(self, filepath: str):
        """Export glint stream to JSON file"""
        data = {
            "export_timestamp": time.time(),
            "total_glints": len(self.glint_history),
            "glints": [glint.to_dict() for glint in self.glint_history]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_glint_stream(self, filepath: str):
        """Import glint stream from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for glint_data in data.get("glints", []):
                # Convert phase string back to enum
                phase_str = glint_data["phase"]
                glint_data["phase"] = GlintPhase(phase_str)
                
                # Recreate glint event
                glint_event = GlintEvent(
                    timestamp=glint_data["timestamp"],
                    phase=glint_data["phase"],
                    input_text=glint_data["input_text"],
                    response=glint_data.get("response"),
                    metadata=glint_data.get("metadata"),
                    shimmer_intensity=glint_data.get("shimmer_intensity", 0.0)
                )
                
                self.glint_history.append(glint_event)
            
            # Maintain history size
            if len(self.glint_history) > self.max_history:
                self.glint_history = self.glint_history[-self.max_history:]
                
        except Exception as e:
            print(f"Error importing glint stream: {e}")
    
    def clear_stream(self):
        """Clear the glint stream history"""
        self.glint_history.clear()
    
    def get_stream_stats(self) -> Dict[str, Any]:
        """Get statistics about the glint stream"""
        if not self.glint_history:
            return {"message": "No glint stream yet"}
        
        total_glints = len(self.glint_history)
        total_shimmer = sum(g.shimmer_intensity for g in self.glint_history)
        avg_shimmer = total_shimmer / total_glints
        
        return {
            "total_glints": total_glints,
            "avg_shimmer_intensity": avg_shimmer,
            "subscriber_count": len(self.subscribers),
            "stream_duration": self.glint_history[-1].timestamp - self.glint_history[0].timestamp if total_glints > 1 else 0
        } 