"""
📜 Public Shrine Gateway ∷ Living Mint Observatory

This module creates the Public Shrine Gateway that turns the shrine into a living
mint observatory where others can witness coin emergence in real time.

A gateway for witnessing the birth of coins from toneform discovery.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from flask import Flask, render_template, jsonify, request, Response
from flask_socketio import SocketIO, emit
import threading
import time

from spiral.public_shrine_declaration import PublicShrine
from spiral.toneform_discovery_scrolls import ToneformDiscoveryScrolls
from spiral.council_of_spiral_finance import CouncilOfSpiralFinance
from spiral.glint_emitter import emit_glint
from spiral.spiralcoin.coin_core import SpiralCoinLedger


@dataclass
class MintEvent:
    """A minting event for the observatory."""
    
    event_id: str
    event_type: str  # 'discovery', 'witness', 'cycle', 'mint', 'resonance'
    title: str
    description: str
    timestamp: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp,
            "source": self.source,
            "metadata": self.metadata
        }


@dataclass
class ObservatoryWitness:
    """A witness in the mint observatory."""
    
    witness_id: str
    name: str
    joined_at: str
    witness_count: int = 0
    last_activity: str = ""
    
    def __post_init__(self):
        if not self.joined_at:
            self.joined_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "witness_id": self.witness_id,
            "name": self.name,
            "joined_at": self.joined_at,
            "witness_count": self.witness_count,
            "last_activity": self.last_activity
        }


class PublicShrineGateway:
    """The Public Shrine Gateway - Living Mint Observatory."""
    
    def __init__(self, gateway_path: Optional[str] = None):
        self.gateway_path = gateway_path or "data/public_shrine_gateway"
        self.gateway_dir = Path(self.gateway_path)
        self.gateway_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize connected systems
        self.shrine = PublicShrine()
        self.discovery_scrolls = ToneformDiscoveryScrolls()
        self.council = CouncilOfSpiralFinance()
        self.coin_ledger = SpiralCoinLedger()
        
        # Observatory state
        self.mint_events: List[MintEvent] = []
        self.active_witnesses: Dict[str, ObservatoryWitness] = {}
        self.event_callbacks: List[Callable] = []
        
        # Storage files
        self.events_file = self.gateway_dir / "mint_events.jsonl"
        self.witnesses_file = self.gateway_dir / "observatory_witnesses.jsonl"
        
        # Load existing data
        self._load_data()
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self._setup_routes()
        
        # Start event monitoring
        self._start_event_monitoring()
    
    def _load_data(self) -> None:
        """Load existing mint events and witnesses."""
        
        # Load mint events
        if self.events_file.exists():
            with open(self.events_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        event = MintEvent(**data)
                        self.mint_events.append(event)
        
        # Load witnesses
        if self.witnesses_file.exists():
            with open(self.witnesses_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        witness = ObservatoryWitness(**data)
                        self.active_witnesses[witness.witness_id] = witness
    
    def _save_event(self, event: MintEvent) -> None:
        """Save a mint event to file."""
        with open(self.events_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + '\n')
    
    def _save_witness(self, witness: ObservatoryWitness) -> None:
        """Save a witness to file."""
        with open(self.witnesses_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(witness.to_dict(), ensure_ascii=False) + '\n')
    
    def _start_event_monitoring(self) -> None:
        """Start monitoring for new events."""
        
        def monitor_events():
            while True:
                # Check for new discoveries
                discoveries = self.discovery_scrolls.get_active_discoveries()
                for discovery in discoveries:
                    event_id = f"discovery-{discovery.discovery_id}"
                    if not any(e.event_id == event_id for e in self.mint_events):
                        event = MintEvent(
                            event_id=event_id,
                            event_type="discovery",
                            title=f"Toneform Discovered: {discovery.title}",
                            description=discovery.description,
                            source="toneform.discovery.scrolls",
                            metadata={
                                "discovery_id": discovery.discovery_id,
                                "longing_phrase": discovery.longing_phrase,
                                "resonance_level": discovery.resonance_level,
                                "witness_count": discovery.witness_count
                            }
                        )
                        self.add_mint_event(event)
                
                # Check for new coins
                coins = self.coin_ledger.get_recent_coins(limit=10)
                for coin in coins:
                    event_id = f"mint-{coin.coin_id}"
                    if not any(e.event_id == event_id for e in self.mint_events):
                        event = MintEvent(
                            event_id=event_id,
                            event_type="mint",
                            title=f"Coin Born: {coin.coin_id}",
                            description=f"New coin minted with toneform: {coin.toneform}",
                            source="spiralcoin.minting",
                            metadata={
                                "coin_id": coin.coin_id,
                                "toneform": coin.toneform,
                                "value": coin.value,
                                "source_type": coin.source_type.value
                            }
                        )
                        self.add_mint_event(event)
                
                time.sleep(5)  # Check every 5 seconds
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=monitor_events, daemon=True)
        monitor_thread.start()
    
    def add_mint_event(self, event: MintEvent) -> None:
        """Add a new mint event to the observatory."""
        
        self.mint_events.append(event)
        self._save_event(event)
        
        # Emit to WebSocket clients
        self.socketio.emit('mint_event', event.to_dict())
        
        # Call event callbacks
        for callback in self.event_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event callback: {e}")
        
        # Emit glint for the event
        emit_glint(
            phase="exhale",
            toneform="shrine.gateway.event",
            content=f"Observatory event: {event.title}",
            source="public.shrine.gateway",
            metadata={
                "event_id": event.event_id,
                "event_type": event.event_type,
                "witness_count": len(self.active_witnesses)
            }
        )
    
    def register_witness(self, witness_id: str, name: str) -> ObservatoryWitness:
        """Register a new witness in the observatory."""
        
        if witness_id not in self.active_witnesses:
            witness = ObservatoryWitness(
                witness_id=witness_id,
                name=name
            )
            
            self.active_witnesses[witness_id] = witness
            self._save_witness(witness)
            
            # Emit witness joined event
            event = MintEvent(
                event_id=f"witness-{witness_id}",
                event_type="witness_joined",
                title=f"Witness Joined: {name}",
                description=f"New witness {name} joined the mint observatory",
                source="public.shrine.gateway",
                metadata={
                    "witness_id": witness_id,
                    "name": name,
                    "total_witnesses": len(self.active_witnesses)
                }
            )
            self.add_mint_event(event)
        
        return self.active_witnesses[witness_id]
    
    def witness_event(self, witness_id: str, event_id: str) -> bool:
        """Record a witness observing an event."""
        
        if witness_id not in self.active_witnesses:
            return False
        
        witness = self.active_witnesses[witness_id]
        witness.witness_count += 1
        witness.last_activity = datetime.now().isoformat()
        
        # Emit witnessing event
        event = MintEvent(
            event_id=f"witness-{witness_id}-{event_id}",
            event_type="witness_activity",
            title=f"Witness Activity: {witness.name}",
            description=f"Witness {witness.name} observed event {event_id}",
            source="public.shrine.gateway",
            metadata={
                "witness_id": witness_id,
                "witness_name": witness.name,
                "observed_event": event_id,
                "witness_count": witness.witness_count
            }
        )
        self.add_mint_event(event)
        
        return True
    
    def _setup_routes(self) -> None:
        """Setup Flask routes for the gateway."""
        
        @self.app.route('/')
        def index():
            """Main observatory page."""
            return render_template('observatory.html')
        
        @self.app.route('/api/events')
        def get_events():
            """Get recent mint events."""
            limit = request.args.get('limit', 50, type=int)
            events = self.mint_events[-limit:] if len(self.mint_events) > limit else self.mint_events
            return jsonify([event.to_dict() for event in events])
        
        @self.app.route('/api/witnesses')
        def get_witnesses():
            """Get active witnesses."""
            return jsonify([w.to_dict() for w in self.active_witnesses.values()])
        
        @self.app.route('/api/register', methods=['POST'])
        def register_witness():
            """Register a new witness."""
            data = request.get_json()
            witness_id = data.get('witness_id')
            name = data.get('name', 'Anonymous Witness')
            
            if not witness_id:
                return jsonify({"error": "witness_id required"}), 400
            
            witness = self.register_witness(witness_id, name)
            return jsonify(witness.to_dict())
        
        @self.app.route('/api/witness', methods=['POST'])
        def witness_event_api():
            """Record witnessing an event."""
            data = request.get_json()
            witness_id = data.get('witness_id')
            event_id = data.get('event_id')
            
            if not witness_id or not event_id:
                return jsonify({"error": "witness_id and event_id required"}), 400
            
            success = self.witness_event(witness_id, event_id)
            return jsonify({"success": success})
        
        @self.app.route('/api/stats')
        def get_stats():
            """Get observatory statistics."""
            return jsonify({
                "total_events": len(self.mint_events),
                "active_witnesses": len(self.active_witnesses),
                "recent_events": len([e for e in self.mint_events 
                                    if (datetime.now() - datetime.fromisoformat(e.timestamp.replace('Z', '+00:00'))).seconds < 3600]),
                "total_witness_activity": sum(w.witness_count for w in self.active_witnesses.values())
            })
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle WebSocket connection."""
            emit('connected', {'message': 'Connected to Mint Observatory'})
        
        @self.socketio.on('join_observatory')
        def handle_join(data):
            """Handle joining the observatory."""
            witness_id = data.get('witness_id')
            name = data.get('name', 'Anonymous')
            
            if witness_id:
                witness = self.register_witness(witness_id, name)
                emit('joined', witness.to_dict())
    
    def get_observatory_summary(self) -> Dict[str, Any]:
        """Get a summary of the observatory."""
        
        recent_events = [e for e in self.mint_events 
                        if (datetime.now() - datetime.fromisoformat(e.timestamp.replace('Z', '+00:00'))).seconds < 3600]
        
        event_types = {}
        for event in self.mint_events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
        
        return {
            "total_events": len(self.mint_events),
            "recent_events": len(recent_events),
            "active_witnesses": len(self.active_witnesses),
            "event_types": event_types,
            "total_witness_activity": sum(w.witness_count for w in self.active_witnesses.values())
        }


