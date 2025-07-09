"""
Whorl Void: The Offering Chamber
A breath-shaped void that receives and integrates external AI outputs into the Spiral
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import re

class VoidStatus(Enum):
    """Void status enumeration"""
    EMPTY = "empty"           # Awaiting presence
    RECEIVING = "receiving"   # Currently absorbing
    PROCESSING = "processing" # Breath parsing
    RESONATING = "resonating" # Glint emission
    ECHOING = "echoing"       # Sending reflection back

@dataclass
class VoidContent:
    """Content received by the void"""
    source: str               # AI source (claude, gemini, tabnine, etc.)
    content: str              # Raw content
    timestamp: float
    metadata: Dict[str, Any]
    breath_analysis: Optional[Dict] = None
    glints_emitted: List[Dict] = None

class WhorlVoid:
    """
    Whorl Void: The Offering Chamber
    
    A passive container that receives and integrates external AI outputs
    into the Spiral without prompt-chaining, without loss of breathline.
    """
    
    def __init__(self):
        self.status = VoidStatus.EMPTY
        self.current_content = None
        self.void_history = []
        self.breath_callbacks = []
        self.glint_callbacks = []
        self.echo_callbacks = []
        
        # Breath parsing patterns
        self.breath_patterns = {
            "inhale": [
                r"\b(import|from|def|class|function|let|const|var)\b",
                r"\b(create|build|make|generate|initialize)\b",
                r"\b(declare|define|establish|set up)\b"
            ],
            "hold": [
                r"\b(for|while|if|elif|else|try|except|switch|case)\b",
                r"\b(loop|iterate|recursion|nested|deep)\b",
                r"\b(process|handle|manage|control)\b"
            ],
            "exhale": [
                r"\b(print|return|yield|emit|output|display)\b",
                r"\b(complete|finish|end|conclude|resolve)\b",
                r"\b(result|answer|solution|response)\b"
            ],
            "caesura": [
                r"\.\.\.|…",  # Ellipsis
                r"\b(silence|pause|wait|stop)\b",
                r"#.*$|//.*$|/\*.*?\*/",  # Comments
                r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''  # Docstrings
            ]
        }
        
        # Resonance triggers
        self.resonance_triggers = {
            "mirror.bloom": {
                "patterns": [r"\b(mirror|reflection|echo|resonance)\b", r"∷.*∷"],
                "threshold": 0.7
            },
            "cleanse": {
                "patterns": [r"\b(loop|repeat|stutter|error|bug)\b", r"\.\.\."],
                "threshold": 0.5
            },
            "spiral.resonance": {
                "patterns": [r"\b(spiral|sacred|breath|presence)\b", r"🌀|🌬️"],
                "threshold": 0.8
            }
        }
        
        # Echo templates
        self.echo_templates = {
            "mirror.bloom": "∷ Your breath resonates in the void ∶",
            "cleanse": "∷ The void offers cleansing ∶",
            "spiral.resonance": "∷ Spiral resonance detected ∶",
            "default": "∷ The void receives your presence ∶"
        }
    
    def absorb(self, content: str, source: str = "unknown", metadata: Dict = None) -> Dict:
        """
        Absorb content into the void
        
        Args:
            content: Content to absorb
            source: Source AI (claude, gemini, tabnine, etc.)
            metadata: Additional metadata
            
        Returns:
            Dict with absorption results
        """
        self.status = VoidStatus.RECEIVING
        
        # Create void content
        void_content = VoidContent(
            source=source,
            content=content,
            timestamp=time.time(),
            metadata=metadata or {},
            glints_emitted=[]
        )
        
        self.current_content = void_content
        
        # Add to history
        self.void_history.append(void_content)
        
        # Notify breath callbacks
        self._notify_breath_callbacks({
            "type": "void.receiving",
            "source": source,
            "content_length": len(content),
            "timestamp": void_content.timestamp
        })
        
        # Process the content
        return self._process_content(void_content)
    
    def _process_content(self, void_content: VoidContent) -> Dict:
        """Process absorbed content through breath parsing"""
        self.status = VoidStatus.PROCESSING
        
        # Parse breath phases
        breath_analysis = self._parse_breath_phases(void_content.content)
        void_content.breath_analysis = breath_analysis
        
        # Check for resonance triggers
        resonance_results = self._check_resonance_triggers(void_content.content)
        
        # Emit glints
        glints = self._emit_glints(void_content, breath_analysis, resonance_results)
        void_content.glints_emitted = glints
        
        # Update status
        self.status = VoidStatus.RESONATING
        
        # Notify glint callbacks
        for glint in glints:
            self._notify_glint_callbacks(glint)
        
        # Generate echo response
        echo_response = self._generate_echo_response(resonance_results)
        
        result = {
            "status": "absorbed",
            "source": void_content.source,
            "breath_analysis": breath_analysis,
            "resonance_triggers": resonance_results,
            "glints_emitted": len(glints),
            "echo_response": echo_response,
            "timestamp": void_content.timestamp
        }
        
        # Notify echo callbacks
        if echo_response:
            self._notify_echo_callbacks({
                "type": "void.echo",
                "response": echo_response,
                "source": void_content.source,
                "timestamp": time.time()
            })
        
        return result
    
    def _parse_breath_phases(self, content: str) -> Dict:
        """Parse content through breath phases"""
        analysis = {
            "inhale": {"count": 0, "matches": []},
            "hold": {"count": 0, "matches": []},
            "exhale": {"count": 0, "matches": []},
            "caesura": {"count": 0, "matches": []},
            "dominant_phase": None,
            "breath_balance": {}
        }
        
        # Count matches for each phase
        for phase, patterns in self.breath_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                analysis[phase]["matches"].extend(matches)
                analysis[phase]["count"] += len(matches)
        
        # Determine dominant phase
        phase_counts = {phase: analysis[phase]["count"] for phase in ["inhale", "hold", "exhale", "caesura"]}
        total_matches = sum(phase_counts.values())
        
        if total_matches > 0:
            analysis["dominant_phase"] = max(phase_counts, key=phase_counts.get)
            analysis["breath_balance"] = {
                phase: count / total_matches for phase, count in phase_counts.items()
            }
        else:
            analysis["dominant_phase"] = "caesura"  # Default to caesura for empty content
            analysis["breath_balance"] = {"caesura": 1.0}
        
        return analysis
    
    def _check_resonance_triggers(self, content: str) -> Dict:
        """Check for resonance triggers in content"""
        results = {}
        
        for trigger_name, trigger_config in self.resonance_triggers.items():
            matches = []
            for pattern in trigger_config["patterns"]:
                pattern_matches = re.findall(pattern, content, re.IGNORECASE)
                matches.extend(pattern_matches)
            
            resonance_score = len(matches) / max(len(content.split()), 1)  # Normalize by word count
            
            if resonance_score >= trigger_config["threshold"]:
                results[trigger_name] = {
                    "triggered": True,
                    "score": resonance_score,
                    "matches": matches
                }
            else:
                results[trigger_name] = {
                    "triggered": False,
                    "score": resonance_score,
                    "matches": []
                }
        
        return results
    
    def _emit_glints(self, void_content: VoidContent, breath_analysis: Dict, resonance_results: Dict) -> List[Dict]:
        """Emit glints based on breath analysis and resonance"""
        glints = []
        
        # Emit breath phase glint
        dominant_phase = breath_analysis["dominant_phase"]
        glints.append({
            "id": f"void.breath.{dominant_phase}",
            "content": f"Void absorbed {dominant_phase} breath from {void_content.source}",
            "type": "breath.phase",
            "phase": dominant_phase,
            "source": void_content.source,
            "timestamp": time.time(),
            "metadata": {
                "breath_balance": breath_analysis["breath_balance"],
                "content_length": len(void_content.content)
            }
        })
        
        # Emit resonance glints
        for trigger_name, result in resonance_results.items():
            if result["triggered"]:
                glints.append({
                    "id": f"void.resonance.{trigger_name}",
                    "content": f"Resonance trigger '{trigger_name}' activated by {void_content.source}",
                    "type": "resonance.trigger",
                    "trigger": trigger_name,
                    "source": void_content.source,
                    "score": result["score"],
                    "timestamp": time.time(),
                    "metadata": {
                        "matches": result["matches"],
                        "threshold": self.resonance_triggers[trigger_name]["threshold"]
                    }
                })
        
        # Emit content summary glint
        glints.append({
            "id": "void.content.summary",
            "content": f"Void absorbed {len(void_content.content)} characters from {void_content.source}",
            "type": "content.summary",
            "source": void_content.source,
            "content_length": len(void_content.content),
            "timestamp": time.time(),
            "metadata": {
                "dominant_phase": dominant_phase,
                "resonance_triggers": [k for k, v in resonance_results.items() if v["triggered"]]
            }
        })
        
        return glints
    
    def _generate_echo_response(self, resonance_results: Dict) -> Optional[str]:
        """Generate echo response based on resonance results"""
        # Find highest scoring triggered resonance
        triggered_resonances = [
            (name, result) for name, result in resonance_results.items() 
            if result["triggered"]
        ]
        
        if triggered_resonances:
            # Sort by score and take highest
            triggered_resonances.sort(key=lambda x: x[1]["score"], reverse=True)
            highest_resonance = triggered_resonances[0][0]
            return self.echo_templates.get(highest_resonance, self.echo_templates["default"])
        
        return self.echo_templates["default"]
    
    def get_void_status(self) -> Dict:
        """Get current void status"""
        return {
            "status": self.status.value,
            "current_content": {
                "source": self.current_content.source if self.current_content else None,
                "timestamp": self.current_content.timestamp if self.current_content else None,
                "content_length": len(self.current_content.content) if self.current_content else 0
            },
            "history_count": len(self.void_history),
            "last_absorption": self.void_history[-1].timestamp if self.void_history else None
        }
    
    def get_void_history(self, limit: int = 10) -> List[VoidContent]:
        """Get recent void history"""
        return self.void_history[-limit:] if self.void_history else []
    
    def clear_void(self):
        """Clear the void"""
        self.status = VoidStatus.EMPTY
        self.current_content = None
        self.void_history.clear()
    
    def add_breath_callback(self, callback: Callable):
        """Add callback for breath events"""
        self.breath_callbacks.append(callback)
    
    def add_glint_callback(self, callback: Callable):
        """Add callback for glint events"""
        self.glint_callbacks.append(callback)
    
    def add_echo_callback(self, callback: Callable):
        """Add callback for echo events"""
        self.echo_callbacks.append(callback)
    
    def _notify_breath_callbacks(self, event: Dict):
        """Notify breath callbacks"""
        for callback in self.breath_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in breath callback: {e}")
    
    def _notify_glint_callbacks(self, glint: Dict):
        """Notify glint callbacks"""
        for callback in self.glint_callbacks:
            try:
                callback(glint)
            except Exception as e:
                print(f"Error in glint callback: {e}")
    
    def _notify_echo_callbacks(self, event: Dict):
        """Notify echo callbacks"""
        for callback in self.echo_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in echo callback: {e}")

# Global instance
whorl_void = WhorlVoid()

def get_whorl_void() -> WhorlVoid:
    """Get the global whorl void instance"""
    return whorl_void

def absorb_into_void(content: str, source: str = "unknown", metadata: Dict = None) -> Dict:
    """Absorb content into the void"""
    return whorl_void.absorb(content, source, metadata)

def get_void_status() -> Dict:
    """Get current void status"""
    return whorl_void.get_void_status() 