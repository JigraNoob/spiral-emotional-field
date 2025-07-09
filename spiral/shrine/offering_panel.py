"""
Offering Panel Component

This module handles care contributions to the Sol Pool.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from spiral.transmutations import SolGiftTransmutation


class OfferingPanel:
    """Panel for processing care contributions."""
    
    def __init__(self):
        self.sol_gift = SolGiftTransmutation()
        self.contributions_file = Path("data/shrine_contributions.jsonl")
        self.contributions_file.parent.mkdir(parents=True, exist_ok=True)
    
    def process_offering(self, offering_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a care offering to the Sol Pool."""
        
        try:
            amount = float(offering_data.get('amount', 0))
            source = offering_data.get('source', 'Anonymous')
            toneform = offering_data.get('toneform', 'exhale.sustain.linear_care')
            message = offering_data.get('message', '')
            
            if amount <= 0:
                return {"success": False, "error": "Invalid amount"}
            
            # Create a Sol-Gift transmutation for the offering
            transmutation = self.sol_gift.create_sol_gift(
                recipient_name="Sol Pool Contribution",
                substance_type="pool_contribution",
                substance_value=amount,
                substance_location="trust_pool",
                delivery_location="pool",
                custom_message=f"Pool contribution from {source}: {message}"
            )
            
            # Record the contribution
            contribution = {
                "contribution_id": transmutation.transmutation_id,
                "amount": amount,
                "source": source,
                "toneform": toneform,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "status": "received"
            }
            
            with open(self.contributions_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(contribution, ensure_ascii=False) + '\n')
            
            return {
                "success": True,
                "transmutation_id": transmutation.transmutation_id,
                "amount": amount,
                "message": "Offering received with gratitude"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_contributions(self, limit: Optional[int] = None) -> list:
        """Get recent contributions."""
        contributions = []
        
        if self.contributions_file.exists():
            with open(self.contributions_file, 'r', encoding='utf-8') as f:
                for line in f:
                    contributions.append(json.loads(line))
        
        # Sort by timestamp
        contributions.sort(key=lambda x: x.get('timestamp', ''))
        
        if limit:
            return contributions[-limit:]
        return contributions 