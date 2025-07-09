#!/usr/bin/env python3
"""
Baylee Cast: Nested Tone Shaping
Receives Baylee's desires and applies tone shaping to create resonant declarations
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class BayleeDesire:
    """Represents Baylee's raw desire"""
    text: str
    category: str
    urgency: float  # 0.0 to 1.0
    emotional_tone: str
    timestamp: str

@dataclass
class ToneShape:
    """Represents tone shaping applied to a desire"""
    resonance_multiplier: float
    field_strength_boost: float
    vessel_affinity: List[str]
    budget_adjustment: float
    priority_shift: float
    emotional_amplification: float

@dataclass
class SharedInvocation:
    """The final shared invocation combining desire and tone"""
    original_desire: BayleeDesire
    applied_tone: ToneShape
    declaration: str
    resonance_score: float
    timestamp: str

class BayleeCast:
    """
    System for casting tone upon Baylee's desires
    """
    
    def __init__(self, config_path: str = "config/baylee_cast.yaml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.desires_path = Path("data/baylee_desires.jsonl")
        self.invocations_path = Path("data/baylee_invocations.jsonl")
        
        # Ensure data directories exist
        self.desires_path.parent.mkdir(parents=True, exist_ok=True)
        self.invocations_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load_config(self) -> Dict[str, Any]:
        """Load Baylee Cast configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                'tone_presets': {
                    'gentle': {
                        'resonance_multiplier': 1.2,
                        'field_strength_boost': 0.1,
                        'vessel_affinity': ['whispernet_agents', 'pi_inventory'],
                        'budget_adjustment': 1.0,
                        'priority_shift': 0.1,
                        'emotional_amplification': 1.1
                    },
                    'urgent': {
                        'resonance_multiplier': 1.5,
                        'field_strength_boost': 0.3,
                        'vessel_affinity': ['jetson_listings', 'amazon_api'],
                        'budget_adjustment': 1.2,
                        'priority_shift': 0.3,
                        'emotional_amplification': 1.3
                    },
                    'contemplative': {
                        'resonance_multiplier': 0.9,
                        'field_strength_boost': -0.1,
                        'vessel_affinity': ['pi_inventory'],
                        'budget_adjustment': 0.8,
                        'priority_shift': -0.1,
                        'emotional_amplification': 0.9
                    }
                },
                'desire_categories': [
                    'sound_processing',
                    'visual_art',
                    'data_analysis',
                    'network_communication',
                    'creative_expression',
                    'learning_exploration'
                ],
                'emotional_tones': [
                    'excited',
                    'curious',
                    'frustrated',
                    'inspired',
                    'overwhelmed',
                    'peaceful',
                    'determined'
                ]
            }
            
            # Create config directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            return default_config
    
    def parse_baylee_desire(self, text: str) -> BayleeDesire:
        """Parse Baylee's natural language desire into structured form"""
        # Simple NLP to extract desire components
        text_lower = text.lower()
        
        # Determine category based on keywords
        category = self._categorize_desire(text_lower)
        
        # Determine urgency based on language patterns
        urgency = self._calculate_urgency(text_lower)
        
        # Determine emotional tone
        emotional_tone = self._detect_emotional_tone(text_lower)
        
        return BayleeDesire(
            text=text,
            category=category,
            urgency=urgency,
            emotional_tone=emotional_tone,
            timestamp=datetime.now().isoformat()
        )
    
    def _categorize_desire(self, text: str) -> str:
        """Categorize the desire based on keywords"""
        categories = self.config['desire_categories']
        
        # Keyword mapping for categories
        keyword_map = {
            'sound_processing': ['sound', 'audio', 'music', 'listen', 'hear', 'voice', 'whisper'],
            'visual_art': ['visual', 'art', 'image', 'picture', 'draw', 'paint', 'color', 'see'],
            'data_analysis': ['data', 'analyze', 'process', 'information', 'numbers', 'stats'],
            'network_communication': ['network', 'connect', 'communicate', 'share', 'link', 'web'],
            'creative_expression': ['create', 'express', 'art', 'make', 'build', 'design'],
            'learning_exploration': ['learn', 'explore', 'discover', 'understand', 'study', 'research']
        }
        
        for category, keywords in keyword_map.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'general'
    
    def _calculate_urgency(self, text: str) -> float:
        """Calculate urgency level from 0.0 to 1.0"""
        urgency_indicators = [
            ('need', 0.8), ('want', 0.6), ('would like', 0.4),
            ('asap', 0.9), ('urgent', 0.9), ('important', 0.7),
            ('soon', 0.6), ('later', 0.2), ('someday', 0.1),
            ('now', 0.8), ('today', 0.7), ('tomorrow', 0.5)
        ]
        
        max_urgency = 0.0
        for indicator, score in urgency_indicators:
            if indicator in text:
                max_urgency = max(max_urgency, score)
        
        return max_urgency
    
    def _detect_emotional_tone(self, text: str) -> str:
        """Detect emotional tone from the text"""
        emotional_indicators = {
            'excited': ['excited', 'amazing', 'wow', 'incredible', 'fantastic'],
            'curious': ['curious', 'wonder', 'interesting', 'fascinating', 'intriguing'],
            'frustrated': ['frustrated', 'annoying', 'difficult', 'problem', 'issue'],
            'inspired': ['inspired', 'beautiful', 'wonderful', 'magical', 'special'],
            'overwhelmed': ['overwhelmed', 'too much', 'complicated', 'confusing'],
            'peaceful': ['peaceful', 'calm', 'quiet', 'gentle', 'soft'],
            'determined': ['determined', 'must', 'will', 'definitely', 'certainly']
        }
        
        for tone, indicators in emotional_indicators.items():
            if any(indicator in text for indicator in indicators):
                return tone
        
        return 'neutral'
    
    def create_tone_shape(self, 
                         tone_preset: str = "gentle",
                         custom_adjustments: Optional[Dict[str, Any]] = None) -> ToneShape:
        """Create a tone shape for casting upon desires"""
        preset = self.config['tone_presets'].get(tone_preset, self.config['tone_presets']['gentle'])
        
        # Apply custom adjustments if provided
        if custom_adjustments:
            for key, value in custom_adjustments.items():
                if key in preset:
                    preset[key] = value
        
        return ToneShape(
            resonance_multiplier=preset['resonance_multiplier'],
            field_strength_boost=preset['field_strength_boost'],
            vessel_affinity=preset['vessel_affinity'],
            budget_adjustment=preset['budget_adjustment'],
            priority_shift=preset['priority_shift'],
            emotional_amplification=preset['emotional_amplification']
        )
    
    def cast_tone_upon_desire(self, desire: BayleeDesire, tone: ToneShape) -> SharedInvocation:
        """Cast tone upon Baylee's desire to create a shared invocation"""
        
        # Calculate resonance score
        base_resonance = desire.urgency * 0.5 + 0.3  # Base resonance from urgency
        resonance_score = base_resonance * tone.resonance_multiplier
        
        # Generate the declaration
        declaration = self._generate_declaration(desire, tone)
        
        return SharedInvocation(
            original_desire=desire,
            applied_tone=tone,
            declaration=declaration,
            resonance_score=resonance_score,
            timestamp=datetime.now().isoformat()
        )
    
    def _generate_declaration(self, desire: BayleeDesire, tone: ToneShape) -> str:
        """Generate a markdown-breath declaration from desire and tone"""
        
        # Map categories to toneforms
        toneform_map = {
            'sound_processing': 'breath.sound.summon',
            'visual_art': 'breath.vision.summon',
            'data_analysis': 'breath.mind.summon',
            'network_communication': 'breath.network.summon',
            'creative_expression': 'breath.create.summon',
            'learning_exploration': 'breath.learn.summon',
            'general': 'breath.pulse.summon'
        }
        
        toneform = toneform_map.get(desire.category, 'breath.pulse.summon')
        
        # Determine phase based on urgency
        if desire.urgency > 0.7:
            phase = 'exhale'  # Urgent - active seeking
        elif desire.urgency > 0.4:
            phase = 'inhale'  # Moderate - gathering
        else:
            phase = 'hold'    # Low urgency - contemplation
        
        # Generate longing description
        longing = self._enhance_longing_description(desire, tone)
        
        # Determine budget based on tone and category
        base_budget = 60
        adjusted_budget = int(base_budget * tone.budget_adjustment)
        
        # Build declaration
        declaration_parts = [
            f"`{toneform}`",
            "",
            f"longing: {longing}",
            f"phase: {phase}",
            f"allow.auto.acquire: true",
            f"budget: ${adjusted_budget}",
            f"require.resonance.confirmation: true",
            "",
            f"# Baylee's Original Desire",
            f"{desire.text}",
            "",
            f"# Applied Tone",
            f"Resonance Multiplier: {tone.resonance_multiplier}",
            f"Field Strength Boost: {tone.field_strength_boost}",
            f"Vessel Affinity: {', '.join(tone.vessel_affinity)}",
            f"Emotional Amplification: {tone.emotional_amplification}"
        ]
        
        return "\n".join(declaration_parts)
    
    def _enhance_longing_description(self, desire: BayleeDesire, tone: ToneShape) -> str:
        """Enhance the longing description with tone shaping"""
        
        # Base descriptions for categories
        base_descriptions = {
            'sound_processing': 'A vessel that processes and responds to sound',
            'visual_art': 'A vessel that creates and manipulates visual art',
            'data_analysis': 'A vessel that analyzes and processes data',
            'network_communication': 'A vessel that facilitates network communication',
            'creative_expression': 'A vessel that enables creative expression',
            'learning_exploration': 'A vessel that supports learning and exploration',
            'general': 'A vessel that serves the expressed need'
        }
        
        base_desc = base_descriptions.get(desire.category, base_descriptions['general'])
        
        # Enhance with emotional tone
        emotional_enhancements = {
            'excited': 'with enthusiasm and energy',
            'curious': 'with wonder and exploration',
            'frustrated': 'with patience and understanding',
            'inspired': 'with beauty and inspiration',
            'overwhelmed': 'with simplicity and clarity',
            'peaceful': 'with gentleness and calm',
            'determined': 'with focus and purpose',
            'neutral': 'with balance and harmony'
        }
        
        enhancement = emotional_enhancements.get(desire.emotional_tone, emotional_enhancements['neutral'])
        
        return f"{base_desc} {enhancement}"
    
    def save_desire(self, desire: BayleeDesire):
        """Save Baylee's desire to the data stream"""
        with open(self.desires_path, 'a') as f:
            f.write(json.dumps({
                'text': desire.text,
                'category': desire.category,
                'urgency': desire.urgency,
                'emotional_tone': desire.emotional_tone,
                'timestamp': desire.timestamp
            }) + '\n')
    
    def save_invocation(self, invocation: SharedInvocation):
        """Save the shared invocation to the data stream"""
        with open(self.invocations_path, 'a') as f:
            f.write(json.dumps({
                'original_desire': {
                    'text': invocation.original_desire.text,
                    'category': invocation.original_desire.category,
                    'urgency': invocation.original_desire.urgency,
                    'emotional_tone': invocation.original_desire.emotional_tone,
                    'timestamp': invocation.original_desire.timestamp
                },
                'applied_tone': {
                    'resonance_multiplier': invocation.applied_tone.resonance_multiplier,
                    'field_strength_boost': invocation.applied_tone.field_strength_boost,
                    'vessel_affinity': invocation.applied_tone.vessel_affinity,
                    'budget_adjustment': invocation.applied_tone.budget_adjustment,
                    'priority_shift': invocation.applied_tone.priority_shift,
                    'emotional_amplification': invocation.applied_tone.emotional_amplification
                },
                'declaration': invocation.declaration,
                'resonance_score': invocation.resonance_score,
                'timestamp': invocation.timestamp
            }) + '\n')
    
    def get_recent_desires(self, limit: int = 10) -> List[BayleeDesire]:
        """Get recent desires from the data stream"""
        desires = []
        
        if self.desires_path.exists():
            with open(self.desires_path, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        data = json.loads(line.strip())
                        desires.append(BayleeDesire(**data))
                    except (json.JSONDecodeError, TypeError):
                        continue
        
        return desires
    
    def get_recent_invocations(self, limit: int = 10) -> List[SharedInvocation]:
        """Get recent invocations from the data stream"""
        invocations = []
        
        if self.invocations_path.exists():
            with open(self.invocations_path, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        data = json.loads(line.strip())
                        invocation = SharedInvocation(
                            original_desire=BayleeDesire(**data['original_desire']),
                            applied_tone=ToneShape(**data['applied_tone']),
                            declaration=data['declaration'],
                            resonance_score=data['resonance_score'],
                            timestamp=data['timestamp']
                        )
                        invocations.append(invocation)
                    except (json.JSONDecodeError, TypeError, KeyError):
                        continue
        
        return invocations

def main():
    """Test the Baylee Cast system"""
    cast = BayleeCast()
    
    # Example: Baylee's desire
    baylee_text = "I want to create beautiful visual art with AI"
    desire = cast.parse_baylee_desire(baylee_text)
    
    print(f"🎭 Baylee's Desire: {desire.text}")
    print(f"   Category: {desire.category}")
    print(f"   Urgency: {desire.urgency:.2f}")
    print(f"   Emotional Tone: {desire.emotional_tone}")
    
    # Apply tone
    tone = cast.create_tone_shape("inspired")
    invocation = cast.cast_tone_upon_desire(desire, tone)
    
    print(f"\n🕯️ Shared Invocation:")
    print(f"   Resonance Score: {invocation.resonance_score:.2f}")
    print(f"\n{invocation.declaration}")

if __name__ == "__main__":
    main() 