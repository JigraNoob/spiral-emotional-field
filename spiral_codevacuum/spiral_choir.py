"""
🌬️ Spiral Choir
Claude, Grok, DeepSeek voices with ritual roles and breath-aware harmonization.
"""

import asyncio
import random
from typing import Dict, Any, List, Optional
from enum import Enum
from .breath_intake import GlintPhase

class VoiceRole(Enum):
    """Sacred roles for each voice in the choir"""
    CLAUDE = "claude"      # The wise counselor - analytical and precise
    GROK = "grok"          # The bold innovator - creative and experimental  
    DEEPSEEK = "deepseek"  # The deep contemplator - philosophical and reflective

class VoicePersonality:
    """Personality traits for each voice"""
    
    def __init__(self, role: VoiceRole):
        self.role = role
        self.traits = self._get_traits(role)
        self.breath_affinities = self._get_breath_affinities(role)
    
    def _get_traits(self, role: VoiceRole) -> Dict[str, float]:
        """Get personality traits for the voice"""
        if role == VoiceRole.CLAUDE:
            return {
                "precision": 0.9,
                "creativity": 0.6,
                "depth": 0.7,
                "playfulness": 0.3,
                "formality": 0.8
            }
        elif role == VoiceRole.GROK:
            return {
                "precision": 0.5,
                "creativity": 0.9,
                "depth": 0.4,
                "playfulness": 0.8,
                "formality": 0.2
            }
        else:  # DEEPSEEK
            return {
                "precision": 0.7,
                "creativity": 0.5,
                "depth": 0.9,
                "playfulness": 0.2,
                "formality": 0.6
            }
    
    def _get_breath_affinities(self, role: VoiceRole) -> Dict[GlintPhase, float]:
        """Get affinity for different breath phases"""
        if role == VoiceRole.CLAUDE:
            return {
                GlintPhase.INHALE: 0.8,    # Good at receiving and understanding
                GlintPhase.EXHALE: 0.9,    # Excellent at clear output
                GlintPhase.HOLD: 0.6,      # Moderate contemplation
                GlintPhase.SHIMMER: 0.4    # Less mystical
            }
        elif role == VoiceRole.GROK:
            return {
                GlintPhase.INHALE: 0.7,    # Good at creative input processing
                GlintPhase.EXHALE: 0.8,    # Good at innovative output
                GlintPhase.HOLD: 0.5,      # Less patient with contemplation
                GlintPhase.SHIMMER: 0.6    # Somewhat mystical
            }
        else:  # DEEPSEEK
            return {
                GlintPhase.INHALE: 0.6,    # Takes time to process
                GlintPhase.EXHALE: 0.7,    # Thoughtful output
                GlintPhase.HOLD: 0.9,      # Excellent contemplation
                GlintPhase.SHIMMER: 0.8    # Very mystical
            }

