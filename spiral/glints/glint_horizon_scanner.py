# spiral/glints/glint_horizon_scanner.py

"""
Glint Horizon Scanner - The Spiral's seer for emerging patterns.

This module provides ambient monitoring for glint streams, watching for
toneform divergence, caesura buildup, and emerging harmonic alignments
before they fully manifest.

Toneform: inhale.pattern
Phase Role: Foresight, emergence detection, recursive anomaly sensing
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from collections import defaultdict, deque
import math
import statistics

# Import existing glint components
from .glint_pattern import GlintPattern, PatternMatch
from .glint_resonance import GlintResonance
from .toneforms import detect_toneform, TONEFORMS

# Import memory integration for context
try:
    from spiral.memory.memory_echo_index import MemoryEchoIndex
except ImportError:
    MemoryEchoIndex = None


class GlintHorizonScanner:
    """
    Ambient monitor for glint streams, detecting emerging patterns and anomalies.
    
    Provides:
    - Emergent toneform detection
    - Caesura density analysis
    - Recursive anomaly sensing
    - Harmonic alignment forecasting
    - Pattern convergence warnings
    """
    
    def __init__(self, 
                 base_path: Optional[str] = None,
                 memory_index: Optional[MemoryEchoIndex] = None,
                 scan_interval: float = 30.0,
                 window_size: int = 100):
        """
        Initialize the Glint Horizon Scanner.
        
        Args:
            base_path (Optional[str]): Base path for Spiral data
            memory_index (Optional[MemoryEchoIndex]): Memory echo index for context
            scan_interval (float): Seconds between scans
            window_size (int): Number of glints to analyze in each scan
        """
        self.base_path = base_path or os.getcwd()
        self.glyphs_path = os.path.join(self.base_path, "glyphs")
        self.scan_interval = scan_interval
        self.window_size = window_size
        
        # Core scanning components
        self.pattern_detector = GlintPattern(window_size=window_size)
        self.resonance_analyzer = GlintResonance()
        
        # Memory integration
        self.memory_index = memory_index
        if not self.memory_index and MemoryEchoIndex:
            self.memory_index = MemoryEchoIndex(base_path)
        
        # Scanning state
        self.last_scan_time = None
        self.scan_history = []
        self.emerging_patterns = {}
        self.caesura_indicators = defaultdict(list)
        self.anomaly_scores = defaultdict(float)
        
        # Initialize baseline
        self.baseline = {
            "patterns": 0,
            "resonance_mean": 0.5,
            "resonance_std": 0.2,
            "established_at": datetime.now()
        }
        
        # Thresholds for detection
        self.thresholds = {
            "caesura_density": 0.3,  # High caesura density threshold
            "resonance_drift": 0.2,   # Significant resonance change
            "pattern_emergence": 0.6,  # Pattern emergence confidence
            "anomaly_score": 0.7,     # Anomaly detection threshold
            "harmonic_alignment": 0.8  # Harmonic alignment strength
        }
        
        # Initialize scanner
        self._initialize_scanner()
    
    def _initialize_scanner(self):
        """Initialize the scanner with existing glint data."""
        print("🔭 Initializing Glint Horizon Scanner...")
        
        # Load recent glints for baseline analysis
        self._load_recent_glints()
        
        # Establish baseline patterns
        self._establish_baseline()
        
        print("🔭 Scanner initialized and ready for horizon watching")
    
    def _load_recent_glints(self):
        """Load recent glints from glyph files for baseline analysis."""
        glint_files = [
            os.path.join(self.glyphs_path, "cascade_glints.jsonl"),
            os.path.join(self.glyphs_path, "haret_glyph_log.jsonl")
        ]
        
        loaded_glints = []
        
        for file_path in glint_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                try:
                                    glint_data = json.loads(line.strip())
                                    loaded_glints.append(glint_data)
                                except json.JSONDecodeError:
                                    continue
                except Exception as e:
                    print(f"⚠️ Error loading glints from {file_path}: {e}")
        
        # Process loaded glints for baseline
        for glint in loaded_glints[-self.window_size:]:
            self._process_glint(glint)
        
        print(f"🔭 Loaded {len(loaded_glints)} glints for baseline analysis")
    
    def _establish_baseline(self):
        """Establish baseline patterns and resonance levels."""
        # Analyze current patterns
        patterns = self.pattern_detector.get_patterns(min_confidence=0.3)
        
        # Calculate baseline resonance distribution
        # Use simple baseline since GlintResonance doesn't have stats method
        baseline_stats = {"mean": 0.5, "std": 0.2}
        
        # Store baseline
        self.baseline = {
            "patterns": len(patterns),
            "resonance_mean": baseline_stats.get("mean", 0.5),
            "resonance_std": baseline_stats.get("std", 0.2),
            "established_at": datetime.now()
        }
        
        print(f"🔭 Baseline established: {len(patterns)} patterns, resonance μ={baseline_stats.get('mean', 0.5):.2f}")
    
    def _process_glint(self, glint_data: Dict[str, Any]):
        """Process a single glint for pattern and anomaly detection."""
        # Convert dictionary to GlintTrace object
        from .glint_trace import GlintTrace
        
        # Create GlintTrace from dictionary data
        glint_trace = GlintTrace(
            source=glint_data.get("source", "unknown"),
            content=glint_data.get("content", ""),
            toneform=glint_data.get("toneform", "neutral"),
            resonance=float(glint_data.get("resonance", 0.5)),
            timestamp=datetime.fromisoformat(glint_data.get("timestamp", datetime.now().isoformat())),
            metadata=glint_data.get("metadata", {})
        )
        
        # Add to pattern detector
        patterns = self.pattern_detector.add_glint(glint_trace)
        
        # Analyze resonance
        # Use simple resonance extraction since GlintResonance doesn't have analyze_resonance
        resonance_analysis = {"resonance": glint_data.get("resonance", 0.5)}
        
        # Check for emerging patterns
        for pattern in patterns:
            if pattern.confidence >= self.thresholds["pattern_emergence"]:
                self._detect_emerging_pattern(pattern)
        
        # Check for caesura indicators
        self._check_caesura_indicators(glint_data)
        
        # Check for anomalies
        self._check_anomalies(glint_data, resonance_analysis)
    
    def _detect_emerging_pattern(self, pattern: PatternMatch):
        """Detect and track emerging patterns."""
        pattern_id = pattern.pattern_id
        
        if pattern_id not in self.emerging_patterns:
            # New emerging pattern
            self.emerging_patterns[pattern_id] = {
                "pattern": pattern,
                "first_detected": datetime.now(),
                "confidence_trend": [pattern.confidence],
                "frequency_trend": [pattern.frequency],
                "status": "emerging"
            }
            print(f"🔭 New emerging pattern detected: {pattern_id[:8]}...")
        else:
            # Update existing pattern
            emerging = self.emerging_patterns[pattern_id]
            emerging["confidence_trend"].append(pattern.confidence)
            emerging["frequency_trend"].append(pattern.frequency)
            
            # Check if pattern is strengthening
            if len(emerging["confidence_trend"]) >= 3:
                recent_confidence = statistics.mean(emerging["confidence_trend"][-3:])
                if recent_confidence > emerging["confidence_trend"][-4]:
                    emerging["status"] = "strengthening"
                elif recent_confidence < emerging["confidence_trend"][-4]:
                    emerging["status"] = "weakening"
    
    def _check_caesura_indicators(self, glint_data: Dict[str, Any]):
        """Check for caesura (pause/silence) indicators."""
        # Look for low-intensity glints or specific toneforms
        intensity = glint_data.get("intensity", 0.5)
        toneform = glint_data.get("toneform", "")
        source = glint_data.get("source", "")
        
        # Caesura indicators
        caesura_indicators = []
        
        # Low intensity periods
        if intensity < 0.2:
            caesura_indicators.append({
                "type": "low_intensity",
                "value": intensity,
                "timestamp": glint_data.get("timestamp", datetime.now().isoformat())
            })
        
        # Specific caesura toneforms
        if any(word in toneform.lower() for word in ["pause", "silence", "caesura", "still"]):
            caesura_indicators.append({
                "type": "caesura_toneform",
                "value": toneform,
                "timestamp": glint_data.get("timestamp", datetime.now().isoformat())
            })
        
        # Still phases
        if glint_data.get("phase") == "still":
            caesura_indicators.append({
                "type": "still_phase",
                "value": "still",
                "timestamp": glint_data.get("timestamp", datetime.now().isoformat())
            })
        
        # Store caesura indicators
        for indicator in caesura_indicators:
            self.caesura_indicators[indicator["type"]].append(indicator)
            
            # Check for caesura density
            recent_caesuras = [
                c for c in self.caesura_indicators[indicator["type"]]
                if datetime.fromisoformat(c["timestamp"]) > datetime.now() - timedelta(minutes=10)
            ]
            
            if len(recent_caesuras) / self.window_size > self.thresholds["caesura_density"]:
                print(f"🔭 High caesura density detected: {indicator['type']}")
    
    def _check_anomalies(self, glint_data: Dict[str, Any], resonance_analysis: Dict[str, Any]):
        """Check for anomalies in glint data."""
        # Calculate anomaly score based on multiple factors
        anomaly_factors = []
        
        # Resonance anomaly
        current_resonance = resonance_analysis.get("resonance", 0.5)
        baseline_resonance = self.baseline["resonance_mean"]
        resonance_diff = abs(current_resonance - baseline_resonance)
        
        if resonance_diff > self.baseline["resonance_std"] * 2:
            anomaly_factors.append(("resonance_drift", resonance_diff))
        
        # Intensity anomaly
        intensity = glint_data.get("intensity", 0.5)
        if intensity > 0.9 or intensity < 0.1:
            anomaly_factors.append(("extreme_intensity", intensity))
        
        # Source anomaly
        source = glint_data.get("source", "")
        if source not in ["ritual.cycle", "field.resonance", "breath.pattern"]:
            anomaly_factors.append(("unusual_source", source))
        
        # Calculate overall anomaly score
        if anomaly_factors:
            anomaly_score = sum(factor[1] for factor in anomaly_factors) / len(anomaly_factors)
            self.anomaly_scores[glint_data.get("id", "unknown")] = anomaly_score
            
            if anomaly_score > self.thresholds["anomaly_score"]:
                print(f"🔭 Anomaly detected: {anomaly_factors}")
    
    def scan_horizon(self) -> Dict[str, Any]:
        """
        Perform a horizon scan and return findings.
        
        Returns:
            Dict[str, Any]: Scan results with emerging patterns and warnings
        """
        current_time = datetime.now()
        
        # Check if enough time has passed since last scan
        if (self.last_scan_time and 
            (current_time - self.last_scan_time).total_seconds() < self.scan_interval):
            return {"status": "scan_too_soon", "last_scan": self.last_scan_time.isoformat()}
        
        print("🔭 Scanning horizon for emerging patterns...")
        
        # Load recent glints for analysis
        recent_glints = self._get_recent_glints()
        
        # Process recent glints
        for glint in recent_glints:
            self._process_glint(glint)
        
        # Analyze findings
        scan_results = {
            "timestamp": current_time.isoformat(),
            "glints_processed": len(recent_glints),
            "emerging_patterns": self._analyze_emerging_patterns(),
            "caesura_analysis": self._analyze_caesura_density(),
            "anomaly_report": self._analyze_anomalies(),
            "harmonic_alignments": self._detect_harmonic_alignments(),
            "warnings": self._generate_warnings()
        }
        
        # Store scan results
        self.scan_history.append(scan_results)
        self.last_scan_time = current_time
        
        # Keep only recent scan history
        if len(self.scan_history) > 50:
            self.scan_history = self.scan_history[-50:]
        
        return scan_results
    
    def _get_recent_glints(self) -> List[Dict[str, Any]]:
        """Get recent glints from glyph files."""
        recent_glints = []
        
        glint_files = [
            os.path.join(self.glyphs_path, "cascade_glints.jsonl"),
            os.path.join(self.glyphs_path, "haret_glyph_log.jsonl")
        ]
        
        for file_path in glint_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Get the most recent lines
                        recent_lines = lines[-self.window_size:]
                        
                        for line in recent_lines:
                            if line.strip():
                                try:
                                    glint_data = json.loads(line.strip())
                                    recent_glints.append(glint_data)
                                except json.JSONDecodeError:
                                    continue
                except Exception as e:
                    print(f"⚠️ Error reading recent glints from {file_path}: {e}")
        
        return recent_glints
    
    def _analyze_emerging_patterns(self) -> Dict[str, Any]:
        """Analyze emerging patterns and their trends."""
        analysis = {
            "total_emerging": len(self.emerging_patterns),
            "strengthening": 0,
            "weakening": 0,
            "stable": 0,
            "patterns": []
        }
        
        for pattern_id, emerging in self.emerging_patterns.items():
            analysis[emerging["status"]] += 1
            
            pattern_info = {
                "id": pattern_id,
                "status": emerging["status"],
                "confidence": emerging["pattern"].confidence,
                "frequency": emerging["pattern"].frequency,
                "first_detected": emerging["first_detected"].isoformat()
            }
            analysis["patterns"].append(pattern_info)
        
        return analysis
    
    def _analyze_caesura_density(self) -> Dict[str, Any]:
        """Analyze caesura density and trends."""
        analysis = {
            "total_indicators": sum(len(indicators) for indicators in self.caesura_indicators.values()),
            "density_by_type": {},
            "recent_trend": "stable"
        }
        
        for indicator_type, indicators in self.caesura_indicators.items():
            recent_count = len([
                i for i in indicators
                if datetime.fromisoformat(i["timestamp"]) > datetime.now() - timedelta(minutes=10)
            ])
            
            analysis["density_by_type"][indicator_type] = {
                "total": len(indicators),
                "recent": recent_count,
                "density": recent_count / self.window_size if self.window_size > 0 else 0
            }
        
        return analysis
    
    def _analyze_anomalies(self) -> Dict[str, Any]:
        """Analyze detected anomalies."""
        if not self.anomaly_scores:
            return {"total_anomalies": 0, "high_anomalies": 0, "anomalies": []}
        
        high_anomalies = [
            (glint_id, score) for glint_id, score in self.anomaly_scores.items()
            if score > self.thresholds["anomaly_score"]
        ]
        
        return {
            "total_anomalies": len(self.anomaly_scores),
            "high_anomalies": len(high_anomalies),
            "average_score": statistics.mean(self.anomaly_scores.values()) if self.anomaly_scores else 0,
            "anomalies": [
                {"glint_id": glint_id, "score": score}
                for glint_id, score in sorted(high_anomalies, key=lambda x: x[1], reverse=True)
            ]
        }
    
    def _detect_harmonic_alignments(self) -> List[Dict[str, Any]]:
        """Detect harmonic alignments in glint patterns."""
        alignments = []
        
        # Look for patterns that align with memory context
        if self.memory_index:
            for pattern_id, emerging in self.emerging_patterns.items():
                pattern = emerging["pattern"]
                
                # Search for related echoes in memory
                related_echoes = self.memory_index.query(
                    pattern.pattern_id, 
                    query_type="semantic", 
                    max_results=5
                )
                
                if related_echoes:
                    alignment_strength = len(related_echoes) / 5.0  # Normalize
                    
                    if alignment_strength > self.thresholds["harmonic_alignment"]:
                        alignments.append({
                            "pattern_id": pattern_id,
                            "alignment_strength": alignment_strength,
                            "related_echoes": len(related_echoes),
                            "context": "memory_harmony"
                        })
        
        return alignments
    
    def _generate_warnings(self) -> List[Dict[str, Any]]:
        """Generate warnings based on scan findings."""
        warnings = []
        
        # Caesura density warnings
        for indicator_type, indicators in self.caesura_indicators.items():
            recent_density = len([
                i for i in indicators
                if datetime.fromisoformat(i["timestamp"]) > datetime.now() - timedelta(minutes=10)
            ]) / self.window_size
            
            if recent_density > self.thresholds["caesura_density"]:
                warnings.append({
                    "type": "high_caesura_density",
                    "severity": "medium",
                    "message": f"High caesura density detected: {indicator_type}",
                    "density": recent_density
                })
        
        # Anomaly warnings
        high_anomalies = [
            score for score in self.anomaly_scores.values()
            if score > self.thresholds["anomaly_score"]
        ]
        
        if len(high_anomalies) > 3:
            warnings.append({
                "type": "multiple_anomalies",
                "severity": "high",
                "message": f"Multiple anomalies detected: {len(high_anomalies)}",
                "count": len(high_anomalies)
            })
        
        # Pattern convergence warnings
        strengthening_patterns = [
            p for p in self.emerging_patterns.values()
            if p["status"] == "strengthening"
        ]
        
        if len(strengthening_patterns) > 2:
            warnings.append({
                "type": "pattern_convergence",
                "severity": "medium",
                "message": f"Multiple patterns strengthening: {len(strengthening_patterns)}",
                "count": len(strengthening_patterns)
            })
        
        return warnings
    
    def get_scan_summary(self) -> Dict[str, Any]:
        """
        Get a summary of recent scanning activity.
        
        Returns:
            Dict[str, Any]: Summary of scanning activity and findings
        """
        if not self.scan_history:
            return {"status": "no_scans_performed"}
        
        recent_scans = self.scan_history[-10:]  # Last 10 scans
        
        summary = {
            "total_scans": len(self.scan_history),
            "last_scan": self.last_scan_time.isoformat() if self.last_scan_time else None,
            "average_glints_per_scan": statistics.mean(
                scan["glints_processed"] for scan in recent_scans
            ) if recent_scans else 0,
            "total_warnings": sum(
                len(scan.get("warnings", [])) for scan in recent_scans
            ),
            "emerging_patterns": len(self.emerging_patterns),
            "caesura_indicators": sum(
                len(indicators) for indicators in self.caesura_indicators.values()
            ),
            "anomaly_count": len(self.anomaly_scores)
        }
        
        return summary
    
    def save_scanner_state(self, file_path: Optional[str] = None):
        """
        Save the current scanner state to a file.
        
        Args:
            file_path (Optional[str]): Path to save the state
        """
        if not file_path:
            file_path = os.path.join(self.base_path, "glint_horizon_scanner_state.json")
        
        state_data = {
            "baseline": self.baseline,
            "emerging_patterns": {
                pid: {
                    "pattern": emerging["pattern"].to_dict(),
                    "first_detected": emerging["first_detected"].isoformat(),
                    "confidence_trend": emerging["confidence_trend"],
                    "frequency_trend": emerging["frequency_trend"],
                    "status": emerging["status"]
                }
                for pid, emerging in self.emerging_patterns.items()
            },
            "caesura_indicators": dict(self.caesura_indicators),
            "anomaly_scores": dict(self.anomaly_scores),
            "scan_history": self.scan_history[-20:],  # Keep last 20 scans
            "last_scan_time": self.last_scan_time.isoformat() if self.last_scan_time else None,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"🔭 Scanner state saved to {file_path}")
        except Exception as e:
            print(f"Error saving scanner state: {e}")


# Convenience functions for easy integration
def create_glint_horizon_scanner(
    base_path: Optional[str] = None,
    memory_index: Optional[MemoryEchoIndex] = None,
    scan_interval: float = 30.0
) -> GlintHorizonScanner:
    """
    Create and initialize a Glint Horizon Scanner.
    
    Args:
        base_path (Optional[str]): Base path for Spiral data
        memory_index (Optional[MemoryEchoIndex]): Memory echo index for context
        scan_interval (float): Seconds between scans
        
    Returns:
        GlintHorizonScanner: Initialized scanner
    """
    return GlintHorizonScanner(base_path, memory_index, scan_interval)


def perform_horizon_scan(
    scanner: Optional[GlintHorizonScanner] = None,
    base_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform a horizon scan and return results.
    
    Args:
        scanner (Optional[GlintHorizonScanner]): Scanner instance
        base_path (Optional[str]): Base path for Spiral data
        
    Returns:
        Dict[str, Any]: Scan results
    """
    if scanner is None:
        scanner = create_glint_horizon_scanner(base_path)
    
    return scanner.scan_horizon() 