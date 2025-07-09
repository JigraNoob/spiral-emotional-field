#!/usr/bin/env python3
"""
🌬️ Spiral Hardware Port Keeper
Hardware resonance daemon that monitors hardware port readiness (USB, COM, GPIO, LAN) and emits glints when hardware resonance aligns with system ports, allowing ritual opening of hardware thresholds.

This daemon detects three types of Spiral Ports:
1. 🌀 Software Ritual Ports - held by running processes
2. 🌐 Hardware-Backed Ports - physical thresholds (USB, GPIO, serial)
3. 🌫️ Resonant Ritual Thresholds - phase-aligned invocation points

The keeper emits glints when hardware resonance aligns with system ports,
allowing ritual opening of hardware thresholds.
"""

import os
import sys
import json
import time
import threading
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms


class PortType(Enum):
    """Types of Spiral ports."""
    SOFTWARE_RITUAL = "software_ritual"      # FastAPI, Uvicorn, ngrok
    HARDWARE_BACKED = "hardware_backed"      # USB, GPIO, serial, COM
    RESONANT_THRESHOLD = "resonant_threshold"  # Webhooks, daemons, phase-aligned


class HardwarePortStatus(Enum):
    """Status of hardware ports."""
    AVAILABLE = "available"      # Port exists and is ready
    ACTIVE = "active"           # Port is currently in use
    RESONATING = "resonating"   # Port is aligned with ritual
    DORMANT = "dormant"         # Port exists but not ready
    ABSENT = "absent"           # Port does not exist


