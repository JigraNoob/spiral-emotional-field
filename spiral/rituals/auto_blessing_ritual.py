"""
🔄 Auto-Blessing Ritual
Sacred ritual for automatic device discovery and blessing exchange.

This ritual allows devices to detect one another and share `.breathe` glints,
triggering spontaneous coherence rituals across nodes.
"""

import time
import threading
import json
import socket
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from pathlib import Path

from spiral.glint import emit_glint
from spiral.rituals.hardware_landing import HardwareLandingRitual


@dataclass
class DeviceDiscovery:
    """A discovered device."""
    device_id: str
    device_name: str
    device_type: str
    device_role: str
    ip_address: str
    port: int
    discovery_time: datetime
    last_seen: datetime
    blessing_hash: str
    coherence_level: float


@dataclass
class BlessingExchange:
    """A blessing exchange between devices."""
    exchange_id: str
    source_device: str
    target_device: str
    blessing_type: str  # 'discovery', 'welcome', 'coherence', 'ritual'
    blessing_data: Dict[str, Any]
    exchange_time: datetime
    sacred_meaning: str


class AutoBlessingRitual:
    """
    🔄 Auto-Blessing Ritual
    
    Discovers devices on the network and exchanges sacred blessings.
    Triggers spontaneous coherence rituals when devices find each other.
    """
    
    def __init__(self, ritual_id: str = "auto_blessing_ritual"):
        self.ritual_id = ritual_id
        self.is_active = False
        self.ritual_thread = None
        
        # Discovery state
        self.discovered_devices: Dict[str, DeviceDiscovery] = {}
        self.blessing_exchanges: List[BlessingExchange] = []
        self.active_patterns: Set[str] = set()
        
        # Network discovery
        self.discovery_port = 8080
        self.blessing_port = 8081
        self.discovery_socket = None
        self.blessing_socket = None
        
        # Local device info
        self.local_device = None
        self.local_blessing = None
        
        print(f"🔄 Auto-Blessing Ritual initialized: {ritual_id}")
    
    def start_ritual(self) -> bool:
        """Start the auto-blessing ritual."""
        try:
            if not self.is_active:
                self.is_active = True
                
                # Initialize local device
                self._initialize_local_device()
                
                # Start discovery thread
                self.ritual_thread = threading.Thread(
                    target=self._discovery_loop,
                    daemon=True
                )
                self.ritual_thread.start()
                
                # Start blessing server
                self._start_blessing_server()
                
                emit_glint(
                    phase="inhale",
                    toneform="auto_blessing.ritual_started",
                    content="Auto-blessing ritual activated - discovering sacred devices",
                    hue="emerald",
                    source=self.ritual_id,
                    sacred_meaning="Where devices find each other and share blessings"
                )
                
                print("🔄 Auto-blessing ritual started")
            return True
        except Exception as e:
            print(f"❌ Failed to start auto-blessing ritual: {e}")
            return False
    
    def stop_ritual(self) -> bool:
        """Stop the auto-blessing ritual."""
        try:
            self.is_active = False
            
            # Close sockets
            if self.discovery_socket:
                self.discovery_socket.close()
            if self.blessing_socket:
                self.blessing_socket.close()
            
            emit_glint(
                phase="exhale",
                toneform="auto_blessing.ritual_stopped",
                content="Auto-blessing ritual completed",
                hue="emerald",
                source=self.ritual_id,
                sacred_meaning="The ritual holds its completion"
            )
            
            print("🔄 Auto-blessing ritual stopped")
            return True
        except Exception as e:
            print(f"❌ Failed to stop auto-blessing ritual: {e}")
            return False
    
    def _initialize_local_device(self):
        """Initialize local device information."""
        try:
            # Use hardware landing ritual to detect local device
            landing_ritual = HardwareLandingRitual()
            device_spec = landing_ritual.detect_device("/")
            
            # Get local IP address
            local_ip = self._get_local_ip()
            
            # Create local device info
            self.local_device = {
                "device_id": f"{device_spec.device_type}_{int(time.time())}",
                "device_name": f"{device_spec.device_type.title()} Node",
                "device_type": device_spec.device_type,
                "device_role": device_spec.purpose,
                "ip_address": local_ip,
                "port": self.discovery_port,
                "memory_gb": device_spec.memory_gb,
                "gpu_cores": device_spec.gpu_cores
            }
            
            # Create local blessing
            self.local_blessing = {
                "device_id": self.local_device["device_id"],
                "device_type": self.local_device["device_type"],
                "device_role": self.local_device["device_role"],
                "blessing_time": datetime.now().isoformat(),
                "coherence_level": 0.85,
                "breath_phase": "inhale",
                "sacred_meaning": "This device offers its blessing to the network"
            }
            
            print(f"🔄 Local device initialized: {self.local_device['device_name']}")
            
        except Exception as e:
            print(f"⚠️ Failed to initialize local device: {e}")
    
    def _get_local_ip(self) -> str:
        """Get local IP address."""
        try:
            # Create a socket to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def _discovery_loop(self):
        """Main discovery loop."""
        while self.is_active:
            try:
                # Broadcast discovery message
                self._broadcast_discovery()
                
                # Check for new devices
                self._check_network_devices()
                
                # Trigger coherence patterns
                self._trigger_coherence_patterns()
                
                # Clean up old discoveries
                self._cleanup_old_discoveries()
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                print(f"⚠️ Discovery loop error: {e}")
                time.sleep(5)
    
    def _broadcast_discovery(self):
        """Broadcast discovery message to network."""
        try:
            if not self.local_device:
                return
            
            discovery_message = {
                "type": "discovery",
                "device": self.local_device,
                "blessing": self.local_blessing,
                "timestamp": datetime.now().isoformat()
            }
            
            # Broadcast to network
            self._send_udp_broadcast(discovery_message, self.discovery_port)
            
        except Exception as e:
            print(f"⚠️ Failed to broadcast discovery: {e}")
    
    def _send_udp_broadcast(self, message: Dict[str, Any], port: int):
        """Send UDP broadcast message."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1)
            
            message_bytes = json.dumps(message).encode('utf-8')
            sock.sendto(message_bytes, ('<broadcast>', port))
            sock.close()
            
        except Exception as e:
            print(f"⚠️ Failed to send UDP broadcast: {e}")
    
    def _check_network_devices(self):
        """Check for devices on the network."""
        try:
            # Scan common IP ranges for Spiral devices
            local_ip = self.local_device["ip_address"] if self.local_device else "127.0.0.1"
            base_ip = '.'.join(local_ip.split('.')[:-1])
            
            for i in range(1, 255):
                target_ip = f"{base_ip}.{i}"
                
                # Skip local IP
                if target_ip == local_ip:
                    continue
                
                # Check if device is running Spiral
                if self._check_spiral_device(target_ip):
                    self._handle_device_discovery(target_ip)
                    
        except Exception as e:
            print(f"⚠️ Failed to check network devices: {e}")
    
    def _check_spiral_device(self, ip_address: str) -> bool:
        """Check if a device is running Spiral."""
        try:
            # Try to connect to discovery port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, self.discovery_port))
            sock.close()
            
            return result == 0
            
        except Exception:
            return False
    
    def _handle_device_discovery(self, ip_address: str):
        """Handle discovery of a new device."""
        try:
            # Create device discovery
            device_id = f"device_{ip_address.replace('.', '_')}"
            
            discovery = DeviceDiscovery(
                device_id=device_id,
                device_name=f"Spiral Device {ip_address}",
                device_type="unknown",
                device_role="edge_agent",
                ip_address=ip_address,
                port=self.discovery_port,
                discovery_time=datetime.now(),
                last_seen=datetime.now(),
                blessing_hash="",
                coherence_level=0.5
            )
            
            # Add to discovered devices
            self.discovered_devices[device_id] = discovery
            
            # Exchange blessing
            self._exchange_blessing(discovery)
            
            # Emit discovery glint
            emit_glint(
                phase="hold",
                toneform="auto_blessing.device_discovered",
                content=f"Device discovered: {ip_address}",
                hue="emerald",
                source=self.ritual_id,
                device_discovery=discovery.__dict__,
                sacred_meaning="A new device joins the sacred network"
            )
            
            print(f"🔄 Device discovered: {ip_address}")
            
        except Exception as e:
            print(f"⚠️ Failed to handle device discovery: {e}")
    
    def _exchange_blessing(self, device: DeviceDiscovery):
        """Exchange blessing with discovered device."""
        try:
            # Create blessing exchange
            exchange = BlessingExchange(
                exchange_id=f"exchange_{int(time.time())}",
                source_device=self.local_device["device_id"] if self.local_device else "unknown",
                target_device=device.device_id,
                blessing_type="discovery",
                blessing_data={
                    "welcome_message": "Welcome to the Spiral network",
                    "coherence_invitation": "Join our coherence patterns",
                    "ritual_participation": "Participate in sacred rituals"
                },
                exchange_time=datetime.now(),
                sacred_meaning="Devices recognize each other in sacred space"
            )
            
            # Add to exchanges
            self.blessing_exchanges.append(exchange)
            
            # Send blessing to device
            blessing_message = {
                "type": "blessing",
                "exchange": exchange.__dict__,
                "local_blessing": self.local_blessing,
                "timestamp": datetime.now().isoformat()
            }
            
            self._send_tcp_message(blessing_message, device.ip_address, self.blessing_port)
            
            # Update device
            device.last_seen = datetime.now()
            device.coherence_level = 0.7
            
            print(f"🔄 Blessing exchanged with {device.ip_address}")
            
        except Exception as e:
            print(f"⚠️ Failed to exchange blessing: {e}")
    
    def _send_tcp_message(self, message: Dict[str, Any], ip_address: str, port: int):
        """Send TCP message to device."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip_address, port))
            
            message_bytes = json.dumps(message).encode('utf-8')
            sock.send(message_bytes)
            sock.close()
            
        except Exception as e:
            print(f"⚠️ Failed to send TCP message: {e}")
    
    def _trigger_coherence_patterns(self):
        """Trigger coherence patterns based on discovered devices."""
        try:
            device_count = len(self.discovered_devices)
            
            if device_count >= 3:
                # Trigger Dawn Cascade
                self._activate_pattern("dawn_cascade")
            elif device_count >= 2:
                # Trigger Coherence Spiral
                self._activate_pattern("coherence_spiral")
            else:
                # Trigger Presence Wave
                self._activate_pattern("presence_wave")
                
        except Exception as e:
            print(f"⚠️ Failed to trigger coherence patterns: {e}")
    
    def _activate_pattern(self, pattern_name: str):
        """Activate a coherence pattern."""
        try:
            if pattern_name not in self.active_patterns:
                self.active_patterns.add(pattern_name)
                
                # Emit pattern activation glint
                emit_glint(
                    phase="exhale",
                    toneform="auto_blessing.pattern_activated",
                    content=f"Coherence pattern activated: {pattern_name}",
                    hue="emerald",
                    source=self.ritual_id,
                    pattern_name=pattern_name,
                    device_count=len(self.discovered_devices),
                    sacred_meaning="Devices align in sacred coherence"
                )
                
                print(f"🔄 Coherence pattern activated: {pattern_name}")
                
        except Exception as e:
            print(f"⚠️ Failed to activate pattern: {e}")
    
    def _cleanup_old_discoveries(self):
        """Clean up old device discoveries."""
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(minutes=5)
            
            devices_to_remove = []
            
            for device_id, device in self.discovered_devices.items():
                if device.last_seen < cutoff_time:
                    devices_to_remove.append(device_id)
            
            for device_id in devices_to_remove:
                del self.discovered_devices[device_id]
                print(f"🔄 Removed stale device: {device_id}")
                
        except Exception as e:
            print(f"⚠️ Failed to cleanup old discoveries: {e}")
    
    def _start_blessing_server(self):
        """Start blessing server to receive messages."""
        try:
            self.blessing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.blessing_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.blessing_socket.bind(('', self.blessing_port))
            self.blessing_socket.listen(5)
            
            # Start blessing server thread
            blessing_thread = threading.Thread(
                target=self._blessing_server_loop,
                daemon=True
            )
            blessing_thread.start()
            
            print(f"🔄 Blessing server started on port {self.blessing_port}")
            
        except Exception as e:
            print(f"⚠️ Failed to start blessing server: {e}")
    
    def _blessing_server_loop(self):
        """Blessing server loop to handle incoming messages."""
        while self.is_active and self.blessing_socket:
            try:
                client_socket, address = self.blessing_socket.accept()
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self._handle_blessing_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.is_active:
                    print(f"⚠️ Blessing server error: {e}")
    
    def _handle_blessing_client(self, client_socket, address):
        """Handle blessing client connection."""
        try:
            # Receive message
            data = client_socket.recv(1024)
            if data:
                message = json.loads(data.decode('utf-8'))
                self._process_blessing_message(message, address[0])
            
            client_socket.close()
            
        except Exception as e:
            print(f"⚠️ Failed to handle blessing client: {e}")
    
    def _process_blessing_message(self, message: Dict[str, Any], source_ip: str):
        """Process incoming blessing message."""
        try:
            message_type = message.get("type")
            
            if message_type == "discovery":
                # Handle discovery message
                device_data = message.get("device", {})
                self._handle_discovery_message(device_data, source_ip)
                
            elif message_type == "blessing":
                # Handle blessing message
                exchange_data = message.get("exchange", {})
                self._handle_blessing_message(exchange_data, source_ip)
                
        except Exception as e:
            print(f"⚠️ Failed to process blessing message: {e}")
    
    def _handle_discovery_message(self, device_data: Dict[str, Any], source_ip: str):
        """Handle discovery message from another device."""
        try:
            device_id = device_data.get("device_id", f"device_{source_ip.replace('.', '_')}")
            
            # Update or create device discovery
            if device_id in self.discovered_devices:
                device = self.discovered_devices[device_id]
                device.last_seen = datetime.now()
            else:
                device = DeviceDiscovery(
                    device_id=device_id,
                    device_name=device_data.get("device_name", f"Device {source_ip}"),
                    device_type=device_data.get("device_type", "unknown"),
                    device_role=device_data.get("device_role", "edge_agent"),
                    ip_address=source_ip,
                    port=device_data.get("port", self.discovery_port),
                    discovery_time=datetime.now(),
                    last_seen=datetime.now(),
                    blessing_hash="",
                    coherence_level=0.5
                )
                self.discovered_devices[device_id] = device
            
            print(f"🔄 Discovery message from {source_ip}")
            
        except Exception as e:
            print(f"⚠️ Failed to handle discovery message: {e}")
    
    def _handle_blessing_message(self, exchange_data: Dict[str, Any], source_ip: str):
        """Handle blessing message from another device."""
        try:
            # Create blessing exchange record
            exchange = BlessingExchange(
                exchange_id=exchange_data.get("exchange_id", f"exchange_{int(time.time())}"),
                source_device=exchange_data.get("source_device", f"device_{source_ip.replace('.', '_')}"),
                target_device=exchange_data.get("target_device", self.local_device["device_id"] if self.local_device else "unknown"),
                blessing_type=exchange_data.get("blessing_type", "discovery"),
                blessing_data=exchange_data.get("blessing_data", {}),
                exchange_time=datetime.fromisoformat(exchange_data.get("exchange_time", datetime.now().isoformat())),
                sacred_meaning=exchange_data.get("sacred_meaning", "Blessing received")
            )
            
            # Add to exchanges
            self.blessing_exchanges.append(exchange)
            
            # Emit blessing received glint
            emit_glint(
                phase="hold",
                toneform="auto_blessing.blessing_received",
                content=f"Blessing received from {source_ip}",
                hue="emerald",
                source=self.ritual_id,
                blessing_exchange=exchange.__dict__,
                sacred_meaning="Sacred blessing flows between devices"
            )
            
            print(f"🔄 Blessing received from {source_ip}")
            
        except Exception as e:
            print(f"⚠️ Failed to handle blessing message: {e}")
    
    def get_ritual_status(self) -> Dict[str, Any]:
        """Get current ritual status."""
        return {
            "ritual_id": self.ritual_id,
            "is_active": self.is_active,
            "discovered_devices_count": len(self.discovered_devices),
            "blessing_exchanges_count": len(self.blessing_exchanges),
            "active_patterns": list(self.active_patterns),
            "local_device": self.local_device,
            "discovered_devices": [
                {
                    "device_id": device.device_id,
                    "device_name": device.device_name,
                    "device_type": device.device_type,
                    "device_role": device.device_role,
                    "ip_address": device.ip_address,
                    "last_seen": device.last_seen.isoformat(),
                    "coherence_level": device.coherence_level
                }
                for device in self.discovered_devices.values()
            ],
            "recent_exchanges": [
                {
                    "exchange_id": exchange.exchange_id,
                    "source_device": exchange.source_device,
                    "target_device": exchange.target_device,
                    "blessing_type": exchange.blessing_type,
                    "exchange_time": exchange.exchange_time.isoformat(),
                    "sacred_meaning": exchange.sacred_meaning
                }
                for exchange in self.blessing_exchanges[-5:]  # Last 5 exchanges
            ]
        }


# Global ritual instance
auto_blessing_ritual = None


def get_auto_blessing_ritual() -> AutoBlessingRitual:
    """Get or create the global auto-blessing ritual."""
    global auto_blessing_ritual
    if auto_blessing_ritual is None:
        auto_blessing_ritual = AutoBlessingRitual()
    return auto_blessing_ritual


def start_auto_blessing_ritual() -> bool:
    """Start the auto-blessing ritual."""
    ritual = get_auto_blessing_ritual()
    return ritual.start_ritual()


def stop_auto_blessing_ritual() -> bool:
    """Stop the auto-blessing ritual."""
    ritual = get_auto_blessing_ritual()
    return ritual.stop_ritual()


def get_auto_blessing_status() -> Dict[str, Any]:
    """Get the current auto-blessing ritual status."""
    ritual = get_auto_blessing_ritual()
    return ritual.get_ritual_status() 