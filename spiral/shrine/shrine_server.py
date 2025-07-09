"""
Spiral Shrine Server ∷ Sacred Altar of Care

This module provides the Flask-based shrine server that serves the sacred altar
where care is witnessed, not counted. Where presence meets participation.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from spiral.transmutations import SolGiftTransmutation, TransmutationLedger
from .coin_panel import SpiralCoinPanel


class ShrineServer:
    """Sacred shrine server for witnessing and participating in care flows."""
    
    def __init__(self, template_dir: Optional[str] = None, static_dir: Optional[str] = None):
        self.app = Flask(__name__, 
                        template_folder=template_dir or "templates/shrine",
                        static_folder=static_dir or "static/shrine")
        CORS(self.app)
        
        # Initialize core systems
        self.sol_gift = SolGiftTransmutation()
        self.ledger = TransmutationLedger()
        self.coin_panel = SpiralCoinPanel()
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup the sacred shrine routes."""
        
        @self.app.route('/')
        def shrine_home():
            """Sacred landing page - the altar of care."""
            return self._render_shrine_home()
        
        @self.app.route('/offer')
        def offering_panel():
            """Panel for offering care contributions."""
            return self._render_offering_panel()
        
        @self.app.route('/witness')
        def transparency_panel():
            """Panel for witnessing care flows."""
            return self._render_transparency_panel()
        
        @self.app.route('/glints')
        def glint_log():
            """Sacred log of emitted glints."""
            return self._render_glint_log()
        
        @self.app.route('/api/sol-pool-status')
        def api_sol_pool_status():
            """API endpoint for Sol Pool status."""
            return jsonify(self._get_sol_pool_status())
        
        @self.app.route('/api/glints')
        def api_glints():
            """API endpoint for glint data."""
            return jsonify(self._get_glints())
        
        @self.app.route('/api/transmutations')
        def api_transmutations():
            """API endpoint for transmutation data."""
            return jsonify(self._get_transmutations())
        
        @self.app.route('/api/offer', methods=['POST'])
        def api_offer():
            """API endpoint for making offerings."""
            return jsonify(self._process_offering(request.json or {}))
        
        @self.app.route('/coins')
        def coins_panel():
            """Panel for viewing SpiralCoins."""
            return self._render_coins_panel()
        
        @self.app.route('/api/coins')
        def api_coins():
            """API endpoint for SpiralCoin data."""
            return jsonify(self.coin_panel.get_coins_data())
        
        @self.app.route('/api/coins/<coin_number>')
        def api_coin_details(coin_number):
            """API endpoint for specific coin details."""
            return jsonify(self.coin_panel.get_coin_details(coin_number))
        
        @self.app.route('/coins/scroll')
        def coins_scroll():
            """Sacred scroll of all SpiralCoin relics."""
            return self._render_coins_scroll()
    
    def _render_shrine_home(self) -> str:
        """Render the sacred shrine home page."""
        
        # Get system status
        sol_pool_status = self._get_sol_pool_status()
        recent_glints = self._get_glints()[-5:]  # Last 5 glints
        recent_transmutations = self._get_transmutations()[-3:]  # Last 3 transmutations
        
        # Sacred invocation
        invocation = {
            "title": "Welcome to the Sol Pool",
            "subtitle": "Here, care becomes climate",
            "message": """In this sacred space, care is not counted, but witnessed.
            Presence meets participation, and giving is not extraction, but exhale.
            The Sol Pool shimmers with purpose, transmuting resonance into relief."""
        }
        
        return render_template('shrine_home.html',
                             invocation=invocation,
                             sol_pool_status=sol_pool_status,
                             recent_glints=recent_glints,
                             recent_transmutations=recent_transmutations)
    
    def _render_offering_panel(self) -> str:
        """Render the offering panel."""
        return render_template('offering_panel.html')
    
    def _render_transparency_panel(self) -> str:
        """Render the transparency panel."""
        transmutations = self._get_transmutations()
        trust_pools = self._get_trust_pools()
        
        return render_template('transparency_panel.html',
                             transmutations=transmutations,
                             trust_pools=trust_pools)
    
    def _render_glint_log(self) -> str:
        """Render the glint log."""
        glints = self._get_glints()
        return render_template('glint_log.html', glints=glints)
    
    def _render_coins_panel(self) -> str:
        """Render the SpiralCoins panel."""
        coins_data = self.coin_panel.get_coins_data()
        return render_template('coins_panel.html', coins_data=coins_data)
    
    def _render_coins_scroll(self) -> str:
        """Render the sacred SpiralCoin relics scroll."""
        return render_template('coins_scroll.html')
    
    def _get_sol_pool_status(self) -> Dict[str, Any]:
        """Get the current Sol Pool status."""
        
        # Read DeFi status
        defi_status_file = Path("data/spiral_defi/defi_status.json")
        if defi_status_file.exists():
            with open(defi_status_file, 'r') as f:
                defi_status = json.load(f)
        else:
            defi_status = {"status": "unknown", "trust_pools_count": 0}
        
        # Read trust pools
        pools_file = Path("data/spiral_defi/trust_pools.jsonl")
        total_capacity = 0
        active_pools = 0
        
        if pools_file.exists():
            with open(pools_file, 'r') as f:
                for line in f:
                    pool = json.loads(line)
                    if pool.get('status') == 'active':
                        active_pools += 1
                        total_capacity += pool.get('initial_capacity', 0)
        
        # Get transmutation count
        transmutations = self.ledger.get_all_transmutations()
        
        return {
            "status": defi_status.get("status", "unknown"),
            "active_pools": active_pools,
            "total_capacity": total_capacity,
            "active_transmutations": len(transmutations),
            "last_updated": defi_status.get("last_updated", datetime.now().isoformat()),
            "system_version": defi_status.get("system_version", "1.0.0")
        }
    
    def _get_glints(self) -> List[Dict[str, Any]]:
        """Get all emitted glints."""
        glints = []
        
        # Read DeFi glints
        defi_glints_file = Path("data/defi_glints.jsonl")
        if defi_glints_file.exists():
            with open(defi_glints_file, 'r') as f:
                for line in f:
                    glint = json.loads(line)
                    glint['source'] = 'defi'
                    glints.append(glint)
        
        # Sort by timestamp
        glints.sort(key=lambda x: x.get('emitted_at', ''))
        return glints
    
    def _get_transmutations(self) -> List[Dict[str, Any]]:
        """Get all transmutations."""
        transmutations = self.ledger.get_all_transmutations()
        return [t.to_dict() for t in transmutations]
    
    def _get_trust_pools(self) -> List[Dict[str, Any]]:
        """Get all trust pools."""
        pools = []
        
        pools_file = Path("data/spiral_defi/trust_pools.jsonl")
        if pools_file.exists():
            with open(pools_file, 'r') as f:
                for line in f:
                    pools.append(json.loads(line))
        
        return pools
    
    def _process_offering(self, offering_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a care offering."""
        
        try:
            amount = float(offering_data.get('amount', 0))
            source = offering_data.get('source', 'anonymous')
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
            
            # Update pool capacity (simplified - in a real system this would be more sophisticated)
            # For now, we'll just record the offering
            
            return {
                "success": True,
                "transmutation_id": transmutation.transmutation_id,
                "amount": amount,
                "message": "Offering received with gratitude"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Run the sacred shrine server."""
        print("🕯️  SPIRAL SHRINE SERVER")
        print("=" * 40)
        print(f"🌐 Shrine URL: http://{host}:{port}")
        print("🕯️  Blessed be the shrine.")
        print()
        
        self.app.run(host=host, port=port, debug=debug) 