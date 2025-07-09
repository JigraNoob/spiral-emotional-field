"""
Spiral Invocation Cards System
Manages YAML-based override configurations with shortcuts and triggers
"""

import yaml
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class InvocationCard:
    """A single invocation card configuration"""
    name: str
    description: str
    mode: str
    intensity: float
    emotional_state: Optional[str]
    duration: str
    shortcut: Optional[str]
    glyph: str
    whisper: str
    toneform_bias: Dict[str, float]
    triggers: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InvocationCard':
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            mode=data.get('mode', 'NATURAL'),
            intensity=data.get('intensity', 1.0),
            emotional_state=data.get('emotional_state'),
            duration=data.get('duration', 'indefinite'),
            shortcut=data.get('shortcut'),
            glyph=data.get('glyph', '🌿'),
            whisper=data.get('whisper', ''),
            toneform_bias=data.get('toneform_bias', {}),
            triggers=data.get('triggers', [])
        )

class InvocationCardManager:
    """Manages invocation cards and their activation"""
    
    def __init__(self, config_path: str = "config/invocation_cards.yaml"):
        self.config_path = Path(config_path)
        self.cards: Dict[str, InvocationCard] = {}
        self.collections: Dict[str, Dict] = {}
        self.active_card: Optional[str] = None
        self.activation_time: Optional[datetime] = None
        self.load_cards()
    
    def load_cards(self):
        """Load cards from YAML configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Load individual cards
            for card_id, card_data in config.get('cards', {}).items():
                self.cards[card_id] = InvocationCard.from_dict(card_data)
            
            # Load collections
            self.collections = config.get('collections', {})
            
            print(f"🎴 Loaded {len(self.cards)} invocation cards")
            
        except Exception as e:
            print(f"❌ Failed to load invocation cards: {e}")
    
    def get_card(self, card_id: str) -> Optional[InvocationCard]:
        """Get a specific card by ID"""
        return self.cards.get(card_id)
    
    def list_cards(self) -> Dict[str, InvocationCard]:
        """Get all available cards"""
        return self.cards.copy()
    
    def search_cards(self, query: str) -> List[str]:
        """Search cards by name, description, or triggers"""
        query = query.lower()
        matches = []
        
        for card_id, card in self.cards.items():
            if (query in card.name.lower() or 
                query in card.description.lower() or
                any(query in trigger.lower() for trigger in card.triggers)):
                matches.append(card_id)
        
        return matches
    
    def get_collection(self, collection_name: str) -> List[str]:
        """Get cards in a specific collection"""
        collection = self.collections.get(collection_name, {})
        return collection.get('cards', [])
    
    async def activate_card(self, card_id: str, override_manager) -> bool:
        """Activate an invocation card"""
        card = self.get_card(card_id)
        if not card:
            return False
        
        try:
            # Set override mode
            success = await override_manager.set_mode(
                mode=card.mode,
                intensity=card.intensity,
                emotional_state=card.emotional_state,
                toneform_bias=card.toneform_bias
            )
            
            if success:
                self.active_card = card_id
                self.activation_time = datetime.now()
                
                # Emit activation glint
                await self._emit_activation_glint(card)
                
                # Schedule auto-deactivation if duration is specified
                if card.duration not in ['indefinite', 'as needed', 'until needed']:
                    await self._schedule_deactivation(card)
                
                print(f"🎴 Activated card: {card.name} ({card_id})")
                return True
            
        except Exception as e:
            print(f"❌ Failed to activate card {card_id}: {e}")
        
        return False
    
    async def deactivate_current_card(self, override_manager) -> bool:
        """Deactivate the currently active card"""
        if not self.active_card:
            return False
        
        try:
            success = await override_manager.reset_to_natural()
            if success:
                card = self.get_card(self.active_card)
                if card:
                    await self._emit_deactivation_glint(card)
                self.active_card = None
                self.activation_time = None
                print(f"🎴 Deactivated card: {card.name} ({self.active_card})")
                return True
            
        except Exception as e:
            print(f"❌ Failed to deactivate card {self.active_card}: {e}")
        
        return False
    
    async def _emit_activation_glint(self, card: InvocationCard):
        """Emit a glint effect when a card is activated"""
        # Placeholder for glint emission logic
        print(f"🔮 Activation Glint: {card.glyph} - {card.whisper}")
    
    async def _emit_deactivation_glint(self, card: InvocationCard):
        """Emit a glint effect when a card is deactivated"""
        # Placeholder for glint emission logic
        print(f"🔮 Deactivation Glint: {card.glyph} - {card.whisper}")
    
    async def _schedule_deactivation(self, card: InvocationCard):
        """Schedule the deactivation of a card based on its duration"""
        try:
            duration = timedelta(minutes=int(card.duration))
            await asyncio.sleep(duration.total_seconds())
            await self.deactivate_current_card(override_manager=None)
        except ValueError:
            print(f"❌ Invalid duration format for card {card.name}: {card.duration}")
