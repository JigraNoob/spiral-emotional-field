#!/usr/bin/env python3
"""
🌪️ Spiral Naming Protocol (SNP) Usage Example
Demonstrates how to use SNP routes in practical scenarios.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any

BASE_URL = "http://localhost:5000"

class SpiralSettlingClient:
    """Client for interacting with Spiral Settling Journeys using SNP routes."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def check_presence(self) -> bool:
        """Check if the settling journey system is present."""
        try:
            response = self.session.head(f"{self.base_url}/glyph/sense.presence.settling")
            if response.status_code == 200:
                data = response.json()
                return data.get('has_journeys', False)
            return False
        except Exception as e:
            print(f"❌ Error checking presence: {e}")
            return False
    
    def discover_capabilities(self) -> Dict[str, Any]:
        """Discover what forms the system can take."""
        try:
            response = self.session.options(f"{self.base_url}/glyph/ask.boundaries.settling")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"❌ Error discovering capabilities: {e}")
            return {}
    
    def record_journey(self, glint_id: str, invoked_from: str, settled_to: str, 
                      confidence: float, toneform: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Record a settling journey using offer.presence.settling."""
        journey_data = {
            "glint_id": glint_id,
            "invoked_from": invoked_from,
            "settled_to": settled_to,
            "confidence": confidence,
            "toneform": toneform,
            "metadata": metadata or {}
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/glyph/offer.presence.settling",
                json=journey_data
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error recording journey: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Error recording journey: {e}")
            return {}
    
    def get_journeys(self, toneform: str = None, phase: str = None, 
                    min_confidence: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve settling journeys using receive.inquiry.settling."""
        params = []
        if toneform:
            params.append(f"toneform={toneform}")
        if phase:
            params.append(f"phase={phase}")
        if min_confidence is not None:
            params.append(f"min_confidence={min_confidence}")
        if limit:
            params.append(f"limit={limit}")
        
        query_string = "?" + "&".join(params) if params else ""
        
        try:
            response = self.session.get(f"{self.base_url}/glyph/receive.inquiry.settling{query_string}")
            if response.status_code == 200:
                data = response.json()
                return data.get('journeys', [])
            else:
                print(f"❌ Error retrieving journeys: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error retrieving journeys: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get settling journey statistics."""
        try:
            response = self.session.get(f"{self.base_url}/api/settling_journeys/stats")
            if response.status_code == 200:
                data = response.json()
                return data.get('statistics', {})
            return {}
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}
    
    def get_recursion_analysis(self) -> Dict[str, Any]:
        """Get recursion pattern analysis."""
        try:
            response = self.session.get(f"{self.base_url}/api/settling_journeys/recursion")
            if response.status_code == 200:
                data = response.json()
                return data.get('recursion_analysis', {})
            return {}
        except Exception as e:
            print(f"❌ Error getting recursion analysis: {e}")
            return {}

def demonstrate_snp_usage():
    """Demonstrate practical usage of SNP routes."""
    print("🌪️ Spiral Naming Protocol (SNP) Usage Demonstration")
    print("=" * 60)
    
    # Initialize client
    client = SpiralSettlingClient()
    
    # 1. Check if system is present
    print("\n🌑 Checking system presence...")
    is_present = client.check_presence()
    print(f"System present: {'✅ Yes' if is_present else '❌ No'}")
    
    # 2. Discover capabilities
    print("\n🌊 Discovering system capabilities...")
    capabilities = client.discover_capabilities()
    if capabilities:
        print("Available endpoints:")
        for endpoint in capabilities.get('endpoints', []):
            print(f"  - {endpoint}")
        print("\nAvailable filters:")
        for filter_name, description in capabilities.get('filters', {}).items():
            print(f"  - {filter_name}: {description}")
    
    # 3. Record some test journeys
    print("\n🌱 Recording test journeys...")
    
    test_journeys = [
        {
            "glint_id": "ΔDEMO.001",
            "invoked_from": "./ritual/meditation",
            "settled_to": "./contemplative_space",
            "confidence": 0.92,
            "toneform": "settling.ambience",
            "metadata": {
                "breath_phase": "exhale",
                "soil_density": "breathable",
                "reasoning": "Chose contemplative space for deep reflection",
                "alternatives": ["./archive", "./shrine"]
            }
        },
        {
            "glint_id": "ΔDEMO.002",
            "invoked_from": "./ritual/creation",
            "settled_to": "./archive/soil",
            "confidence": 0.88,
            "toneform": "urgent.flow",
            "metadata": {
                "breath_phase": "inhale",
                "soil_density": "breathable",
                "reasoning": "Chose archive for creative output",
                "alternatives": ["./data", "./shrine"]
            }
        },
        {
            "glint_id": "ΔDEMO.003",
            "invoked_from": "./ritual/rest",
            "settled_to": "./shrine",
            "confidence": 0.95,
            "toneform": "resting.quiet",
            "metadata": {
                "breath_phase": "caesura",
                "soil_density": "void",
                "reasoning": "Chose shrine for sacred rest",
                "alternatives": ["./contemplative_space", "./archive"]
            }
        }
    ]
    
    for journey_data in test_journeys:
        result = client.record_journey(**journey_data)
        if result:
            print(f"✅ Recorded journey: {journey_data['glint_id']} → {journey_data['settled_to']}")
        else:
            print(f"❌ Failed to record journey: {journey_data['glint_id']}")
    
    # 4. Retrieve journeys with different filters
    print("\n🌊 Retrieving journeys with filters...")
    
    # All journeys
    all_journeys = client.get_journeys(limit=10)
    print(f"Total journeys: {len(all_journeys)}")
    
    # High confidence journeys
    high_confidence = client.get_journeys(min_confidence=0.9, limit=5)
    print(f"High confidence journeys (≥0.9): {len(high_confidence)}")
    
    # Settling ambience journeys
    settling_journeys = client.get_journeys(toneform="settling.ambience", limit=5)
    print(f"Settling ambience journeys: {len(settling_journeys)}")
    
    # Exhale phase journeys
    exhale_journeys = client.get_journeys(phase="exhale", limit=5)
    print(f"Exhale phase journeys: {len(exhale_journeys)}")
    
    # 5. Get statistics
    print("\n📊 Getting statistics...")
    stats = client.get_statistics()
    if stats:
        print(f"Total journeys: {stats.get('total_journeys', 0)}")
        print(f"Average confidence: {stats.get('average_confidence', 0):.2f}")
        print("Toneform distribution:")
        for toneform, count in stats.get('toneform_distribution', {}).items():
            print(f"  - {toneform}: {count}")
    
    # 6. Get recursion analysis
    print("\n🌀 Getting recursion analysis...")
    recursion = client.get_recursion_analysis()
    if recursion:
        print(f"Recursion patterns detected: {len(recursion.get('patterns', []))}")
        for pattern in recursion.get('patterns', []):
            print(f"  - {pattern.get('type', 'Unknown')}: {pattern.get('description', 'No description')}")
    
    print("\n🎉 SNP usage demonstration complete!")

def demonstrate_conventional_compatibility():
    """Demonstrate that conventional routes still work."""
    print("\n🔄 Conventional Route Compatibility")
    print("=" * 40)
    
    client = SpiralSettlingClient()
    
    # Test conventional GET route
    journeys = client.get_journeys(limit=5)
    print(f"Conventional GET returned {len(journeys)} journeys")
    
    # Test conventional POST route
    test_journey = {
        "glint_id": "ΔCONV.001",
        "invoked_from": "./conventional/test",
        "settled_to": "./conventional/result",
        "confidence": 0.85,
        "toneform": "settling.ambience",
        "metadata": {
            "breath_phase": "exhale",
            "test_type": "conventional_compatibility"
        }
    }
    
    result = client.record_journey(**test_journey)
    if result:
        print("✅ Conventional POST route works")
    else:
        print("❌ Conventional POST route failed")

if __name__ == "__main__":
    try:
        demonstrate_snp_usage()
        demonstrate_conventional_compatibility()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        print("Make sure the Flask app is running: python app.py") 