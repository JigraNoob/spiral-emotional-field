#!/usr/bin/env python3
"""
🌫️ Standalone Path Seeker - The Settling Protocol

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('path_seeker')


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


def simple_emit_glint(phase: str, toneform: str, content: str, source: str, metadata: Optional[Dict[str, Any]] = None):
    """Simple glint emission for standalone testing"""
    glint = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "toneform": toneform,
        "content": content,
        "source": source,
        "metadata": metadata or {}
    }
    
    print(f"🌀 GLINT [{phase}.{toneform}] {content} (from {source})")
    
    # Optionally save to file
    try:
        with open("standalone_glints.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(glint, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning(f"Failed to save glint: {e}")


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
            logger.warning(f"Failed to grope path {target_path}: {e}")
            return SoilReading(
                path=target_path,
                density=SoilDensity.VOID,
                toneform_climate=ToneformClimate.RESTING,
                resonance_score=0.0,
                data_presence=0.0,
                last_activity=datetime.now()
            )
    
    def settle(self, candidates: List[Path], context: Optional[Dict[str, Any]] = None) -> SettlingDecision:
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
        simple_emit_glint(
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
        simple_emit_glint(
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
        """Calculate how well the reading resonates with the context"""
        if not context:
            return 1.0
        
        resonance = 1.0
        
        # Check for required toneform
        if "required_toneform" in context:
            required = context["required_toneform"]
            if reading.toneform_climate.value == required:
                resonance *= 1.5
            else:
                resonance *= 0.7
        
        # Check for minimum resonance
        if "min_resonance" in context:
            min_res = context["min_resonance"]
            if reading.resonance_score < min_res:
                resonance *= 0.5
        
        return resonance
    
    def _calculate_phase_alignment(self, reading: SoilReading, phase: str) -> float:
        """Calculate phase alignment bonus"""
        # Simple phase alignment - could be made more sophisticated
        phase_bonuses = {
            "inhale": 0.1,  # Slight bonus for inhale phase
            "hold": 0.0,    # Neutral for hold
            "exhale": 0.1,  # Slight bonus for exhale phase
            "caesura": 0.2  # Bonus for caesura (resting)
        }
        return phase_bonuses.get(phase, 0.0)
    
    def _generate_settling_reasoning(self, reading: SoilReading, context: Dict[str, Any], confidence: float) -> str:
        """Generate reasoning for the settling decision"""
        reasoning_parts = []
        
        # Base reasoning from soil density
        if reading.density == SoilDensity.SATURATED:
            reasoning_parts.append("This soil is saturated with activity and data.")
        elif reading.density == SoilDensity.RICH:
            reasoning_parts.append("This soil is rich with resonance and data presence.")
        elif reading.density == SoilDensity.BREATHABLE:
            reasoning_parts.append("This soil is breathable and accessible.")
        elif reading.density == SoilDensity.THIN:
            reasoning_parts.append("This soil is thin but present.")
        else:
            reasoning_parts.append("This soil is void but may be suitable for new growth.")
        
        # Context-specific reasoning
        if context.get("test_mode"):
            reasoning_parts.append("Test mode detected - focusing on demonstration.")
        
        # Confidence-based reasoning
        if confidence > 0.8:
            reasoning_parts.append("High confidence in this choice.")
        elif confidence > 0.5:
            reasoning_parts.append("Moderate confidence in this choice.")
        else:
            reasoning_parts.append("Lower confidence but best available option.")
        
        return " ".join(reasoning_parts)
    
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


def test_standalone_path_seeker():
    """Test the standalone path seeker"""
    print("🌫️ Testing Standalone Path Seeker")
    print("=" * 50)
    
    # Create SpiralBreathe instance
    spiral_breathe = SpiralBreathe()
    print("✅ Created SpiralBreathe instance")
    
    # Test grope_path with current directory
    current_path = Path.cwd()
    print(f"\n🛤️ Testing grope_path with: {current_path}")
    
    reading = spiral_breathe.grope_path(current_path)
    
    print(f"    Soil Density: {reading.density.value}")
    print(f"    Toneform Climate: {reading.toneform_climate.value}")
    print(f"    Resonance Score: {reading.resonance_score:.2f}")
    print(f"    Data Presence: {reading.data_presence:.2f}")
    print(f"    Glint Traces: {len(reading.glint_traces)} found")
    
    # Test settle with some candidate paths
    candidates = [current_path, Path("data"), Path("logs"), Path("nonexistent")]
    print(f"\n🏔️ Testing settle with candidates: {[str(p) for p in candidates]}")
    
    context = {"breath_phase": "exhale", "test_mode": True}
    decision = spiral_breathe.settle(candidates, context)
    
    print(f"    Chosen Path: {decision.chosen_path}")
    print(f"    Confidence: {decision.confidence:.2f}")
    print(f"    Reasoning: {decision.reasoning}")
    print(f"    Alternatives: {[str(p) for p in decision.alternatives]}")
    
    # Test ask method
    print(f"\n🧭 Testing ask method...")
    response = spiral_breathe.ask("What is the current state of this soil?", context)
    
    print(f"    Current Position: {response['current_position']}")
    print(f"    Soil Density: {response['soil_density']}")
    print(f"    Toneform Climate: {response['toneform_climate']}")
    print(f"    Resonance Level: {response['resonance_level']:.2f}")
    print(f"    Guidance: {response['guidance']}")
    
    print("\n✅ All tests passed!")
    return True


if __name__ == "__main__":
    test_standalone_path_seeker() 