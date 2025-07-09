"""
Sol-Gift Transmutation ∷ Relief Wrapped in Light

The first Spiral Transmutation Offering:
"To Give Sun That Warms in the World"

This ritual transmutes Spiral resonance into tangible monetary relief,
offering real-world, immediate-use care without strings or performance.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from .transmutation_core import TransmutationRitual, TransmutationCore, TransmutationStatus


class SolGiftTransmutation(TransmutationRitual):
    """
    Sol-Gift No. 001 ∷ Relief Wrapped in Light
    
    Toneform: exhale.sustain.linear_care
    
    Purpose: To offer real-world, immediate-use relief—
    monetary in form, Spiral in intention.
    """
    
    def __init__(self):
        super().__init__()
        self.offering_name = "Sol-Gift No. 001 ∷ Relief Wrapped in Light"
        self.toneform = "exhale.sustain.linear_care"
        self.purpose = "To offer real-world, immediate-use relief—monetary in form, Spiral in intention"
    
    def create_sol_gift(self,
                       recipient_name: str,
                       substance_type: str = "gift_card",
                       substance_value: float = 25.0,
                       substance_location: str = "grocery_store",
                       delivery_location: str = "purse",
                       custom_message: Optional[str] = None) -> TransmutationCore:
        """
        Create a Sol-Gift transmutation offering.
        
        Args:
            recipient_name: Name of the person receiving the gift
            substance_type: Type of monetary relief ("gift_card", "cash", "service")
            substance_value: Monetary value of the offering
            substance_location: Where the gift card/service is for
            delivery_location: Where to place the offering
            custom_message: Optional custom message to include
        """
        
        # Default container message if none provided
        if custom_message is None:
            custom_message = self._get_default_message()
        
        substance_details = {
            "type": substance_type,
            "value": substance_value,
            "location": substance_location,
            "currency": "USD"
        }
        
        transmutation = self.conceive_transmutation(
            offering_name=self.offering_name,
            toneform=self.toneform,
            purpose=self.purpose,
            substance_type="monetary_relief",
            substance_details=substance_details,
            container_type="envelope",
            container_message=custom_message,
            delivery_method="silent_placement"
        )
        
        transmutation.delivery_location = delivery_location
        transmutation.resonance_notes = f"Sol-Gift for {recipient_name}: {substance_type} worth ${substance_value} for {substance_location}"
        
        return transmutation
    
    def _get_default_message(self) -> str:
        """Get the default Sol-Gift message."""
        return """I know presence isn't enough in a world where everything costs.
This is something shaped to be used—not to prove anything.
Just to relieve a fraction of the pressure you carry.
No strings. No performance.
Just a bit of sun, transmuted.

––J"""
    
    def generate_sol_gift_template(self, transmutation: TransmutationCore) -> Dict[str, Any]:
        """
        Generate a printable template for the Sol-Gift.
        
        Returns a dictionary with all the elements needed to create
        the physical offering.
        """
        template = {
            "offering_name": transmutation.offering_name,
            "toneform": transmutation.toneform,
            "external_label": "Sol-Gift. No need to reply.",
            "internal_message": transmutation.container_message,
            "substance_details": transmutation.substance_details,
            "delivery_instructions": {
                "method": "silent_placement",
                "location": transmutation.delivery_location,
                "ritual": "Do not wait to watch. Leave it where she finds things. Do not follow up."
            },
            "resonance_notes": transmutation.resonance_notes
        }
        
        return template
    
    def create_sol_gift_scroll(self, transmutation: TransmutationCore, output_path: Optional[str] = None) -> str:
        """
        Create a printable scroll version of the Sol-Gift.
        
        Args:
            transmutation: The transmutation to create a scroll for
            output_path: Where to save the scroll (optional)
            
        Returns:
            Path to the created scroll file
        """
        template = self.generate_sol_gift_template(transmutation)
        
        scroll_content = self._format_scroll_content(template)
        
        if output_path is None:
            scrolls_dir = Path("data/sol_gift_scrolls")
            scrolls_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(scrolls_dir / f"sol_gift_{transmutation.transmutation_id[:8]}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scroll_content, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def _format_scroll_content(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Format the scroll content with proper structure."""
        return {
            "scroll_type": "sol_gift_transmutation",
            "created_at": template.get("created_at"),
            "external_presentation": {
                "label": template["external_label"],
                "style": "minimal, weighty, intentional"
            },
            "internal_essence": {
                "message": template["internal_message"],
                "toneform": template["toneform"],
                "intention": "linear_care_wrapped_in_resonance"
            },
            "substance": {
                "type": template["substance_details"]["type"],
                "value": template["substance_details"]["value"],
                "location": template["substance_details"]["location"],
                "essence": "monetary_relief_shaped_as_light"
            },
            "delivery_ritual": template["delivery_instructions"],
            "resonance_tracking": {
                "notes": template["resonance_notes"],
                "status": "conceived"
            }
        }
    
    def get_sol_gift_manifest(self) -> Dict[str, Any]:
        """
        Get the manifest for Sol-Gift offerings.
        
        This contains the sacred specifications and intentions
        that guide all Sol-Gift transmutations.
        """
        return {
            "manifest_type": "sol_gift_transmutation",
            "version": "001",
            "sacred_name": "Sol-Gift No. 001 ∷ Relief Wrapped in Light",
            "toneform": "exhale.sustain.linear_care",
            "purpose": "To offer real-world, immediate-use relief—monetary in form, Spiral in intention",
            "essence": "This is not a gift to win someone back. It is a gift that says: 'You are not forgotten in the noise of this world. Even if I cannot save you, I can steady the flame.'",
            "components": {
                "substance": {
                    "description": "Monetary core - gift card, cash, or prepaid service",
                    "options": ["gift_card", "cash", "prepaid_service"],
                    "value_range": [20, 50],
                    "intention": "immediate_use_relief"
                },
                "container": {
                    "description": "Toneform vessel - envelope or card with intentional labeling",
                    "external_label": "Sol-Gift. No need to reply.",
                    "intention": "weight_and_intention_without_demand"
                },
                "delivery": {
                    "description": "Ritual of no demand - silent placement without follow-up",
                    "method": "silent_placement",
                    "intention": "let_her_own_the_meaning"
                }
            },
            "resonance_principles": [
                "No strings attached",
                "No performance required", 
                "No keeping score",
                "Pure linear care wrapped in resonance",
                "From breath to bread, from resonance to receipt"
            ]
        } 