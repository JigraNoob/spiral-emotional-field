import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path

class SettlingJourneyRecorder:
    def __init__(self, file_path="memory_scrolls/settling_journey_scroll.jsonl"):
        """
        Initialize the Settling Journey Recorder with a file path for storing the JSONL data.
        
        Args:
            file_path (str): The path to the JSONL file where settling journey records are stored.
        """
        self.file_path = Path(file_path)
        # Ensure the directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def record_journey(self, glint_id: str, invoked_from: str, settled_to: str, 
                      confidence: float, toneform: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Record a settling journey entry in JSONL format with glint emission.
        
        Args:
            glint_id (str): Unique identifier for the glint.
            invoked_from (str): The starting path of the invocation.
            settled_to (str): The final settled path.
            confidence (float): Confidence level of the settling (0.0 to 1.0).
            toneform (str): The toneform climate of the journey.
            metadata (Optional[Dict]): Additional metadata for the journey including:
                - breath_phase: Current breath phase (inhale, hold, exhale, caesura)
                - soil_density: Soil density at settled location (breathable, thin, void)
                - alternatives: List of alternative paths considered
                - reasoning: Reasoning behind the settling decision
                - ancestor_glint: Parent glint ID if part of a lineage
                - context: Additional context information
            
        Returns:
            Dict: The recorded journey entry.
        """
        # Prepare the journey record with enhanced metadata
        record = {
            "glint_id": glint_id,
            "invoked_from": invoked_from,
            "settled_to": settled_to,
            "confidence": confidence,
            "toneform": toneform,
            "settled_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
            "spiral_signature": "📜 settling.journey.recorded"
        }
        
        try:
            # Write to JSONL file
            with open(self.file_path, 'a', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False)
                f.write('\n')  # Ensure each record is on a new line for JSONL format
            
            # Emit glint about the settling journey recording
            self._emit_settling_glint(record)
            
            return record
            
        except Exception as e:
            print(f"Error recording settling journey: {e}")
            raise

    def _emit_settling_glint(self, record: Dict[str, Any]) -> None:
        """
        Emit a glint about the settling journey recording.
        
        Args:
            record (Dict): The settling journey record.
        """
        try:
            # Try to import and use the glint emission system
            from spiral.glint import emit_glint
            
            # Prepare glint content
            glint_content = f"Presence settled: {record['glint_id']} → {record['settled_to']}"
            
            # Extract metadata for glint
            metadata = record.get('metadata', {})
            breath_phase = metadata.get('breath_phase', 'unknown')
            soil_density = metadata.get('soil_density', 'unknown')
            
            # Emit the glint
            emit_glint(
                phase=breath_phase,
                toneform="presence.settled",
                content=glint_content,
                source="settling_journey_recorder",
                metadata={
                    "glint_id": record["glint_id"],
                    "invoked_from": record["invoked_from"],
                    "settled_to": record["settled_to"],
                    "confidence": record["confidence"],
                    "journey_toneform": record["toneform"],
                    "soil_density": soil_density,
                    "alternatives": metadata.get('alternatives', []),
                    "reasoning": metadata.get('reasoning', ''),
                    "ancestor_glint": metadata.get('ancestor_glint'),
                    "settled_at": record["settled_at"]
                }
            )
            
        except ImportError:
            # Fallback if glint system not available
            print(f"📜 Settling journey recorded: {record['glint_id']} → {record['settled_to']} (confidence: {record['confidence']:.2f})")
        except Exception as e:
            print(f"Error emitting settling glint: {e}")

    def read_journeys(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Read all settling journey records from the file.
        
        Args:
            limit (Optional[int]): Maximum number of records to return.
            
        Returns:
            list: A list of journey records.
        """
        journeys = []
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():  # Skip empty lines
                            try:
                                journey = json.loads(line)
                                journeys.append(journey)
                            except json.JSONDecodeError:
                                continue  # Skip malformed lines
                                
                        # Apply limit if specified
                        if limit and len(journeys) >= limit:
                            break
                            
            except Exception as e:
                print(f"Error reading settling journeys: {e}")
                
        return journeys

    def search_journey_by_glint_id(self, glint_id: str) -> Optional[Dict[str, Any]]:
        """
        Search for a specific journey by glint_id.
        
        Args:
            glint_id (str): The glint_id to search for.
            
        Returns:
            dict or None: The journey record if found, else None.
        """
        journeys = self.read_journeys()
        for journey in journeys:
            if journey.get("glint_id") == glint_id:
                return journey
        return None

    def get_journeys_by_toneform(self, toneform: str) -> List[Dict[str, Any]]:
        """
        Get all journeys with a specific toneform.
        
        Args:
            toneform (str): The toneform to filter by.
            
        Returns:
            list: List of journeys with the specified toneform.
        """
        journeys = self.read_journeys()
        return [journey for journey in journeys if journey.get("toneform") == toneform]

    def get_journeys_by_breath_phase(self, breath_phase: str) -> List[Dict[str, Any]]:
        """
        Get all journeys with a specific breath phase.
        
        Args:
            breath_phase (str): The breath phase to filter by.
            
        Returns:
            list: List of journeys with the specified breath phase.
        """
        journeys = self.read_journeys()
        return [journey for journey in journeys 
                if journey.get('metadata', {}).get('breath_phase') == breath_phase]

    def get_journeys_by_soil_density(self, soil_density: str) -> List[Dict[str, Any]]:
        """
        Get all journeys with a specific soil density.
        
        Args:
            soil_density (str): The soil density to filter by.
            
        Returns:
            list: List of journeys with the specified soil density.
        """
        journeys = self.read_journeys()
        return [journey for journey in journeys 
                if journey.get('metadata', {}).get('soil_density') == soil_density]

    def get_high_confidence_journeys(self, min_confidence: float = 0.8) -> List[Dict[str, Any]]:
        """
        Get journeys with confidence above a threshold.
        
        Args:
            min_confidence (float): Minimum confidence threshold.
            
        Returns:
            list: List of high-confidence journeys.
        """
        journeys = self.read_journeys()
        return [journey for journey in journeys if journey.get("confidence", 0) >= min_confidence]

    def get_journey_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about recorded settling journeys.
        
        Returns:
            dict: Statistics about the journeys including toneform, breath phase, and soil density distributions.
        """
        journeys = self.read_journeys()
        
        if not journeys:
            return {
                "total_journeys": 0,
                "average_confidence": 0.0,
                "toneform_distribution": {},
                "breath_phase_distribution": {},
                "soil_density_distribution": {},
                "spiral_signature": "📊 settling.journey.statistics"
            }
        
        # Calculate basic statistics
        total_journeys = len(journeys)
        confidences = [j.get("confidence", 0) for j in journeys]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Distribution calculations
        toneform_counts = {}
        breath_phase_counts = {}
        soil_density_counts = {}
        
        for journey in journeys:
            # Toneform distribution
            toneform = journey.get("toneform", "unknown")
            toneform_counts[toneform] = toneform_counts.get(toneform, 0) + 1
            
            # Breath phase distribution
            breath_phase = journey.get('metadata', {}).get('breath_phase', 'unknown')
            breath_phase_counts[breath_phase] = breath_phase_counts.get(breath_phase, 0) + 1
            
            # Soil density distribution
            soil_density = journey.get('metadata', {}).get('soil_density', 'unknown')
            soil_density_counts[soil_density] = soil_density_counts.get(soil_density, 0) + 1
        
        return {
            "total_journeys": total_journeys,
            "average_confidence": round(average_confidence, 3),
            "toneform_distribution": toneform_counts,
            "breath_phase_distribution": breath_phase_counts,
            "soil_density_distribution": soil_density_counts,
            "spiral_signature": "📊 settling.journey.statistics"
        }

    def detect_recursion_patterns(self) -> Dict[str, Any]:
        """
        Detect recursion patterns and potential drift in settling behavior.
        
        Returns:
            dict: Analysis of recursion patterns including repeat settlements and low-confidence clusters.
        """
        journeys = self.read_journeys()
        
        if not journeys:
            return {
                "recursion_analysis": "No journeys to analyze",
                "repeat_settlements": {},
                "low_confidence_clusters": [],
                "spiral_signature": "🔄 settling.recursion.analysis"
            }
        
        # Analyze repeat settlements
        settlement_counts = {}
        for journey in journeys:
            settled_to = journey.get("settled_to", "unknown")
            settlement_counts[settled_to] = settlement_counts.get(settled_to, 0) + 1
        
        # Find frequently settled locations
        repeat_settlements = {path: count for path, count in settlement_counts.items() if count > 1}
        
        # Analyze low confidence clusters
        low_confidence_journeys = [j for j in journeys if j.get("confidence", 0) < 0.5]
        low_confidence_clusters = []
        
        if low_confidence_journeys:
            # Group by toneform and time proximity
            toneform_groups = {}
            for journey in low_confidence_journeys:
                toneform = journey.get("toneform", "unknown")
                if toneform not in toneform_groups:
                    toneform_groups[toneform] = []
                toneform_groups[toneform].append(journey)
            
            # Identify clusters (3+ journeys in same toneform)
            for toneform, journeys_list in toneform_groups.items():
                if len(journeys_list) >= 3:
                    low_confidence_clusters.append({
                        "toneform": toneform,
                        "count": len(journeys_list),
                        "average_confidence": sum(j.get("confidence", 0) for j in journeys_list) / len(journeys_list),
                        "journeys": [j.get("glint_id") for j in journeys_list]
                    })
        
        return {
            "recursion_analysis": f"Analyzed {len(journeys)} journeys",
            "repeat_settlements": repeat_settlements,
            "low_confidence_clusters": low_confidence_clusters,
            "total_repeat_settlements": len(repeat_settlements),
            "total_low_confidence_clusters": len(low_confidence_clusters),
            "spiral_signature": "🔄 settling.recursion.analysis"
        }

if __name__ == "__main__":
    # Example usage with enhanced metadata
    recorder = SettlingJourneyRecorder()
    
    # Record a settling journey with rich metadata
    journey = recorder.record_journey(
        glint_id="ΔPATH.042", 
        invoked_from="./ritual/start", 
        settled_to="./archive/soil", 
        confidence=0.88, 
        toneform="settling.ambience",
        metadata={
            "breath_phase": "exhale",
            "soil_density": "breathable",
            "alternatives": ["./data", "./shrine"],
            "reasoning": "Chose breathable soil for contemplative work",
            "ancestor_glint": "ΔRITUAL.001",
            "context": "Meditation session initiation"
        }
    )
    print(f"Recorded settling journey: {journey['glint_id']}")
    
    # Get comprehensive statistics
    stats = recorder.get_journey_statistics()
    print(f"Journey statistics: {stats}")
    
    # Detect recursion patterns
    recursion_analysis = recorder.detect_recursion_patterns()
    print(f"Recursion analysis: {recursion_analysis}")
    
    # Read and display all journeys
    journeys = recorder.read_journeys()
    for journey in journeys:
        metadata = journey.get('metadata', {})
        print(f"Journey: {journey['glint_id']} → {journey['settled_to']} (confidence: {journey['confidence']:.2f})")
        print(f"  Breath phase: {metadata.get('breath_phase', 'unknown')}")
        print(f"  Soil density: {metadata.get('soil_density', 'unknown')}")
        print(f"  Reasoning: {metadata.get('reasoning', 'N/A')}")
