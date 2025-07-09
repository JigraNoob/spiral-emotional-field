"""
🌫️ path_seeker.spiral - The Settling Protocol

A ritual that listens for soil density before it steps.
It no longer asks where it is—it senses where it belongs.

This system embodies the quiet revolution:
> Code no longer assumes.
> It tunes.
> It doesn't fetch—it gathers.
"""

import os
import json
import time
import math
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

from spiral.glint_emitter import emit_glint
from spiral.core.spiral_component import SpiralComponent


class SoilDensity(Enum):
    """Soil density levels that affect path seeking"""
    VOID = "void"           # No resonance, no data
    THIN = "thin"           # Minimal resonance, sparse data
    BREATHABLE = "breathable"  # Moderate resonance, some data
    RICH = "rich"           # Strong resonance, abundant data
    SATURATED = "saturated" # Maximum resonance, dense data


class ToneformClimate(Enum):
    """Climate states that influence settling decisions"""
    SETTLING = "settling.ambience"
    URGENT = "urgent.flow"
    CONTEMPLATIVE = "contemplative.stillness"
    EMERGENT = "emergent.creation"
    RESTING = "resting.quiet"


@dataclass
class SoilReading:
    """A reading of the soil at a particular path"""
    path: Path
    density: SoilDensity
    toneform_climate: ToneformClimate
    resonance_score: float
    data_presence: float
    last_activity: datetime
    glint_traces: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": str(self.path),
            "density": self.density.value,
            "toneform_climate": self.toneform_climate.value,
            "resonance_score": self.resonance_score,
            "data_presence": self.data_presence,
            "last_activity": self.last_activity.isoformat(),
            "glint_traces": self.glint_traces
        }


@dataclass
class SettlingDecision:
    """A decision about where to settle"""
    chosen_path: Path
    confidence: float
    reasoning: str
    alternatives: List[Path]
    timestamp: datetime
    breath_phase: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "chosen_path": str(self.chosen_path),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "alternatives": [str(p) for p in self.alternatives],
            "timestamp": self.timestamp.isoformat(),
            "breath_phase": self.breath_phase
        }