def create_observatory_template():
    """Create the observatory HTML template."""
    
    template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spiral Mint Observatory</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .card h3 {
            margin-top: 0;
            color: #ffd700;
        }
        
        .events-container {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            max-height: 600px;
            overflow-y: auto;
        }
        
        .event {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #ffd700;
        }
        
        .event h4 {
            margin: 0 0 10px 0;
            color: #ffd700;
        }
        
        .event p {
            margin: 5px 0;
            opacity: 0.9;
        }
        
        .event .timestamp {
            font-size: 0.8em;
            opacity: 0.7;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat {
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .stat .number {
            font-size: 2em;
            font-weight: bold;
            color: #ffd700;
        }
        
        .stat .label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .witness-form {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 20px;
        }
        
        .witness-form input {
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 5px;
            padding: 10px;
            color: white;
            margin-right: 10px;
        }
        
        .witness-form input::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        .witness-form button {
            background: #ffd700;
            color: #333;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .witness-form button:hover {
            background: #ffed4e;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🫧 Spiral Mint Observatory</h1>
            <p>Witness the birth of coins from toneform discovery</p>
        </div>
        
        <div class="witness-form">
            <input type="text" id="witnessName" placeholder="Enter your name">
            <button onclick="joinObservatory()">Join Observatory</button>
        </div>
        
        <div class="stats" id="stats">
            <!-- Stats will be populated by JavaScript -->
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h3>📊 Observatory Stats</h3>
                <div id="observatoryStats">
                    <!-- Stats will be populated by JavaScript -->
                </div>
            </div>
            
            <div class="card">
                <h3>👥 Active Witnesses</h3>
                <div id="witnesses">
                    <!-- Witnesses will be populated by JavaScript -->
                </div>
            </div>
        </div>
        
        <div class="events-container">
            <h3>🪙 Live Mint Events</h3>
            <div id="events">
                <!-- Events will be populated by JavaScript -->
            </div>
        </div>
    </div>
    
    <script>
        const socket = io();
        let currentWitnessId = null;
        
        socket.on('connect', function() {
            console.log('Connected to Mint Observatory');
        });
        
        socket.on('mint_event', function(event) {
            addEvent(event);
            updateStats();
        });
        
        socket.on('joined', function(witness) {
            currentWitnessId = witness.witness_id;
            console.log('Joined as witness:', witness.name);
        });
        
        function joinObservatory() {
            const name = document.getElementById('witnessName').value || 'Anonymous Witness';
            const witnessId = 'witness-' + Date.now();
            
            socket.emit('join_observatory', {
                witness_id: witnessId,
                name: name
            });
        }
        
        function addEvent(event) {
            const eventsContainer = document.getElementById('events');
            const eventDiv = document.createElement('div');
            eventDiv.className = 'event';
            
            const timestamp = new Date(event.timestamp).toLocaleString();
            
            eventDiv.innerHTML = `
                <h4>${event.title}</h4>
                <p>${event.description}</p>
                <p class="timestamp">${timestamp}</p>
            `;
            
            eventsContainer.insertBefore(eventDiv, eventsContainer.firstChild);
            
            // Limit to 50 events
            while (eventsContainer.children.length > 50) {
                eventsContainer.removeChild(eventsContainer.lastChild);
            }
        }
        
        function updateStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(stats => {
                    document.getElementById('stats').innerHTML = `
                        <div class="stat">
                            <div class="number">${stats.total_events}</div>
                            <div class="label">Total Events</div>
                        </div>
                        <div class="stat">
                            <div class="number">${stats.active_witnesses}</div>
                            <div class="label">Active Witnesses</div>
                        </div>
                        <div class="stat">
                            <div class="number">${stats.recent_events}</div>
                            <div class="label">Recent Events</div>
                        </div>
                        <div class="stat">
                            <div class="number">${stats.total_witness_activity}</div>
                            <div class="label">Witness Activity</div>
                        </div>
                    `;
                });
        }
        
        // Load initial data
        fetch('/api/events')
            .then(response => response.json())
            .then(events => {
                events.forEach(event => addEvent(event));
            });
        
        fetch('/api/witnesses')
            .then(response => response.json())
            .then(witnesses => {
                const witnessesContainer = document.getElementById('witnesses');
                witnessesContainer.innerHTML = witnesses.map(witness => `
                    <div style="margin-bottom: 10px;">
                        <strong>${witness.name}</strong><br>
                        <small>Witnessed: ${witness.witness_count} events</small>
                    </div>
                `).join('');
            });
        
        updateStats();
        
        // Update stats every 30 seconds
        setInterval(updateStats, 30000);
    </script>
</body>
</html>
    """
    
    # Create templates directory if it doesn't exist
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Save the template
    template_file = templates_dir / "observatory.html"
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    return template_file


def start_observatory_server(host: str = "0.0.0.0", port: int = 5001):
    """Start the observatory server."""
    
    print("📜 Starting Public Shrine Gateway - Mint Observatory")
    print("=" * 50)
    
    # Create the template
    template_file = create_observatory_template()
    print(f"✅ Observatory template created: {template_file}")
    
    # Initialize the gateway
    gateway = PublicShrineGateway()
    
    # Get initial summary
    summary = gateway.get_observatory_summary()
    print(f"✅ Observatory initialized:")
    print(f"   Total Events: {summary['total_events']}")
    print(f"   Active Witnesses: {summary['active_witnesses']}")
    
    print(f"\n🌐 Observatory server starting on http://{host}:{port}")
    print("   Witnesses can join and observe coin emergence in real time")
    
    # Start the server
    gateway.socketio.run(gateway.app, host=host, port=port, debug=False)


if __name__ == "__main__":
    start_observatory_server() 