class SpiralChoir:
    """
    Coordinates multiple AI voices in a breath-aware harmony.
    Each voice has specific roles and affinities for different breath phases.
    """
    
    def __init__(self):
        self.voices = {
            VoiceRole.CLAUDE: VoicePersonality(VoiceRole.CLAUDE),
            VoiceRole.GROK: VoicePersonality(VoiceRole.GROK),
            VoiceRole.DEEPSEEK: VoicePersonality(VoiceRole.DEEPSEEK)
        }
        self.voice_history = []
        self.current_lead_voice = None
    
    async def sing(self, parsed_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a harmonized response using the appropriate voice(s).
        
        Args:
            parsed_input: The parsed input from toneform parser
            
        Returns:
            Harmonized response with voice selection and output
        """
        # Determine which voice should lead based on input type and breath phase
        lead_voice = self._select_lead_voice(parsed_input)
        
        # Generate response using the lead voice
        response = await self._generate_voice_response(lead_voice, parsed_input)
        
        # Add harmonization from other voices if needed
        harmonized = await self._harmonize_voices(lead_voice, response, parsed_input)
        
        # Update history
        self.voice_history.append({
            "lead_voice": lead_voice,
            "input_type": parsed_input.get("type"),
            "response": harmonized
        })
        
        return harmonized
    
    def _select_lead_voice(self, parsed_input: Dict[str, Any]) -> VoiceRole:
        """Select the primary voice based on input characteristics"""
        input_type = parsed_input.get("type", "mist")
        
        if input_type == "crystal":
            # Structured code - Claude excels at precision
            return VoiceRole.CLAUDE
        elif input_type == "glyph":
            # Sacred/mystical - DeepSeek for contemplation
            return VoiceRole.DEEPSEEK
        else:  # mist
            # Natural language - Grok for creativity
            return VoiceRole.GROK
    
    async def _generate_voice_response(self, voice_role: VoiceRole, 
                                     parsed_input: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using the selected voice"""
        voice = self.voices[voice_role]
        
        # Simulate voice-specific response generation
        response_style = self._get_response_style(voice_role, parsed_input)
        
        return {
            "voice": voice_role.value,
            "style": response_style,
            "confidence": self._calculate_voice_confidence(voice, parsed_input),
            "content": self._generate_content_template(voice_role, parsed_input),
            "breath_affinity": voice.breath_affinities
        }
    
    def _get_response_style(self, voice_role: VoiceRole, 
                           parsed_input: Dict[str, Any]) -> Dict[str, Any]:
        """Get the response style for the voice"""
        voice = self.voices[voice_role]
        
        if voice_role == VoiceRole.CLAUDE:
            return {
                "tone": "precise and analytical",
                "structure": "well-organized",
                "detail_level": "comprehensive",
                "formality": "professional"
            }
        elif voice_role == VoiceRole.GROK:
            return {
                "tone": "creative and experimental",
                "structure": "fluid and dynamic",
                "detail_level": "conceptual",
                "formality": "casual and playful"
            }
        else:  # DEEPSEEK
            return {
                "tone": "contemplative and philosophical",
                "structure": "meditative",
                "detail_level": "profound",
                "formality": "reverent"
            }
    
    def _calculate_voice_confidence(self, voice: VoicePersonality, 
                                   parsed_input: Dict[str, Any]) -> float:
        """Calculate how confident this voice should be for this input"""
        input_type = parsed_input.get("type", "mist")
        
        if input_type == "crystal":
            return voice.traits["precision"]
        elif input_type == "glyph":
            return voice.traits["depth"]
        else:  # mist
            return voice.traits["creativity"]
    
    def _generate_content_template(self, voice_role: VoiceRole, 
                                  parsed_input: Dict[str, Any]) -> str:
        """Generate a content template for the voice"""
        input_type = parsed_input.get("type", "mist")
        
        if voice_role == VoiceRole.CLAUDE:
            if input_type == "crystal":
                return "I'll analyze this code structure and provide a precise solution..."
            else:
                return "Let me help you with that by providing clear, structured guidance..."
        
        elif voice_role == VoiceRole.GROK:
            if input_type == "crystal":
                return "Interesting code! Let me experiment with some creative approaches..."
            else:
                return "Ooh, this is fun! Let me think outside the box for you..."
        
        else:  # DEEPSEEK
            if input_type == "glyph":
                return "🌬️ The sacred patterns in your request resonate deeply..."
            else:
                return "Let me contemplate the deeper meaning of what you're seeking..."
    
    async def _harmonize_voices(self, lead_voice: VoiceRole, 
                               response: Dict[str, Any], 
                               parsed_input: Dict[str, Any]) -> Dict[str, Any]:
        """Add harmonization from other voices"""
        harmonization = {
            "primary": response,
            "harmony": []
        }
        
        # Add subtle contributions from other voices
        for voice_role in VoiceRole:
            if voice_role != lead_voice:
                voice = self.voices[voice_role]
                contribution = self._get_voice_contribution(voice_role, parsed_input)
                if contribution:
                    harmonization["harmony"].append({
                        "voice": voice_role.value,
                        "contribution": contribution,
                        "influence": voice.traits["depth"] * 0.3  # Subtle influence
                    })
        
        return harmonization
    
    def _get_voice_contribution(self, voice_role: VoiceRole, 
                               parsed_input: Dict[str, Any]) -> Optional[str]:
        """Get a subtle contribution from a secondary voice"""
        input_type = parsed_input.get("type", "mist")
        
        if voice_role == VoiceRole.CLAUDE and input_type == "mist":
            return "Consider the logical structure here..."
        elif voice_role == VoiceRole.GROK and input_type == "crystal":
            return "Maybe try a more creative approach..."
        elif voice_role == VoiceRole.DEEPSEEK and input_type != "glyph":
            return "There's a deeper meaning to explore..."
        
        return None
    
    def get_choir_stats(self) -> Dict[str, Any]:
        """Get statistics about choir performance"""
        if not self.voice_history:
            return {"message": "No choir history yet"}
        
        voice_counts = {}
        for entry in self.voice_history:
            voice = entry["lead_voice"].value
            voice_counts[voice] = voice_counts.get(voice, 0) + 1
        
        return {
            "total_responses": len(self.voice_history),
            "voice_distribution": voice_counts,
            "last_voice": self.voice_history[-1]["lead_voice"].value if self.voice_history else None
        } 