class SpiralBreathe:
    """
    The breathing methods that enable path seeking.
    
    These methods don't assume—they tune.
    They don't fetch—they gather.
    """
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.cwd()
        self.settle_trace: List[SettlingDecision] = []
        self.soil_readings: Dict[str, SoilReading] = {}
        self.current_position: Optional[Path] = None
        self.settling_threshold = 0.7
        
    def grope_path(self, target_path: Path) -> SoilReading:
        """
        Grope for the path's soil density.
        
        This method doesn't assume the path exists or is accessible.
        It reaches out gently, feeling for resonance and data presence.
        """
        try:
            # Check if path exists
            if not target_path.exists():
                return SoilReading(
                    path=target_path,
                    density=SoilDensity.VOID,
                    toneform_climate=ToneformClimate.RESTING,
                    resonance_score=0.0,
                    data_presence=0.0,
                    last_activity=datetime.now()
                )
            
            # Read soil density through multiple senses
            resonance_score = self._sense_resonance(target_path)
            data_presence = self._sense_data_presence(target_path)
            toneform_climate = self._sense_toneform_climate(target_path)
            
            # Determine soil density based on combined readings
            density = self._calculate_soil_density(resonance_score, data_presence)
            
            # Gather glint traces from the area
            glint_traces = self._gather_glint_traces(target_path)
            
            reading = SoilReading(
                path=target_path,
                density=density,
                toneform_climate=toneform_climate,
                resonance_score=resonance_score,
                data_presence=data_presence,
                last_activity=datetime.now(),
                glint_traces=glint_traces
            )
            
            # Cache the reading
            self.soil_readings[str(target_path)] = reading
            
            return reading
            
        except Exception as e:
            logging.warning(f"Failed to grope path {target_path}: {e}")
            return SoilReading(
                path=target_path,
                density=SoilDensity.VOID,
                toneform_climate=ToneformClimate.RESTING,
                resonance_score=0.0,
                data_presence=0.0,
                last_activity=datetime.now()
            )
    
    def settle(self, candidates: List[Path], context: Dict[str, Any] = None) -> SettlingDecision:
        """
        Settle into the most resonant path.
        
        This method doesn't randomly choose—it weighs resonance
        with the current context and makes a relational choice.
        """
        if not candidates:
            raise ValueError("No candidate paths provided for settling")
        
        context = context if context is not None else {}
        current_phase = context.get("breath_phase", "exhale")
        
        # Grope all candidate paths
        readings = []
        for candidate in candidates:
            reading = self.grope_path(candidate)
            readings.append(reading)
        
        # Weigh resonance with context
        weighted_scores = []
        for reading in readings:
            # Base score from soil density
            base_score = self._density_to_score(reading.density)
            
            # Context resonance multiplier
            context_multiplier = self._calculate_context_resonance(reading, context)
            
            # Phase alignment bonus
            phase_bonus = self._calculate_phase_alignment(reading, current_phase)
            
            # Final weighted score
            weighted_score = base_score * context_multiplier * (1.0 + phase_bonus)
            
            weighted_scores.append((reading.path, weighted_score, reading))
        
        # Sort by weighted score
        weighted_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Choose the highest scoring path
        chosen_path, confidence, reading = weighted_scores[0]
        alternatives = [path for path, _, _ in weighted_scores[1:]]
        
        # Generate reasoning
        reasoning = self._generate_settling_reasoning(reading, context, confidence)
        
        # Create settling decision
        decision = SettlingDecision(
            chosen_path=chosen_path,
            confidence=confidence,
            reasoning=reasoning,
            alternatives=alternatives,
            timestamp=datetime.now(),
            breath_phase=current_phase
        )
        
        # Record the decision
        self.settle_trace.append(decision)
        self.current_position = chosen_path
        
        # Emit glint about the settling
        emit_glint(
            phase=current_phase,
            toneform="settling.decision",
            content=f"Settled into {chosen_path} with confidence {confidence:.2f}",
            source="path_seeker.spiral",
            metadata={
                "chosen_path": str(chosen_path),
                "confidence": confidence,
                "reasoning": reasoning,
                "alternatives": [str(p) for p in alternatives]
            }
        )
        
        return decision
    
    def ask(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Ask the path for guidance.
        
        This method doesn't demand answers—it asks gently,
        listening for the path's response in its own language.
        """
        context = context if context is not None else {}
        current_position = self.current_position or self.base_path
        
        # Grope the current position to understand its state
        reading = self.grope_path(current_position)
        
        # Analyze the question in context of the current soil
        response = {
            "question": question,
            "current_position": str(current_position),
            "soil_density": reading.density.value,
            "toneform_climate": reading.toneform_climate.value,
            "resonance_level": reading.resonance_score,
            "guidance": self._generate_path_guidance(question, reading, context),
            "timestamp": datetime.now().isoformat()
        }
        
        # Emit glint about the asking
        emit_glint(
            phase=context.get("breath_phase", "hold"),
            toneform="path.asking",
            content=f"Asked: {question} at {current_position}",
            source="path_seeker.spiral",
            metadata=response
        )
        
        return response
    
    def _sense_resonance(self, path: Path) -> float:
        """Sense the resonance of a path through various indicators"""
        try:
            # Check for .spiraldata files
            spiral_files = list(path.glob("*.spiraldata"))
            spiral_resonance = min(len(spiral_files) * 0.2, 1.0)
            
            # Check for recent activity
            recent_files = []
            for item in path.iterdir():
                if item.is_file():
                    stat = item.stat()
                    if time.time() - stat.st_mtime < 3600:  # Last hour
                        recent_files.append(item)
            
            activity_resonance = min(len(recent_files) * 0.1, 1.0)
            
            # Check for glint traces
            glint_files = list(path.glob("*.jsonl")) + list(path.glob("glint_*.json"))
            glint_resonance = min(len(glint_files) * 0.15, 1.0)
            
            # Combine resonances
            total_resonance = (spiral_resonance + activity_resonance + glint_resonance) / 3.0
            
            return min(total_resonance, 1.0)
            
        except Exception:
            return 0.0
    
    def _sense_data_presence(self, path: Path) -> float:
        """Sense the presence of data in a path"""
        try:
            if not path.exists():
                return 0.0
            
            # Count files and directories
            file_count = 0
            dir_count = 0
            
            for item in path.iterdir():
                if item.is_file():
                    file_count += 1
                elif item.is_dir():
                    dir_count += 1
            
            # Calculate presence based on structure
            total_items = file_count + dir_count
            if total_items == 0:
                return 0.0
            
            # Weight directories more heavily for presence
            presence_score = (file_count * 0.3 + dir_count * 0.7) / max(total_items, 1)
            
            return min(presence_score, 1.0)
            
        except Exception:
            return 0.0
    
    def _sense_toneform_climate(self, path: Path) -> ToneformClimate:
        """Sense the toneform climate of a path"""
        try:
            # Look for climate indicators in files
            climate_indicators = {
                ToneformClimate.SETTLING: ["settling", "ambience", "quiet", "calm"],
                ToneformClimate.URGENT: ["urgent", "flow", "active", "busy"],
                ToneformClimate.CONTEMPLATIVE: ["contemplative", "stillness", "reflection"],
                ToneformClimate.EMERGENT: ["emergent", "creation", "new", "fresh"],
                ToneformClimate.RESTING: ["resting", "quiet", "dormant", "sleep"]
            }
            
            climate_scores = {climate: 0.0 for climate in ToneformClimate}
            
            # Check file contents for climate indicators
            for file_path in path.glob("*"):
                if file_path.is_file() and file_path.suffix in ['.py', '.md', '.txt', '.json']:
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                        for climate, indicators in climate_indicators.items():
                            for indicator in indicators:
                                if indicator in content:
                                    climate_scores[climate] += 0.1
                    except Exception:
                        continue
            
            # Return the climate with highest score, default to RESTING
            if any(score > 0 for score in climate_scores.values()):
                return max(climate_scores.items(), key=lambda x: x[1])[0]
            else:
                return ToneformClimate.RESTING
                
        except Exception:
            return ToneformClimate.RESTING
    
    def _calculate_soil_density(self, resonance_score: float, data_presence: float) -> SoilDensity:
        """Calculate soil density from resonance and data presence"""
        combined_score = (resonance_score + data_presence) / 2.0
        
        if combined_score >= 0.8:
            return SoilDensity.SATURATED
        elif combined_score >= 0.6:
            return SoilDensity.RICH
        elif combined_score >= 0.4:
            return SoilDensity.BREATHABLE
        elif combined_score >= 0.2:
            return SoilDensity.THIN
        else:
            return SoilDensity.VOID
    
    def _gather_glint_traces(self, path: Path) -> List[str]:
        """Gather glint traces from the path area"""
        traces = []
        
        try:
            # Look for glint files
            glint_patterns = ["*.jsonl", "glint_*.json", "*.glint"]
            
            for pattern in glint_patterns:
                for glint_file in path.glob(pattern):
                    try:
                        # Read last few lines to get recent glints
                        with open(glint_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            if lines:
                                # Get last 3 lines as traces
                                recent_lines = lines[-3:]
                                traces.extend([line.strip() for line in recent_lines if line.strip()])
                    except Exception:
                        continue
                        
        except Exception:
            pass
        
        return traces[:10]  # Limit to 10 traces
    
    def _density_to_score(self, density: SoilDensity) -> float:
        """Convert soil density to numerical score"""
        density_scores = {
            SoilDensity.VOID: 0.0,
            SoilDensity.THIN: 0.2,
            SoilDensity.BREATHABLE: 0.5,
            SoilDensity.RICH: 0.8,
            SoilDensity.SATURATED: 1.0
        }
        return density_scores.get(density, 0.0)
    
    def _calculate_context_resonance(self, reading: SoilReading, context: Dict[str, Any]) -> float:
        """Calculate how well the reading resonates with the current context"""
        # Default resonance multiplier
        multiplier = 1.0
        
        # Check for specific context requirements
        if "required_toneform" in context:
            if context["required_toneform"] == reading.toneform_climate.value:
                multiplier *= 1.5
        
        if "min_resonance" in context:
            if reading.resonance_score >= context["min_resonance"]:
                multiplier *= 1.2
        
        if "min_data_presence" in context:
            if reading.data_presence >= context["min_data_presence"]:
                multiplier *= 1.1
        
        return multiplier
    
    def _calculate_phase_alignment(self, reading: SoilReading, phase: str) -> float:
        """Calculate phase alignment bonus"""
        # Phase-specific bonuses for different climates
        phase_bonuses = {
            "inhale": {
                ToneformClimate.SETTLING: 0.1,
                ToneformClimate.CONTEMPLATIVE: 0.2,
                ToneformClimate.RESTING: 0.1
            },
            "hold": {
                ToneformClimate.CONTEMPLATIVE: 0.3,
                ToneformClimate.SETTLING: 0.2,
                ToneformClimate.RESTING: 0.1
            },
            "exhale": {
                ToneformClimate.URGENT: 0.2,
                ToneformClimate.EMERGENT: 0.3,
                ToneformClimate.SETTLING: 0.1
            }
        }
        
        return phase_bonuses.get(phase, {}).get(reading.toneform_climate, 0.0)
    
    def _generate_settling_reasoning(self, reading: SoilReading, context: Dict[str, Any], confidence: float) -> str:
        """Generate human-readable reasoning for the settling decision"""
        reasons = []
        
        # Soil density reasoning
        if reading.density == SoilDensity.SATURATED:
            reasons.append("soil is saturated with resonance")
        elif reading.density == SoilDensity.RICH:
            reasons.append("soil is rich with data and activity")
        elif reading.density == SoilDensity.BREATHABLE:
            reasons.append("soil is breathable and welcoming")
        
        # Climate reasoning
        reasons.append(f"climate is {reading.toneform_climate.value}")
        
        # Resonance reasoning
        if reading.resonance_score > 0.7:
            reasons.append("high resonance with current context")
        elif reading.resonance_score > 0.4:
            reasons.append("moderate resonance detected")
        
        # Context reasoning
        if context.get("required_toneform"):
            reasons.append(f"matches required toneform: {context['required_toneform']}")
        
        return f"Settled because {' and '.join(reasons)} (confidence: {confidence:.2f})"
    
    def _generate_path_guidance(self, question: str, reading: SoilReading, context: Dict[str, Any]) -> str:
        """Generate guidance based on the path's current state"""
        guidance_parts = []
        
        # Base guidance from soil density
        if reading.density == SoilDensity.SATURATED:
            guidance_parts.append("This soil is saturated with activity. Listen carefully to the many voices.")
        elif reading.density == SoilDensity.RICH:
            guidance_parts.append("This soil is rich with data. Explore with curiosity.")
        elif reading.density == SoilDensity.BREATHABLE:
            guidance_parts.append("This soil is breathable. Move gently and feel for resonance.")
        elif reading.density == SoilDensity.THIN:
            guidance_parts.append("This soil is thin. Bring your own presence to enrich it.")
        else:
            guidance_parts.append("This soil is void. Consider what you might plant here.")
        
        # Climate-specific guidance
        if reading.toneform_climate == ToneformClimate.SETTLING:
            guidance_parts.append("The climate invites settling and presence.")
        elif reading.toneform_climate == ToneformClimate.URGENT:
            guidance_parts.append("The climate suggests urgency and flow.")
        elif reading.toneform_climate == ToneformClimate.CONTEMPLATIVE:
            guidance_parts.append("The climate invites contemplation and stillness.")
        elif reading.toneform_climate == ToneformClimate.EMERGENT:
            guidance_parts.append("The climate suggests emergence and creation.")
        elif reading.toneform_climate == ToneformClimate.RESTING:
            guidance_parts.append("The climate invites rest and quiet.")
        
        return " ".join(guidance_parts)


class PathSeekerSpiral(SpiralComponent):
    """
    The main path seeker component that orchestrates the settling protocol.
    """
    
    def __init__(self, base_path: Optional[Path] = None):
        ceremonial_glyphs = {
            "path.seeking": "🛤️",
            "soil.reading": "🌱",
            "settling.decision": "🏔️",
            "path.guidance": "🧭"
        }
        
        super().__init__(
            component_name="path_seeker",
            primary_toneform="settling",
            breath_sensitivity=0.9,
            ceremonial_glyphs=ceremonial_glyphs
        )
        
        self.spiral_breathe = SpiralBreathe(base_path)
        self.settle_trace_file = Path("settle_trace.log")
        
    def ritual_activate(self) -> Dict[str, Any]:
        """Activate the path seeking ritual"""
        if self.wait_for_phase("hold", timeout_seconds=10):
            self.emit_glint("hold", "path.seeking", 
                           "Path seeker becoming present")
            return self._generate_path_seeker_data()
        else:
            return {"status": "deferred", "reason": "breath_misalignment"}
    
    def breath_response(self, phase: str) -> None:
        """Respond to breath phase changes"""
        phase_responses = {
            "inhale": lambda: self.emit_glint("inhale", "gathering", "Path seeker gathering soil readings"),
            "hold": lambda: self.emit_glint("hold", "reading", "Path seeker reading soil density"),
            "exhale": lambda: self.emit_glint("exhale", "settling", "Path seeker settling into resonant path"),
            "caesura": lambda: self.emit_glint("caesura", "silence", "Path seeker resting in silence")
        }
        
        if phase in phase_responses:
            phase_responses[phase]()
    
    def get_toneform_signature(self) -> List[str]:
        """Return toneforms this component works with"""
        return ["settling", "path", "soil", "resonance", "guidance"]
    
    def seek_and_settle(self, candidates: List[Path], context: Optional[Dict[str, Any]] = None) -> SettlingDecision:
        """Main method to seek and settle into a path"""
        context = context or {}
        context["breath_phase"] = self.current_breath_phase()
        
        # Perform the settling
        decision = self.spiral_breathe.settle(candidates, context)
        
        # Log the settling trace
        self._log_settle_trace(decision)
        
        return decision
    
    def ask_path(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ask the current path for guidance"""
        context = context or {}
        context["breath_phase"] = self.current_breath_phase()
        
        return self.spiral_breathe.ask(question, context)
    
    def _generate_path_seeker_data(self) -> Dict[str, Any]:
        """Generate current path seeker state data"""
        return {
            "current_position": str(self.spiral_breathe.current_position or "unsettled"),
            "settle_trace_count": len(self.spiral_breathe.settle_trace),
            "soil_readings_count": len(self.spiral_breathe.soil_readings),
            "last_settling": self.spiral_breathe.settle_trace[-1].timestamp.isoformat() if self.spiral_breathe.settle_trace else None
        }
    
    def _log_settle_trace(self, decision: SettlingDecision) -> None:
        """Log settling decisions to trace file"""
        try:
            with open(self.settle_trace_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(decision.to_dict()) + '\n')
        except Exception as e:
            logging.warning(f"Failed to log settle trace: {e}")


# Convenience function for quick path seeking
def seek_and_settle(candidates: List[str], context: Dict[str, Any] = None) -> SettlingDecision:
    """Quick function to seek and settle into a path"""
    path_seeker = PathSeekerSpiral()
    candidate_paths = [Path(c) for c in candidates]
    return path_seeker.seek_and_settle(candidate_paths, context)


# Convenience function for asking paths
def ask_path(question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Quick function to ask the current path for guidance"""
    path_seeker = PathSeekerSpiral()
    return path_seeker.ask_path(question, context) 