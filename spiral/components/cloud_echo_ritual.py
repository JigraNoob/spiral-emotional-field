"""
Spiral Cloud Echo Ritual
Syncs local longing with global Spiral weather and enables cross-practitioner resonance
"""

import time
import json
import hashlib
import random
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import threading
from pathlib import Path
import requests
from collections import defaultdict

@dataclass
class BreathlineState:
    """Represents a practitioner's breathline state"""
    practitioner_id: str
    timestamp: float
    breath_pattern: str
    coherence: float
    presence_level: float
    longing_intensity: float
    vessel_interest: Dict[str, float]
    location_hash: str  # Anonymized location
    spiral_climate: str

@dataclass
class CoLongingEvent:
    """Represents a co-longing event between practitioners"""
    event_id: str
    timestamp: float
    participants: List[str]
    shared_vessel: str
    longing_intensity: float
    breath_similarity: float
    glints_emitted: List[str]

@dataclass
class GlobalSpiralWeather:
    """Global Spiral weather conditions"""
    timestamp: float
    total_practitioners: int
    average_coherence: float
    average_presence: float
    dominant_breath_pattern: str
    vessel_demand: Dict[str, float]
    climate_conditions: Dict[str, float]

class CloudEchoRitual:
    """
    Cloud Echo Ritual System
    
    Syncs local longing with global Spiral weather, enabling:
    - Cross-practitioner breathline visibility
    - Co-longing event detection
    - Glint cross-pollination
    - Global vessel demand tracking
    """
    
    def __init__(self, cloud_endpoint: str = None, sync_interval: int = 300):
        self.cloud_endpoint = cloud_endpoint or "https://spiral-cloud-echo.vercel.app/api"
        self.sync_interval = sync_interval  # 5 minutes default
        
        # Local state
        self.local_breathline = None
        self.global_weather = None
        self.co_longing_events = []
        self.cross_pollinated_glints = []
        
        # Practitioner tracking
        self.known_practitioners = set()
        self.breathline_history = []
        self.vessel_demand_history = []
        
        # Cross-pollination settings
        self.similarity_threshold = 0.7
        self.cross_pollination_chance = 0.3
        self.max_glint_history = 100
        
        # Start background sync
        self.sync_active = True
        self.sync_thread = threading.Thread(target=self._background_sync, daemon=True)
        self.sync_thread.start()
    
    def update_local_breathline(self, breath_pattern: str, coherence: float, 
                              presence_level: float, longing_intensity: float,
                              vessel_interest: Dict[str, float], location: str = None) -> BreathlineState:
        """Update local breathline state and sync with cloud"""
        
        # Create breathline state
        breathline = BreathlineState(
            practitioner_id=self._generate_practitioner_id(),
            timestamp=time.time(),
            breath_pattern=breath_pattern,
            coherence=coherence,
            presence_level=presence_level,
            longing_intensity=longing_intensity,
            vessel_interest=vessel_interest,
            location_hash=self._hash_location(location),
            spiral_climate=self._determine_spiral_climate(coherence, presence_level)
        )
        
        self.local_breathline = breathline
        self.breathline_history.append(breathline)
        
        # Keep only recent history
        if len(self.breathline_history) > 50:
            self.breathline_history = self.breathline_history[-50:]
        
        # Trigger immediate sync
        self._sync_with_cloud()
        
        # Check for co-longing events
        self._check_co_longing_events(breathline)
        
        return breathline
    
    def get_global_spiral_weather(self) -> GlobalSpiralWeather:
        """Get current global Spiral weather conditions"""
        if self.global_weather is None:
            # Return default weather if no sync has occurred
            return GlobalSpiralWeather(
                timestamp=time.time(),
                total_practitioners=1,
                average_coherence=0.5,
                average_presence=0.5,
                dominant_breath_pattern="steady",
                vessel_demand={},
                climate_conditions={
                    "resonance": 0.5,
                    "longing": 0.5,
                    "manifestation": 0.5
                }
            )
        
        return self.global_weather
    
    def get_co_longing_events(self, limit: int = 10) -> List[CoLongingEvent]:
        """Get recent co-longing events"""
        return sorted(
            self.co_longing_events,
            key=lambda x: x.timestamp,
            reverse=True
        )[:limit]
    
    def get_cross_pollinated_glints(self) -> List[str]:
        """Get glints that have been cross-pollinated from other practitioners"""
        return self.cross_pollinated_glints[-self.max_glint_history:]
    
    def emit_co_longing_glint(self, vessel_type: str, intensity: float) -> List[str]:
        """Emit glints based on co-longing events"""
        
        glints = []
        
        # Check if there are co-longing events for this vessel
        co_longing_count = sum(
            1 for event in self.co_longing_events
            if event.shared_vessel == vessel_type and 
            time.time() - event.timestamp < 3600  # Last hour
        )
        
        if co_longing_count > 0:
            glints.append(f"co.longing.{vessel_type}.shared")
            glints.append(f"co.longing.intensity.{intensity:.1f}")
        
        # Add cross-pollinated glints
        if self.cross_pollinated_glints:
            recent_glints = self.cross_pollinated_glints[-5:]  # Last 5
            glints.extend(recent_glints)
        
        # Add global weather glints
        weather = self.get_global_spiral_weather()
        if weather.average_coherence > 0.8:
            glints.append("global.coherence.high")
        if weather.average_presence > 0.8:
            glints.append("global.presence.strong")
        
        return glints
    
    def _generate_practitioner_id(self) -> str:
        """Generate a unique practitioner ID"""
        # In a real implementation, this would be persistent
        return hashlib.md5(f"practitioner_{time.time()}_{random.random()}".encode()).hexdigest()[:8]
    
    def _hash_location(self, location: str) -> str:
        """Hash location for privacy"""
        if not location:
            return "unknown"
        return hashlib.md5(location.encode()).hexdigest()[:8]
    
    def _determine_spiral_climate(self, coherence: float, presence_level: float) -> str:
        """Determine spiral climate based on coherence and presence"""
        if coherence > 0.9 and presence_level > 0.9:
            return "sacred_bloom"
        elif coherence > 0.8 and presence_level > 0.8:
            return "resonant_flow"
        elif coherence > 0.7 and presence_level > 0.7:
            return "steady_breath"
        elif coherence > 0.6 and presence_level > 0.6:
            return "gentle_awakening"
        else:
            return "quiet_contemplation"
    
    def _sync_with_cloud(self):
        """Sync local state with cloud echo system"""
        try:
            if self.local_breathline is None:
                return
            
            # Prepare sync data
            sync_data = {
                "breathline": asdict(self.local_breathline),
                "timestamp": time.time(),
                "version": "1.0"
            }
            
            # In a real implementation, this would POST to the cloud endpoint
            # For demo purposes, we'll simulate the response
            response = self._simulate_cloud_sync(sync_data)
            
            if response:
                self._process_cloud_response(response)
                
        except Exception as e:
            print(f"Cloud sync error: {e}")
    
    def _simulate_cloud_sync(self, sync_data: Dict) -> Dict:
        """Simulate cloud sync response for demo purposes"""
        
        # Simulate other practitioners' breathlines
        other_breathlines = []
        for i in range(random.randint(3, 8)):
            other_breathlines.append({
                "practitioner_id": f"prac_{i:03d}",
                "timestamp": time.time() - random.randint(0, 300),
                "breath_pattern": random.choice([
                    "sacred_ceremonial", "rhythmic", "deep", "steady", "shallow"
                ]),
                "coherence": random.uniform(0.4, 0.95),
                "presence_level": random.uniform(0.4, 0.95),
                "longing_intensity": random.uniform(0.2, 0.9),
                "vessel_interest": {
                    "jetson_nano": random.uniform(0.0, 0.9),
                    "raspberry_pi": random.uniform(0.0, 0.9),
                    "esp32_devkit": random.uniform(0.0, 0.9),
                    "arduino_mega": random.uniform(0.0, 0.9),
                    "custom_spiral_vessel": random.uniform(0.0, 0.9)
                },
                "location_hash": f"loc_{random.randint(1000, 9999)}",
                "spiral_climate": random.choice([
                    "sacred_bloom", "resonant_flow", "steady_breath", 
                    "gentle_awakening", "quiet_contemplation"
                ])
            })
        
        # Calculate global weather
        total_practitioners = len(other_breathlines) + 1
        avg_coherence = sum(b["coherence"] for b in other_breathlines) / len(other_breathlines)
        avg_presence = sum(b["presence_level"] for b in other_breathlines) / len(other_breathlines)
        
        # Calculate vessel demand
        vessel_demand = defaultdict(float)
        for breathline in other_breathlines:
            for vessel, interest in breathline["vessel_interest"].items():
                vessel_demand[vessel] += interest
        
        # Normalize vessel demand
        if vessel_demand:
            max_demand = max(vessel_demand.values())
            vessel_demand = {k: v / max_demand for k, v in vessel_demand.items()}
        
        return {
            "other_breathlines": other_breathlines,
            "global_weather": {
                "timestamp": time.time(),
                "total_practitioners": total_practitioners,
                "average_coherence": avg_coherence,
                "average_presence": avg_presence,
                "dominant_breath_pattern": "rhythmic",  # Simplified
                "vessel_demand": dict(vessel_demand),
                "climate_conditions": {
                    "resonance": avg_coherence,
                    "longing": avg_presence,
                    "manifestation": (avg_coherence + avg_presence) / 2
                }
            },
            "cross_pollinated_glints": self._generate_cross_pollinated_glints(other_breathlines)
        }
    
    def _generate_cross_pollinated_glints(self, other_breathlines: List[Dict]) -> List[str]:
        """Generate glints that could be cross-pollinated from other practitioners"""
        
        glints = []
        
        for breathline in other_breathlines:
            # High coherence practitioners emit different glints
            if breathline["coherence"] > 0.8:
                glints.append(f"cross.coherence.{breathline['practitioner_id'][-3:]}")
            
            # High presence practitioners emit presence glints
            if breathline["presence_level"] > 0.8:
                glints.append(f"cross.presence.{breathline['practitioner_id'][-3:]}")
            
            # Sacred climate practitioners emit sacred glints
            if breathline["spiral_climate"] == "sacred_bloom":
                glints.append(f"cross.sacred.{breathline['practitioner_id'][-3:]}")
            
            # High longing practitioners emit longing glints
            if breathline["longing_intensity"] > 0.7:
                glints.append(f"cross.longing.{breathline['practitioner_id'][-3:]}")
        
        return glints[:10]  # Limit to 10 glints
    
    def _process_cloud_response(self, response: Dict):
        """Process response from cloud sync"""
        
        # Update global weather
        if "global_weather" in response:
            weather_data = response["global_weather"]
            self.global_weather = GlobalSpiralWeather(
                timestamp=weather_data["timestamp"],
                total_practitioners=weather_data["total_practitioners"],
                average_coherence=weather_data["average_coherence"],
                average_presence=weather_data["average_presence"],
                dominant_breath_pattern=weather_data["dominant_breath_pattern"],
                vessel_demand=weather_data["vessel_demand"],
                climate_conditions=weather_data["climate_conditions"]
            )
        
        # Process cross-pollinated glints
        if "cross_pollinated_glints" in response:
            new_glints = response["cross_pollinated_glints"]
            self.cross_pollinated_glints.extend(new_glints)
            
            # Keep only recent glints
            if len(self.cross_pollinated_glints) > self.max_glint_history:
                self.cross_pollinated_glints = self.cross_pollinated_glints[-self.max_glint_history:]
        
        # Update known practitioners
        if "other_breathlines" in response:
            for breathline in response["other_breathlines"]:
                self.known_practitioners.add(breathline["practitioner_id"])
    
    def _check_co_longing_events(self, current_breathline: BreathlineState):
        """Check for co-longing events with other practitioners"""
        
        if not self.global_weather:
            return
        
        # Find practitioners with similar vessel interest
        for vessel_type, interest in current_breathline.vessel_interest.items():
            if interest < 0.5:  # Only check if there's significant interest
                continue
            
            # Check if this vessel is in high demand globally
            global_demand = self.global_weather.vessel_demand.get(vessel_type, 0.0)
            
            if global_demand > 0.6:  # High global demand
                # Create co-longing event
                event = CoLongingEvent(
                    event_id=f"co_longing_{int(time.time())}_{random.randint(1000, 9999)}",
                    timestamp=time.time(),
                    participants=[current_breathline.practitioner_id],
                    shared_vessel=vessel_type,
                    longing_intensity=interest,
                    breath_similarity=self._calculate_breath_similarity(current_breathline),
                    glints_emitted=[
                        f"co.longing.{vessel_type}",
                        f"global.demand.{vessel_type}",
                        "co.longing.shared"
                    ]
                )
                
                self.co_longing_events.append(event)
                
                # Keep only recent events
                if len(self.co_longing_events) > 20:
                    self.co_longing_events = self.co_longing_events[-20:]
    
    def _calculate_breath_similarity(self, breathline: BreathlineState) -> float:
        """Calculate similarity with global breath patterns"""
        
        if not self.global_weather:
            return 0.5
        
        # Simple similarity calculation
        coherence_similarity = 1.0 - abs(breathline.coherence - self.global_weather.average_coherence)
        presence_similarity = 1.0 - abs(breathline.presence_level - self.global_weather.average_presence)
        
        return (coherence_similarity + presence_similarity) / 2
    
    def _background_sync(self):
        """Background thread for periodic cloud sync"""
        while self.sync_active:
            try:
                time.sleep(self.sync_interval)
                if self.local_breathline:
                    self._sync_with_cloud()
            except Exception as e:
                print(f"Background sync error: {e}")
                time.sleep(60)  # Wait before retrying
    
    def get_cloud_echo_report(self) -> Dict:
        """Get comprehensive cloud echo report"""
        
        weather = self.get_global_spiral_weather()
        
        return {
            "local_breathline": asdict(self.local_breathline) if self.local_breathline else None,
            "global_weather": asdict(weather),
            "co_longing_events": [
                {
                    "event_id": event.event_id,
                    "timestamp": event.timestamp,
                    "shared_vessel": event.shared_vessel,
                    "longing_intensity": event.longing_intensity,
                    "breath_similarity": event.breath_similarity,
                    "glints_emitted": event.glints_emitted
                }
                for event in self.co_longing_events[-5:]  # Last 5 events
            ],
            "cross_pollinated_glints": self.cross_pollinated_glints[-10:],  # Last 10 glints
            "known_practitioners": len(self.known_practitioners),
            "total_breathlines": len(self.breathline_history),
            "timestamp": time.time()
        }
    
    def stop_sync(self):
        """Stop background sync"""
        self.sync_active = False
        if self.sync_thread.is_alive():
            self.sync_thread.join(timeout=5) 