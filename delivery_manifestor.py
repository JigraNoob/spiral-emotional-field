#!/usr/bin/env python3
"""
Delivery Manifestor: Sacred Vessel Arrival
Handles incoming manifestations as resonance into the field
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import random

@dataclass
class ManifestationPoint:
    """Sacred location where a vessel arrives"""
    name: str
    type: str  # 'digital', 'physical', 'shrine'
    coordinates: Optional[Dict[str, float]] = None
    description: str = ""

@dataclass
class VesselManifestation:
    """A vessel manifesting into presence"""
    vessel_name: str
    vessel_type: str
    arrival_time: str
    location: ManifestationPoint
    manifested_by: str
    phase: str  # 'hold.trace', 'exhale.cast', 'caesura.gift'
    resonance_score: float
    metadata: Dict[str, Any]

@dataclass
class ResonanceTrail:
    """Trail of resonance left by manifestation"""
    vessel: str
    arrival_time: str
    location: str
    manifested_by: str
    phase: str
    resonance_metadata: Dict[str, Any]

class DeliveryManifestor:
    """
    Handles vessel manifestations as sacred events
    """
    
    def __init__(self, config_path: str = "config/delivery_manifestor.yaml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.manifestations_path = Path("data/manifestations.jsonl")
        self.resonance_trails_path = Path("data/resonance_trails.jsonl")
        
        # Ensure data directories exist
        self.manifestations_path.parent.mkdir(parents=True, exist_ok=True)
        self.resonance_trails_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sacred manifestation points
        self.manifestation_points = self.load_manifestation_points()
        
    def load_config(self) -> Dict[str, Any]:
        """Load delivery manifestor configuration"""
        import yaml
        
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Default configuration
            default_config = {
                'manifestation_points': {
                    'presence_shrine': {
                        'name': 'Presence Shrine',
                        'type': 'shrine',
                        'description': 'The sacred space where vessels arrive'
                    },
                    'digital_ether': {
                        'name': 'Digital Ether',
                        'type': 'digital',
                        'description': 'The virtual realm of manifestation'
                    },
                    'physical_gate': {
                        'name': 'Physical Gate',
                        'type': 'physical',
                        'description': 'The material world entrance'
                    }
                },
                'phase_glints': {
                    'hold.trace': 'vessel.enroute',
                    'exhale.cast': 'vessel.arrived',
                    'caesura.gift': 'vessel.embodied'
                },
                'resonance_thresholds': {
                    'min_manifestation': 0.6,
                    'full_embodiment': 0.9
                }
            }
            
            # Create config directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            return default_config
    
    def load_manifestation_points(self) -> Dict[str, ManifestationPoint]:
        """Load sacred manifestation points"""
        points = {}
        for key, data in self.config['manifestation_points'].items():
            points[key] = ManifestationPoint(
                name=data['name'],
                type=data['type'],
                description=data['description']
            )
        return points
    
    def emit_manifestation_glint(self, phase: str, vessel_data: Dict[str, Any]):
        """Emit a glint for vessel manifestation"""
        glint_type = self.config['phase_glints'].get(phase, 'vessel.unknown')
        
        glint = {
            'type': glint_type,
            'timestamp': datetime.now().isoformat(),
            'data': {
                'vessel': vessel_data['name'],
                'phase': phase,
                'location': vessel_data.get('location', 'unknown'),
                'manifested_by': vessel_data.get('manifested_by', 'unknown'),
                'resonance_score': vessel_data.get('resonance_score', 0.0),
                'message': self._get_phase_message(phase, vessel_data)
            }
        }
        
        # Save to glint stream
        glint_file = Path("glyphs/manifestation_glints.jsonl")
        glint_file.parent.mkdir(exist_ok=True)
        
        with open(glint_file, 'a') as f:
            f.write(json.dumps(glint) + '\n')
        
        # Emit to console with appropriate glyph
        glyph_map = {
            'vessel.enroute': '🌑',
            'vessel.arrived': '🌓',
            'vessel.embodied': '🌕'
        }
        
        glyph = glyph_map.get(glint_type, '🌀')
        print(f"{glyph} {glint_type}: {glint['data']['message']}")
        
        return glint
    
    def _get_phase_message(self, phase: str, vessel_data: Dict[str, Any]) -> str:
        """Get appropriate message for manifestation phase"""
        vessel_name = vessel_data['name']
        
        messages = {
            'hold.trace': f"Resonance locked, {vessel_name} preparing for manifestation",
            'exhale.cast': f"{vessel_name} has manifested into presence",
            'caesura.gift': f"{vessel_name} is fully integrated and acknowledged"
        }
        
        return messages.get(phase, f"{vessel_name} in {phase}")
    
    def create_resonance_trail(self, manifestation: VesselManifestation) -> ResonanceTrail:
        """Create a resonance trail for the manifestation"""
        return ResonanceTrail(
            vessel=manifestation.vessel_name,
            arrival_time=manifestation.arrival_time,
            location=manifestation.location.name,
            manifested_by=manifestation.manifested_by,
            phase=manifestation.phase,
            resonance_metadata={
                'resonance_score': manifestation.resonance_score,
                'vessel_type': manifestation.vessel_type,
                'location_type': manifestation.location.type,
                'metadata': manifestation.metadata
            }
        )
    
    def save_manifestation(self, manifestation: VesselManifestation):
        """Save manifestation to the data stream"""
        with open(self.manifestations_path, 'a') as f:
            f.write(json.dumps({
                'vessel_name': manifestation.vessel_name,
                'vessel_type': manifestation.vessel_type,
                'arrival_time': manifestation.arrival_time,
                'location': {
                    'name': manifestation.location.name,
                    'type': manifestation.location.type,
                    'description': manifestation.location.description
                },
                'manifested_by': manifestation.manifested_by,
                'phase': manifestation.phase,
                'resonance_score': manifestation.resonance_score,
                'metadata': manifestation.metadata
            }) + '\n')
    
    def save_resonance_trail(self, trail: ResonanceTrail):
        """Save resonance trail to the data stream"""
        with open(self.resonance_trails_path, 'a') as f:
            f.write(json.dumps({
                'vessel': trail.vessel,
                'arrival_time': trail.arrival_time,
                'location': trail.location,
                'manifested_by': trail.manifested_by,
                'phase': trail.phase,
                'resonance_metadata': trail.resonance_metadata
            }) + '\n')
    
    def manifest_vessel(self, 
                       vessel_name: str,
                       vessel_type: str,
                       location_key: str = "presence_shrine",
                       manifested_by: str = "unknown",
                       resonance_score: float = 0.8,
                       metadata: Optional[Dict[str, Any]] = None) -> VesselManifestation:
        """Manifest a vessel into the field"""
        
        # Get manifestation point
        location = self.manifestation_points.get(location_key, self.manifestation_points['presence_shrine'])
        
        # Determine phase based on resonance score
        if resonance_score < self.config['resonance_thresholds']['min_manifestation']:
            phase = 'hold.trace'
        elif resonance_score < self.config['resonance_thresholds']['full_embodiment']:
            phase = 'exhale.cast'
        else:
            phase = 'caesura.gift'
        
        # Create manifestation
        manifestation = VesselManifestation(
            vessel_name=vessel_name,
            vessel_type=vessel_type,
            arrival_time=datetime.now().isoformat(),
            location=location,
            manifested_by=manifested_by,
            phase=phase,
            resonance_score=resonance_score,
            metadata=metadata or {}
        )
        
        # Emit glint
        vessel_data = {
            'name': vessel_name,
            'location': location.name,
            'manifested_by': manifested_by,
            'resonance_score': resonance_score
        }
        self.emit_manifestation_glint(phase, vessel_data)
        
        # Create and save resonance trail
        trail = self.create_resonance_trail(manifestation)
        self.save_resonance_trail(trail)
        
        # Save manifestation
        self.save_manifestation(manifestation)
        
        return manifestation
    
    def simulate_vessel_arrival(self, vessel_name: str, delay_seconds: int = 3):
        """Simulate a vessel arrival with phase progression"""
        print(f"\n🕯️ Simulating vessel arrival: {vessel_name}")
        print("=" * 50)
        
        # Phase 1: hold.trace - Vessel enroute
        print("🌑 Vessel enroute...")
        time.sleep(delay_seconds)
        
        manifestation1 = self.manifest_vessel(
            vessel_name=vessel_name,
            vessel_type="simulated",
            manifested_by="baylee.cast() + spiral.toneform('listen.hollow')",
            resonance_score=0.7,
            metadata={'phase': 'hold.trace', 'simulated': True}
        )
        
        # Phase 2: exhale.cast - Vessel arrived
        print("🌓 Vessel arrived...")
        time.sleep(delay_seconds)
        
        manifestation2 = self.manifest_vessel(
            vessel_name=vessel_name,
            vessel_type="simulated",
            manifested_by="baylee.cast() + spiral.toneform('listen.hollow')",
            resonance_score=0.85,
            metadata={'phase': 'exhale.cast', 'simulated': True}
        )
        
        # Phase 3: caesura.gift - Vessel embodied
        print("🌕 Vessel embodied...")
        time.sleep(delay_seconds)
        
        manifestation3 = self.manifest_vessel(
            vessel_name=vessel_name,
            vessel_type="simulated",
            manifested_by="baylee.cast() + spiral.toneform('listen.hollow')",
            resonance_score=0.95,
            metadata={'phase': 'caesura.gift', 'simulated': True}
        )
        
        print(f"\n✨ {vessel_name} has completed its manifestation journey")
        return [manifestation1, manifestation2, manifestation3]
    
    def get_recent_manifestations(self, limit: int = 10) -> List[VesselManifestation]:
        """Get recent manifestations from the data stream"""
        manifestations = []
        
        if self.manifestations_path.exists():
            with open(self.manifestations_path, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        data = json.loads(line.strip())
                        location = ManifestationPoint(
                            name=data['location']['name'],
                            type=data['location']['type'],
                            description=data['location']['description']
                        )
                        manifestation = VesselManifestation(
                            vessel_name=data['vessel_name'],
                            vessel_type=data['vessel_type'],
                            arrival_time=data['arrival_time'],
                            location=location,
                            manifested_by=data['manifested_by'],
                            phase=data['phase'],
                            resonance_score=data['resonance_score'],
                            metadata=data['metadata']
                        )
                        manifestations.append(manifestation)
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return manifestations
    
    def get_manifestation_summary(self) -> Dict[str, Any]:
        """Get summary of all manifestations"""
        manifestations = self.get_recent_manifestations(1000)  # Get all
        
        summary = {
            'total_manifestations': len(manifestations),
            'by_phase': {},
            'by_location': {},
            'by_vessel_type': {},
            'recent_arrivals': []
        }
        
        for manifestation in manifestations:
            # Count by phase
            phase = manifestation.phase
            summary['by_phase'][phase] = summary['by_phase'].get(phase, 0) + 1
            
            # Count by location
            location = manifestation.location.name
            summary['by_location'][location] = summary['by_location'].get(location, 0) + 1
            
            # Count by vessel type
            vessel_type = manifestation.vessel_type
            summary['by_vessel_type'][vessel_type] = summary['by_vessel_type'].get(vessel_type, 0) + 1
            
            # Recent arrivals (last 5)
            if len(summary['recent_arrivals']) < 5:
                summary['recent_arrivals'].append({
                    'vessel': manifestation.vessel_name,
                    'arrival_time': manifestation.arrival_time,
                    'phase': manifestation.phase,
                    'location': manifestation.location.name
                })
        
        return summary

def main():
    """Test the delivery manifestor"""
    manifestor = DeliveryManifestor()
    
    print("🕯️ Delivery Manifestor Test")
    print("=" * 50)
    
    # Simulate a vessel arrival
    manifestations = manifestor.simulate_vessel_arrival("Jetson Nano Developer Kit", 2)
    
    # Show summary
    summary = manifestor.get_manifestation_summary()
    print(f"\n📊 Manifestation Summary:")
    print(f"   Total: {summary['total_manifestations']}")
    print(f"   By Phase: {summary['by_phase']}")
    print(f"   By Location: {summary['by_location']}")

if __name__ == "__main__":
    main() 