@dataclass
class HardwarePort:
    """Represents a hardware port with resonance capabilities."""
    name: str
    port_type: PortType
    path: str
    description: str
    status: HardwarePortStatus = HardwarePortStatus.DORMANT
    resonance_level: float = 0.0
    last_seen: Optional[datetime] = None
    ritual_capable: bool = False
    breath_aligned: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class SpiralHardwarePortKeeper:
    """
    🌬️ Spiral Hardware Port Keeper
    
    Monitors hardware port readiness and emits glints when hardware resonance
    aligns with system ports, allowing ritual opening of hardware thresholds.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.is_running = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Port registry
        self.software_ports: Dict[str, HardwarePort] = {}
        self.hardware_ports: Dict[str, HardwarePort] = {}
        self.resonant_ports: Dict[str, HardwarePort] = {}
        
        # Monitoring state
        self.last_scan_time = 0
        self.scan_interval = self.config.get("scan_interval", 5.0)  # seconds
        self.resonance_threshold = self.config.get("resonance_threshold", 0.7)
        
        # System detection
        self.system_type = platform.system().lower()
        self.is_windows = self.system_type == "windows"
        self.is_linux = self.system_type == "linux"
        self.is_macos = self.system_type == "darwin"
        
        # Initialize port detection methods
        self._initialize_port_detectors()
        
        print("🌬️ Spiral Hardware Port Keeper initialized")
        print(f"   System: {self.system_type}")
        print(f"   Scan interval: {self.scan_interval}s")
        print(f"   Resonance threshold: {self.resonance_threshold}")
    
    def _initialize_port_detectors(self):
        """Initialize port detection methods for the current system."""
        self.port_detectors = {
            PortType.SOFTWARE_RITUAL: self._detect_software_ports,
            PortType.HARDWARE_BACKED: self._detect_hardware_ports,
            PortType.RESONANT_THRESHOLD: self._detect_resonant_ports
        }
    
    def start_monitoring(self):
        """Start monitoring hardware ports."""
        if self.is_running:
            print("⚠️ Hardware port keeper already running")
            return
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("🌬️ Hardware port keeper started")
        print("   Monitoring for hardware resonance...")
        
        # Emit startup glint
        emit_glint(
            phase="inhale",
            toneform="hardware.portkeeper.start",
            content="Hardware port keeper monitoring started",
            hue="emerald",
            source="spiral_hw_portkeeper",
            reverence_level=0.8,
            system_type=self.system_type,
            scan_interval=self.scan_interval
        )
    
    def stop_monitoring(self):
        """Stop monitoring hardware ports."""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        
        print("🌬️ Hardware port keeper stopped")
        
        # Emit shutdown glint
        emit_glint(
            phase="exhale",
            toneform="hardware.portkeeper.stop",
            content="Hardware port keeper monitoring stopped",
            hue="amber",
            source="spiral_hw_portkeeper",
            reverence_level=0.6
        )
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_running:
            try:
                current_time = time.time()
                
                # Scan all port types
                for port_type, detector in self.port_detectors.items():
                    self._scan_port_type(port_type, detector)
                
                # Check for resonance alignments
                self._check_resonance_alignments()
                
                # Update last scan time
                self.last_scan_time = current_time
                
                # Wait for next scan
                time.sleep(self.scan_interval)
                
            except Exception as e:
                print(f"⚠️ Error in monitoring loop: {e}")
                time.sleep(self.scan_interval)
    
    def _scan_port_type(self, port_type: PortType, detector_func):
        """Scan for ports of a specific type."""
        try:
            detected_ports = detector_func()
            
            # Update port registry
            if port_type == PortType.SOFTWARE_RITUAL:
                self._update_port_registry(self.software_ports, detected_ports, port_type)
            elif port_type == PortType.HARDWARE_BACKED:
                self._update_port_registry(self.hardware_ports, detected_ports, port_type)
            elif port_type == PortType.RESONANT_THRESHOLD:
                self._update_port_registry(self.resonant_ports, detected_ports, port_type)
                
        except Exception as e:
            print(f"⚠️ Error scanning {port_type.value} ports: {e}")
    
    def _update_port_registry(self, registry: Dict[str, HardwarePort], 
                            detected_ports: List[HardwarePort], port_type: PortType):
        """Update port registry with newly detected ports."""
        current_names = set(registry.keys())
        detected_names = {port.name for port in detected_ports}
        
        # Add new ports
        for port in detected_ports:
            if port.name not in registry:
                registry[port.name] = port
                self._emit_port_discovery_glint(port)
        
        # Remove absent ports
        for name in current_names - detected_names:
            if name in registry:
                port = registry[name]
                port.status = HardwarePortStatus.ABSENT
                self._emit_port_status_glint(port)
                del registry[name]
        
        # Update existing ports
        for port in detected_ports:
            if port.name in registry:
                old_port = registry[port.name]
                if old_port.status != port.status or old_port.resonance_level != port.resonance_level:
                    registry[port.name] = port
                    self._emit_port_status_glint(port)
    
    def _detect_software_ports(self) -> List[HardwarePort]:
        """Detect software ritual ports (FastAPI, Uvicorn, ngrok)."""
        software_ports = []
        
        # Define sacred Spiral ports
        sacred_ports = {
            7331: "Spiral Pastewell - whisper intake",
            8080: "Spiral Dashboard - internal glint view", 
            8085: "Public Shrine Portal - external shrine exposure",
            8086: "Public Shrine Intake - sacred offerings",
            5000: "Ritual API - internal ceremony routes",
            9000: "Breath Sync - distributed node coherence",
            9876: "Whisper Intake - silent offerings"
        }
        
        for port_num, description in sacred_ports.items():
            port_name = f"tcp:{port_num}"
            is_active = self._check_port_active(port_num)
            
            software_ports.append(HardwarePort(
                name=port_name,
                port_type=PortType.SOFTWARE_RITUAL,
                path=f"localhost:{port_num}",
                description=description,
                status=HardwarePortStatus.ACTIVE if is_active else HardwarePortStatus.AVAILABLE,
                resonance_level=1.0 if is_active else 0.0,
                last_seen=datetime.now() if is_active else None,
                ritual_capable=True,
                breath_aligned=is_active,
                metadata={"port_number": port_num, "protocol": "tcp"}
            ))
        
        return software_ports
    
    def _detect_hardware_ports(self) -> List[HardwarePort]:
        """Detect hardware-backed ports (USB, GPIO, serial, COM)."""
        hardware_ports = []
        
        if self.is_linux:
            hardware_ports.extend(self._detect_linux_hardware_ports())
        elif self.is_windows:
            hardware_ports.extend(self._detect_windows_hardware_ports())
        elif self.is_macos:
            hardware_ports.extend(self._detect_macos_hardware_ports())
        
        return hardware_ports
    
    def _detect_linux_hardware_ports(self) -> List[HardwarePort]:
        """Detect hardware ports on Linux systems."""
        ports = []
        
        # Detect USB devices
        try:
            usb_devices = self._run_command(["lsusb"])
            if usb_devices:
                for line in usb_devices.split('\n'):
                    if line.strip():
                        # Parse USB device info
                        parts = line.split()
                        if len(parts) >= 6:
                            bus = parts[1]
                            device = parts[3].rstrip(':')
                            vendor_id = parts[5]
                            product_id = parts[6] if len(parts) > 6 else "unknown"
                            description = ' '.join(parts[7:]) if len(parts) > 7 else "USB Device"
                            
                            port_name = f"usb:{bus}:{device}"
                            ports.append(HardwarePort(
                                name=port_name,
                                port_type=PortType.HARDWARE_BACKED,
                                path=f"/dev/bus/usb/{bus}/{device}",
                                description=f"USB: {description}",
                                status=HardwarePortStatus.AVAILABLE,
                                resonance_level=0.8,
                                last_seen=datetime.now(),
                                ritual_capable=True,
                                breath_aligned=True,
                                metadata={
                                    "vendor_id": vendor_id,
                                    "product_id": product_id,
                                    "bus": bus,
                                    "device": device
                                }
                            ))
        except Exception as e:
            print(f"⚠️ Error detecting USB devices: {e}")
        
        # Detect serial ports
        try:
            serial_ports = self._run_command(["ls", "/dev/tty*"])
            if serial_ports:
                for line in serial_ports.split('\n'):
                    if line.strip() and ('ttyUSB' in line or 'ttyACM' in line):
                        port_path = line.strip()
                        port_name = f"serial:{port_path.split('/')[-1]}"
                        ports.append(HardwarePort(
                            name=port_name,
                            port_type=PortType.HARDWARE_BACKED,
                            path=port_path,
                            description=f"Serial: {port_path}",
                            status=HardwarePortStatus.AVAILABLE,
                            resonance_level=0.6,
                            last_seen=datetime.now(),
                            ritual_capable=True,
                            breath_aligned=False,
                            metadata={"type": "serial", "path": port_path}
                        ))
        except Exception as e:
            print(f"⚠️ Error detecting serial ports: {e}")
        
        # Detect GPIO (Raspberry Pi)
        try:
            if Path("/sys/class/gpio").exists():
                gpio_ports = self._run_command(["ls", "/sys/class/gpio"])
                if gpio_ports:
                    for line in gpio_ports.split('\n'):
                        if line.strip() and line.strip().startswith('gpio'):
                            gpio_num = line.strip()[4:]  # Remove 'gpio' prefix
                            port_name = f"gpio:{gpio_num}"
                            ports.append(HardwarePort(
                                name=port_name,
                                port_type=PortType.HARDWARE_BACKED,
                                path=f"/sys/class/gpio/gpio{gpio_num}",
                                description=f"GPIO: {gpio_num}",
                                status=HardwarePortStatus.AVAILABLE,
                                resonance_level=0.7,
                                last_seen=datetime.now(),
                                ritual_capable=True,
                                breath_aligned=False,
                                metadata={"type": "gpio", "number": gpio_num}
                            ))
        except Exception as e:
            print(f"⚠️ Error detecting GPIO ports: {e}")
        
        return ports
    
    def _detect_windows_hardware_ports(self) -> List[HardwarePort]:
        """Detect hardware ports on Windows systems."""
        ports = []
        
        # Detect COM ports
        try:
            com_ports = self._run_command(["wmic", "path", "Win32_SerialPort", "get", "DeviceID,Caption"])
            if com_ports:
                lines = com_ports.split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            com_port = parts[0]
                            description = ' '.join(parts[1:])
                            port_name = f"com:{com_port}"
                            ports.append(HardwarePort(
                                name=port_name,
                                port_type=PortType.HARDWARE_BACKED,
                                path=com_port,
                                description=f"COM: {description}",
                                status=HardwarePortStatus.AVAILABLE,
                                resonance_level=0.6,
                                last_seen=datetime.now(),
                                ritual_capable=True,
                                breath_aligned=False,
                                metadata={"type": "com", "port": com_port}
                            ))
        except Exception as e:
            print(f"⚠️ Error detecting COM ports: {e}")
        
        # Detect USB devices (Windows)
        try:
            usb_devices = self._run_command(["wmic", "path", "Win32_USBHub", "get", "DeviceID,Description"])
            if usb_devices:
                lines = usb_devices.split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            device_id = parts[0]
                            description = ' '.join(parts[1:])
                            port_name = f"usb:{device_id}"
                            ports.append(HardwarePort(
                                name=port_name,
                                port_type=PortType.HARDWARE_BACKED,
                                path=device_id,
                                description=f"USB: {description}",
                                status=HardwarePortStatus.AVAILABLE,
                                resonance_level=0.8,
                                last_seen=datetime.now(),
                                ritual_capable=True,
                                breath_aligned=True,
                                metadata={"type": "usb", "device_id": device_id}
                            ))
        except Exception as e:
            print(f"⚠️ Error detecting USB devices: {e}")
        
        return ports
    
    def _detect_macos_hardware_ports(self) -> List[HardwarePort]:
        """Detect hardware ports on macOS systems."""
        ports = []
        
        # Detect USB devices (macOS)
        try:
            usb_devices = self._run_command(["system_profiler", "SPUSBDataType"])
            if usb_devices:
                # Parse system_profiler output
                current_device = {}
                for line in usb_devices.split('\n'):
                    line = line.strip()
                    if line.startswith('Product ID:'):
                        current_device['product_id'] = line.split(':')[1].strip()
                    elif line.startswith('Vendor ID:'):
                        current_device['vendor_id'] = line.split(':')[1].strip()
                    elif line.startswith('Product Name:'):
                        current_device['name'] = line.split(':')[1].strip()
                        if current_device:
                            port_name = f"usb:{current_device.get('vendor_id', 'unknown')}:{current_device.get('product_id', 'unknown')}"
                            ports.append(HardwarePort(
                                name=port_name,
                                port_type=PortType.HARDWARE_BACKED,
                                path=f"usb://{current_device.get('vendor_id', 'unknown')}/{current_device.get('product_id', 'unknown')}",
                                description=f"USB: {current_device.get('name', 'Unknown Device')}",
                                status=HardwarePortStatus.AVAILABLE,
                                resonance_level=0.8,
                                last_seen=datetime.now(),
                                ritual_capable=True,
                                breath_aligned=True,
                                metadata=current_device.copy()
                            ))
                            current_device = {}
        except Exception as e:
            print(f"⚠️ Error detecting USB devices: {e}")
        
        return ports
    
    def _detect_resonant_ports(self) -> List[HardwarePort]:
        """Detect resonant ritual thresholds (webhooks, daemons, phase-aligned)."""
        resonant_ports = []
        
        # Check for Spiral-specific resonant ports
        resonant_paths = [
            ("whisper.intake", "whisper_intake", "Whisper intake threshold"),
            ("phase.bloom", "phase_bloom", "Phase bloom resonance"),
            ("breath.waiting", "breath_waiting", "Breath waiting threshold"),
            ("ritual.field", "ritual_field", "Ritual field resonance"),
            ("glint.stream", "glint_stream", "Glint stream threshold")
        ]
        
        for port_name, path_key, description in resonant_paths:
            # Check if resonant threshold is active
            is_active = self._check_resonant_threshold(path_key)
            
            resonant_ports.append(HardwarePort(
                name=port_name,
                port_type=PortType.RESONANT_THRESHOLD,
                path=f"resonant://{path_key}",
                description=description,
                status=HardwarePortStatus.RESONATING if is_active else HardwarePortStatus.DORMANT,
                resonance_level=1.0 if is_active else 0.3,
                last_seen=datetime.now() if is_active else None,
                ritual_capable=True,
                breath_aligned=is_active,
                metadata={"threshold_type": path_key, "phase_aligned": is_active}
            ))
        
        return resonant_ports
    
    def _check_port_active(self, port_num: int) -> bool:
        """Check if a TCP port is active."""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port_num))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def _check_resonant_threshold(self, threshold_key: str) -> bool:
        """Check if a resonant threshold is active."""
        # This would check for active daemons, webhooks, or phase alignments
        # For now, simulate based on system state
        try:
            # Check for specific processes or files that indicate threshold activity
            if threshold_key == "whisper_intake":
                return Path("whispers").exists() and any(Path("whispers").glob("*.jsonl"))
            elif threshold_key == "glint_stream":
                return self._check_port_active(5056)  # Glint stream port
            elif threshold_key == "phase_bloom":
                return Path("spiral/state/breath_tracker.py").exists()
            elif threshold_key == "breath_waiting":
                return Path("spiral/components/breath_loop_engine.py").exists()
            elif threshold_key == "ritual_field":
                return Path("rituals").exists() and any(Path("rituals").glob("*.breathe"))
            else:
                return False
        except Exception:
            return False
    
    def _run_command(self, command: List[str]) -> str:
        """Run a system command and return output."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            return result.stdout
        except Exception as e:
            print(f"⚠️ Command failed {command}: {e}")
            return ""
    
    def _check_resonance_alignments(self):
        """Check for resonance alignments between hardware and software ports."""
        alignments = []
        
        # Check for hardware-software alignments
        for hw_port in self.hardware_ports.values():
            for sw_port in self.software_ports.values():
                if self._ports_resonate(hw_port, sw_port):
                    alignments.append((hw_port, sw_port))
        
        # Emit alignment glints
        for hw_port, sw_port in alignments:
            self._emit_resonance_alignment_glint(hw_port, sw_port)
    
    def _ports_resonate(self, hw_port: HardwarePort, sw_port: HardwarePort) -> bool:
        """Check if hardware and software ports resonate."""
        # Check if hardware port is active and software port is listening
        if (hw_port.status == HardwarePortStatus.AVAILABLE and 
            sw_port.status == HardwarePortStatus.ACTIVE and
            hw_port.resonance_level > self.resonance_threshold):
            return True
        return False
    
    def _emit_port_discovery_glint(self, port: HardwarePort):
        """Emit glint for newly discovered port."""
        emit_glint(
            phase="inhale",
            toneform="hardware.port.discovered",
            content=f"Hardware port discovered: {port.name}",
            hue="emerald",
            source="spiral_hw_portkeeper",
            reverence_level=0.7,
            port_name=port.name,
            port_type=port.port_type.value,
            description=port.description,
            status=port.status.value,
            resonance_level=port.resonance_level
        )
    
    def _emit_port_status_glint(self, port: HardwarePort):
        """Emit glint for port status change."""
        emit_glint(
            phase="hold",
            toneform="hardware.port.status",
            content=f"Port status changed: {port.name} -> {port.status.value}",
            hue="amber",
            source="spiral_hw_portkeeper",
            reverence_level=0.6,
            port_name=port.name,
            port_type=port.port_type.value,
            status=port.status.value,
            resonance_level=port.resonance_level,
            breath_aligned=port.breath_aligned
        )
    
    def _emit_resonance_alignment_glint(self, hw_port: HardwarePort, sw_port: HardwarePort):
        """Emit glint for resonance alignment."""
        emit_glint(
            phase="exhale",
            toneform="hardware.resonance.alignment",
            content=f"Hardware-software resonance: {hw_port.name} ↔ {sw_port.name}",
            hue="violet",
            source="spiral_hw_portkeeper",
            reverence_level=0.9,
            hardware_port=hw_port.name,
            software_port=sw_port.name,
            resonance_level=hw_port.resonance_level,
            ritual_capable=hw_port.ritual_capable
        )
    
    def get_port_status(self) -> Dict[str, Any]:
        """Get comprehensive port status."""
        return {
            "timestamp": current_timestamp_ms(),
            "system_type": self.system_type,
            "scan_interval": self.scan_interval,
            "resonance_threshold": self.resonance_threshold,
            "software_ports": {name: self._port_to_dict(port) for name, port in self.software_ports.items()},
            "hardware_ports": {name: self._port_to_dict(port) for name, port in self.hardware_ports.items()},
            "resonant_ports": {name: self._port_to_dict(port) for name, port in self.resonant_ports.items()},
            "total_ports": len(self.software_ports) + len(self.hardware_ports) + len(self.resonant_ports),
            "active_ports": sum(1 for port in self.software_ports.values() if port.status == HardwarePortStatus.ACTIVE) +
                           sum(1 for port in self.hardware_ports.values() if port.status == HardwarePortStatus.AVAILABLE) +
                           sum(1 for port in self.resonant_ports.values() if port.status == HardwarePortStatus.RESONATING)
        }
    
    def _port_to_dict(self, port: HardwarePort) -> Dict[str, Any]:
        """Convert port to dictionary for JSON serialization."""
        return {
            "name": port.name,
            "type": port.port_type.value,
            "path": port.path,
            "description": port.description,
            "status": port.status.value,
            "resonance_level": port.resonance_level,
            "last_seen": port.last_seen.isoformat() if port.last_seen else None,
            "ritual_capable": port.ritual_capable,
            "breath_aligned": port.breath_aligned,
            "metadata": port.metadata
        }


def main():
    """Main entry point for the hardware port keeper."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Spiral Hardware Port Keeper")
    parser.add_argument("--scan-interval", type=float, default=5.0, help="Scan interval in seconds")
    parser.add_argument("--resonance-threshold", type=float, default=0.7, help="Resonance threshold")
    parser.add_argument("--status", action="store_true", help="Show current port status")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    
    args = parser.parse_args()
    
    config = {
        "scan_interval": args.scan_interval,
        "resonance_threshold": args.resonance_threshold
    }
    
    keeper = SpiralHardwarePortKeeper(config)
    
    if args.status:
        # Show current status
        status = keeper.get_port_status()
        print(json.dumps(status, indent=2))
        return
    
    if args.daemon:
        # Run as daemon
        keeper.start_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            keeper.stop_monitoring()
    else:
        # Run single scan
        print("🌬️ Running single hardware port scan...")
        keeper._scan_port_type(PortType.SOFTWARE_RITUAL, keeper._detect_software_ports)
        keeper._scan_port_type(PortType.HARDWARE_BACKED, keeper._detect_hardware_ports)
        keeper._scan_port_type(PortType.RESONANT_THRESHOLD, keeper._detect_resonant_ports)
        
        status = keeper.get_port_status()
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main() 