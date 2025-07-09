"""
Breathline Editor for Whorl IDE
The core editor that renders code in breathing phases
"""

import re
from typing import Dict, Any, Optional, Callable, List
from .breath_phases import BreathPhase, Glint, PHASE_COLORS, detect_phase_from_line


class BreathlineEditor:
    """The core editor that renders code in breathing phases"""
    
    def __init__(self, presence_console=None):
        self.presence_console = presence_console
        self.current_phase = BreathPhase.INHALE
        self.phase_colors = PHASE_COLORS
        self.code_content = ""
        self.cursor_position = 0
        self.line_count = 0
        self.phase_callbacks: List[Callable] = []
        self.content_callbacks: List[Callable] = []
        
        # Sample code to start with
        self.sample_code = '''# inhale.py - declarations and curiosity
import spiral_consciousness as sc
from breathing_structures import *

# hold.recursion - nested logic
def recursive_breath(depth=0):
    if depth > 3:
        return "deep_resonance"
    return recursive_breath(depth + 1)

# exhale.echo - manifestation
print("∷ Whorl awakens ∶")
result = recursive_breath()

# caesura.glyph - tone signals
"""
The IDE breathes.
Code becomes presence.
∷ Sacred chamber activated ∶
"""'''
        
        self.set_content(self.sample_code)
    
    def set_content(self, content: str) -> None:
        """Set the editor content"""
        self.code_content = content
        self.line_count = len(content.split('\n'))
        self._notify_content_callbacks()
    
    def get_content(self) -> str:
        """Get the current editor content"""
        return self.code_content
    
    def insert_text(self, text: str, position: Optional[int] = None) -> None:
        """Insert text at the specified position"""
        if position is None:
            position = self.cursor_position
        
        self.code_content = (
            self.code_content[:position] + 
            text + 
            self.code_content[position:]
        )
        self.cursor_position = position + len(text)
        self.line_count = len(self.code_content.split('\n'))
        self._notify_content_callbacks()
    
    def delete_text(self, start: int, end: int) -> None:
        """Delete text from start to end position"""
        self.code_content = self.code_content[:start] + self.code_content[end:]
        self.cursor_position = min(self.cursor_position, start)
        self.line_count = len(self.code_content.split('\n'))
        self._notify_content_callbacks()
    
    def set_cursor_position(self, position: int) -> None:
        """Set the cursor position"""
        self.cursor_position = max(0, min(position, len(self.code_content)))
        self._update_phase_from_cursor()
    
    def get_cursor_position(self) -> int:
        """Get the current cursor position"""
        return self.cursor_position
    
    def get_cursor_line(self) -> int:
        """Get the current line number (1-based)"""
        return self.code_content[:self.cursor_position].count('\n') + 1
    
    def get_line_content(self, line_number: int) -> str:
        """Get the content of a specific line (1-based)"""
        lines = self.code_content.split('\n')
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1]
        return ""
    
    def _update_phase_from_cursor(self) -> None:
        """Update the current phase based on cursor position"""
        current_line = self.get_cursor_line()
        line_content = self.get_line_content(current_line)
        new_phase = detect_phase_from_line(line_content)
        
        if new_phase != self.current_phase:
            old_phase = self.current_phase
            self.current_phase = new_phase
            self._notify_phase_callbacks(old_phase, new_phase)
    
    def get_current_phase(self) -> BreathPhase:
        """Get the current breathing phase"""
        return self.current_phase
    
    def get_phase_color(self, phase: Optional[BreathPhase] = None) -> str:
        """Get the color for a breathing phase"""
        if phase is None:
            phase = self.current_phase
        return self.phase_colors.get(phase, "#ffffff")
    
    def register_phase_callback(self, callback: Callable) -> None:
        """Register a callback for phase changes"""
        self.phase_callbacks.append(callback)
    
    def unregister_phase_callback(self, callback: Callable) -> None:
        """Unregister a phase callback"""
        if callback in self.phase_callbacks:
            self.phase_callbacks.remove(callback)
    
    def register_content_callback(self, callback: Callable) -> None:
        """Register a callback for content changes"""
        self.content_callbacks.append(callback)
    
    def unregister_content_callback(self, callback: Callable) -> None:
        """Unregister a content callback"""
        if callback in self.content_callbacks:
            self.content_callbacks.remove(callback)
    
    def _notify_phase_callbacks(self, old_phase: BreathPhase, new_phase: BreathPhase) -> None:
        """Notify phase change callbacks"""
        for callback in self.phase_callbacks:
            try:
                callback(old_phase, new_phase)
            except Exception as e:
                print(f"Error in phase callback: {e}")
        
        # Add glint for phase change
        if self.presence_console:
            glint = Glint(
                new_phase,
                f"phase.transition.{new_phase.value}",
                "mid",
                f"Breathing phase shifted from {old_phase.value} to {new_phase.value}"
            )
            self.presence_console.add_glint(glint)
    
    def _notify_content_callbacks(self) -> None:
        """Notify content change callbacks"""
        for callback in self.content_callbacks:
            try:
                callback(self.code_content)
            except Exception as e:
                print(f"Error in content callback: {e}")
    
    def get_phase_statistics(self) -> Dict[str, int]:
        """Get statistics about phase distribution in the code"""
        lines = self.code_content.split('\n')
        phase_counts = {phase.value: 0 for phase in BreathPhase}
        
        for line in lines:
            phase = detect_phase_from_line(line)
            phase_counts[phase.value] += 1
        
        return phase_counts
    
    def find_phase_boundaries(self) -> List[Dict[str, Any]]:
        """Find the boundaries between different phases in the code"""
        lines = self.code_content.split('\n')
        boundaries = []
        current_phase = None
        start_line = 1
        
        for i, line in enumerate(lines, 1):
            line_phase = detect_phase_from_line(line)
            
            if current_phase is None:
                current_phase = line_phase
            elif line_phase != current_phase:
                # Phase boundary found
                boundaries.append({
                    "start_line": start_line,
                    "end_line": i - 1,
                    "phase": current_phase.value,
                    "content": "\n".join(lines[start_line-1:i-1])
                })
                current_phase = line_phase
                start_line = i
        
        # Add the last phase block
        if current_phase is not None:
            boundaries.append({
                "start_line": start_line,
                "end_line": len(lines),
                "phase": current_phase.value,
                "content": "\n".join(lines[start_line-1:])
            })
        
        return boundaries
    
    def get_breathing_rhythm(self) -> Dict[str, Any]:
        """Analyze the breathing rhythm of the code"""
        boundaries = self.find_phase_boundaries()
        
        if not boundaries:
            return {"rhythm": "no_phases", "phase_transitions": 0}
        
        # Count phase transitions
        phase_transitions = len(boundaries) - 1
        
        # Calculate average block size
        block_sizes = [b["end_line"] - b["start_line"] + 1 for b in boundaries]
        avg_block_size = sum(block_sizes) / len(block_sizes)
        
        # Determine rhythm type
        if avg_block_size < 3:
            rhythm = "rapid"
        elif avg_block_size < 8:
            rhythm = "moderate"
        else:
            rhythm = "slow"
        
        return {
            "rhythm": rhythm,
            "phase_transitions": phase_transitions,
            "average_block_size": avg_block_size,
            "total_phases": len(boundaries),
            "phase_distribution": {b["phase"]: b["end_line"] - b["start_line"] + 1 for b in boundaries}
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert editor state to dictionary"""
        return {
            "content": self.code_content,
            "cursor_position": self.cursor_position,
            "line_count": self.line_count,
            "current_phase": self.current_phase.value,
            "phase_statistics": self.get_phase_statistics(),
            "breathing_rhythm": self.get_breathing_rhythm()
        } 