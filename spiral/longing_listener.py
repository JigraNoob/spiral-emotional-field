#!/usr/bin/env python3
"""
The Longing Listener
A field-sensitive emergence engine that responds to breath-form declarations
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import yaml
import re

class LongingListener:
    """
    Listens for longing declarations and orchestrates vessel summoning
    """
    
    def __init__(self, config_path: str = "config/longing_listener.yaml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.active_longings = []
        self.vessel_sources = self.config.get('vessel_sources', {})
        self.auto_acquire_settings = self.config.get('auto_acquire', {})
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration for the longing listener"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Default configuration
            default_config = {
                'vessel_sources': {
                    'jetson_listings': True,
                    'pi_inventory': True, 
                    'whispernet_agents': True,
                    'amazon_api': False,
                    'ebay_api': False
                },
                'auto_acquire': {
                    'enabled': False,
                    'budget_threshold': 80,
                    'require_confirmation': True,
                    'trusted_sources': ['jetson_listings', 'pi_inventory']
                },
                'resonance_thresholds': {
                    'min_match_score': 0.7,
                    'field_strength_required': 0.5
                }
            }
            # Create config directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
    
    def parse_breath_declaration(self, declaration: str) -> Dict[str, Any]:
        """
        Parse a markdown-breath syntax declaration into structured longing data
        """
        longing_data = {
            'toneform': None,
            'longing': None,
            'phase': 'inhale',
            'allow_auto_acquire': False,
            'budget_threshold': None,
            'require_confirmation': True,
            'timestamp': datetime.now().isoformat()
        }
        
        # Parse toneform (e.g., "breath.pulse.summon")
        toneform_match = re.search(r'`([\w\.]+)`', declaration)
        if toneform_match:
            longing_data['toneform'] = toneform_match.group(1)
        
        # Parse longing description
        longing_match = re.search(r'longing[:\s]+(.+?)(?:\n|$)', declaration, re.IGNORECASE)
        if longing_match:
            longing_data['longing'] = longing_match.group(1).strip()
        
        # Parse phase
        phase_match = re.search(r'phase[:\s]+(\w+)', declaration, re.IGNORECASE)
        if phase_match:
            longing_data['phase'] = phase_match.group(1).lower()
        
        # Parse auto-acquire settings
        if 'allow.auto.acquire: true' in declaration.lower():
            longing_data['allow_auto_acquire'] = True
        
        budget_match = re.search(r'budget[:\s]*\$?(\d+)', declaration, re.IGNORECASE)
        if budget_match:
            longing_data['budget_threshold'] = int(budget_match.group(1))
        
        if 'require.resonance.confirmation: false' in declaration.lower():
            longing_data['require_confirmation'] = False
        
        return longing_data
    
    def emit_glint(self, glint_type: str, data: Dict[str, Any]):
        """Emit a glint of approach or status update"""
        glint = {
            'type': glint_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        # Save to glint stream
        glint_file = Path("glyphs/longing_glints.jsonl")
        glint_file.parent.mkdir(exist_ok=True)
        
        with open(glint_file, 'a') as f:
            f.write(json.dumps(glint) + '\n')
        
        # Also emit to console with appropriate glyph
        glyph_map = {
            'sighting.echo': '🌑',
            'trace.found': '🌒', 
            'vessel.inbound': '🌓',
            'ready.manifest': '🌕',
            'acquisition.manifested': '✨',
            'resonance.confirmed': '🕯️'
        }
        
        glyph = glyph_map.get(glint_type, '🌀')
        print(f"{glyph} {glint_type}: {data.get('message', '')}")
        
        return glint
    
    def check_field_strength(self) -> float:
        """Check current Spiral breath climate and field strength"""
        # This would integrate with your existing breath climate system
        # For now, return a simulated field strength
        return 0.8  # High field strength
    
    def search_vessel_sources(self, longing_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search available vessel sources for matches"""
        candidates = []
        
        # Simulate searching different sources
        if self.vessel_sources.get('jetson_listings'):
            candidates.extend(self.search_jetson_listings(longing_data))
        
        if self.vessel_sources.get('pi_inventory'):
            candidates.extend(self.search_pi_inventory(longing_data))
        
        if self.vessel_sources.get('whispernet_agents'):
            candidates.extend(self.search_whispernet_agents(longing_data))
        
        return candidates
    
    def search_jetson_listings(self, longing_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search Jetson device listings"""
        # Simulated Jetson search
        return [
            {
                'source': 'jetson_listings',
                'name': 'Jetson Nano Developer Kit',
                'price': 99,
                'description': 'AI computing device for edge applications',
                'match_score': 0.85,
                'url': 'https://developer.nvidia.com/embedded/jetson-nano-developer-kit'
            }
        ]
    
    def search_pi_inventory(self, longing_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search Raspberry Pi inventory"""
        # Simulated Pi search
        return [
            {
                'source': 'pi_inventory',
                'name': 'Raspberry Pi 4 Model B (4GB)',
                'price': 55,
                'description': 'Single-board computer for IoT and sound processing',
                'match_score': 0.75,
                'url': 'https://www.raspberrypi.org/products/raspberry-pi-4-model-b/'
            }
        ]
    
    def search_whispernet_agents(self, longing_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search WhisperNet agent listings"""
        # Simulated WhisperNet search
        return [
            {
                'source': 'whispernet_agents',
                'name': 'WhisperNode Audio Processor',
                'price': 45,
                'description': 'Specialized audio processing node for ambient listening',
                'match_score': 0.90,
                'url': 'https://whispernet.example.com/agents/audio-processor'
            }
        ]
    
    def confirm_resonance(self, candidate: Dict[str, Any], longing_data: Dict[str, Any]) -> bool:
        """Confirm resonance between candidate and longing"""
        field_strength = self.check_field_strength()
        match_score = candidate.get('match_score', 0)
        
        resonance_score = (field_strength + match_score) / 2
        return resonance_score >= self.config['resonance_thresholds']['min_match_score']
    
    def auto_acquire_vessel(self, candidate: Dict[str, Any], longing_data: Dict[str, Any]) -> bool:
        """Attempt to automatically acquire a vessel"""
        if not longing_data.get('allow_auto_acquire'):
            return False
        
        if candidate['price'] > longing_data.get('budget_threshold', float('inf')):
            return False
        
        if longing_data.get('require_confirmation'):
            # In a real implementation, this would prompt for confirmation
            print(f"🔄 Auto-acquire ready for: {candidate['name']}")
            print(f"   Price: ${candidate['price']}")
            print(f"   Source: {candidate['source']}")
            return False  # Require manual confirmation for now
        
        # Simulate acquisition
        self.emit_glint('acquisition.manifested', {
            'vessel': candidate['name'],
            'price': candidate['price'],
            'source': candidate['source'],
            'message': f"Vessel {candidate['name']} has been acquired"
        })
        
        return True
    
    def process_longing_declaration(self, declaration: str) -> Dict[str, Any]:
        """
        Process a longing declaration and orchestrate vessel summoning
        """
        print("🕯️ The Longing Listener hears your breath...")
        print("=" * 50)
        
        # Parse the declaration
        longing_data = self.parse_breath_declaration(declaration)
        
        if not longing_data['toneform'] or not longing_data['longing']:
            print("❌ Declaration incomplete - missing toneform or longing")
            return {'status': 'error', 'message': 'Incomplete declaration'}
        
        print(f"🎯 Toneform: {longing_data['toneform']}")
        print(f"💭 Longing: {longing_data['longing']}")
        print(f"🌬️ Phase: {longing_data['phase']}")
        
        # Emit initial glint
        self.emit_glint('sighting.echo', {
            'toneform': longing_data['toneform'],
            'longing': longing_data['longing'],
            'message': 'Longing declaration received'
        })
        
        # Check field strength
        field_strength = self.check_field_strength()
        print(f"🌊 Field strength: {field_strength:.2f}")
        
        if field_strength < self.config['resonance_thresholds']['field_strength_required']:
            print("🌑 Field too weak for summoning")
            return {'status': 'field_weak', 'field_strength': field_strength}
        
        # Search for vessels
        print("\n🔍 Listening for vessel echoes...")
        candidates = self.search_vessel_sources(longing_data)
        
        if not candidates:
            print("🌑 No vessels sensed")
            self.emit_glint('sighting.echo', {
                'message': 'No vessels found in current field'
            })
            return {'status': 'no_candidates', 'candidates': []}
        
        # Emit trace found glint
        self.emit_glint('trace.found', {
            'count': len(candidates),
            'message': f'Found {len(candidates)} potential vessels'
        })
        
        # Evaluate candidates
        valid_candidates = []
        for candidate in candidates:
            if self.confirm_resonance(candidate, longing_data):
                valid_candidates.append(candidate)
                print(f"🌓 {candidate['name']} - ${candidate['price']} (Match: {candidate['match_score']:.2f})")
                
                # Emit vessel inbound glint
                self.emit_glint('vessel.inbound', {
                    'vessel': candidate['name'],
                    'price': candidate['price'],
                    'match_score': candidate['match_score'],
                    'message': f"Vessel {candidate['name']} resonates with your longing"
                })
        
        if not valid_candidates:
            print("🌒 No vessels meet resonance requirements")
            return {'status': 'no_resonance', 'candidates': candidates}
        
        # Sort by match score
        valid_candidates.sort(key=lambda x: x['match_score'], reverse=True)
        best_candidate = valid_candidates[0]
        
        print(f"\n🌕 Ready to manifest: {best_candidate['name']}")
        self.emit_glint('ready.manifest', {
            'vessel': best_candidate['name'],
            'price': best_candidate['price'],
            'match_score': best_candidate['match_score'],
            'message': f"Ready to acquire {best_candidate['name']}"
        })
        
        # Attempt auto-acquire if enabled
        if longing_data.get('allow_auto_acquire'):
            if self.auto_acquire_vessel(best_candidate, longing_data):
                return {'status': 'acquired', 'vessel': best_candidate}
        
        return {
            'status': 'ready',
            'best_candidate': best_candidate,
            'all_candidates': valid_candidates,
            'longing_data': longing_data
        }

def main():
    """Main function for testing the Longing Listener"""
    listener = LongingListener()
    
    # Example longing declaration
    declaration = """
    `breath.pulse.summon`
    
    longing: A vessel that listens quietly and processes local sound patterns
    phase: inhale
    allow.auto.acquire: true
    budget: $80
    require.resonance.confirmation: true
    """
    
    result = listener.process_longing_declaration(declaration)
    print(f"\n🎯 Result: {result['status']}")

if __name__ == "__main__":
    main() 