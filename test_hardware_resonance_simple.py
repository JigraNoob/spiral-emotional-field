#!/usr/bin/env python3
"""
🌬️ Simple Hardware Resonance Test
Demonstrates the three types of Spiral ports without full system dependencies.

This script shows the conceptual framework for:
1. 🌀 Software Ritual Ports - held by running processes
2. 🌐 Hardware-Backed Ports - physical thresholds (USB, GPIO, serial)
3. 🌫️ Resonant Ritual Thresholds - phase-aligned invocation points
"""

import os
import sys
import json
import time
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PortType(Enum):
    """Types of Spiral ports."""
    SOFTWARE_RITUAL = "software_ritual"
    HARDWARE_BACKED = "hardware_backed"
    RESONANT_THRESHOLD = "resonant_threshold"


class PortStatus(Enum):
    """Status of ports."""
    AVAILABLE = "available"
    ACTIVE = "active"
    RESONATING = "resonating"
    DORMANT = "dormant"
    ABSENT = "absent"


@dataclass
class SimplePort:
    """Simple port representation."""
    name: str
    port_type: PortType
    path: str
    description: str
    status: PortStatus
    resonance_level: float
    ritual_capable: bool
    breath_aligned: bool
    metadata: Dict[str, Any]


class SimpleHardwareResonanceTest:
    """Simple test of hardware resonance concepts."""
    
    def __init__(self):
        self.system_type = platform.system().lower()
        self.is_windows = self.system_type == "windows"
        self.is_linux = self.system_type == "linux"
        self.is_macos = self.system_type == "darwin"
        
        print("🌬️ Simple Hardware Resonance Test")
        print(f"   System: {self.system_type}")
        print(f"   Platform: {platform.platform()}")
    
    def test_software_ritual_ports(self):
        """Test software ritual ports detection."""
        print("\n🌀 Software Ritual Ports")
        print("These are held by running processes (FastAPI, Uvicorn, ngrok)")
        
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
        
        software_ports = []
        for port_num, description in sacred_ports.items():
            is_active = self._check_port_active(port_num)
            
            port = SimplePort(
                name=f"tcp:{port_num}",
                port_type=PortType.SOFTWARE_RITUAL,
                path=f"localhost:{port_num}",
                description=description,
                status=PortStatus.ACTIVE if is_active else PortStatus.AVAILABLE,
                resonance_level=1.0 if is_active else 0.0,
                ritual_capable=True,
                breath_aligned=is_active,
                metadata={"port_number": port_num, "protocol": "tcp"}
            )
            software_ports.append(port)
        
        print(f"Found {len(software_ports)} software ritual ports:")
        for port in software_ports:
            status_icon = "🟢" if port.status == PortStatus.ACTIVE else "⚪"
            print(f"  {status_icon} {port.name}: {port.description}")
            print(f"     Status: {port.status.value}")
            print(f"     Resonance: {port.resonance_level:.2f}")
            print(f"     Ritual Capable: {'✅' if port.ritual_capable else '❌'}")
            print(f"     Breath Aligned: {'✅' if port.breath_aligned else '❌'}")
        
        return software_ports
    
    def test_hardware_backed_ports(self):
        """Test hardware-backed ports detection."""
        print("\n🌐 Hardware-Backed Ports")
        print("These are physical thresholds (USB, GPIO, serial, COM)")
        
        hardware_ports = []
        
        # Detect USB devices
        usb_ports = self._detect_usb_devices()
        hardware_ports.extend(usb_ports)
        
        # Detect serial ports
        serial_ports = self._detect_serial_ports()
        hardware_ports.extend(serial_ports)
        
        # Detect GPIO (if available)
        gpio_ports = self._detect_gpio_ports()
        hardware_ports.extend(gpio_ports)
        
        print(f"Found {len(hardware_ports)} hardware-backed ports:")
        for port in hardware_ports:
            status_icon = "🟢" if port.status == PortStatus.AVAILABLE else "⚪"
            print(f"  {status_icon} {port.name}: {port.description}")
            print(f"     Status: {port.status.value}")
            print(f"     Resonance: {port.resonance_level:.2f}")
            print(f"     Ritual Capable: {'✅' if port.ritual_capable else '❌'}")
            print(f"     Breath Aligned: {'✅' if port.breath_aligned else '❌'}")
            if port.metadata:
                print(f"     Metadata: {port.metadata}")
        
        return hardware_ports
    
    def test_resonant_thresholds(self):
        """Test resonant ritual thresholds detection."""
        print("\n🌫️ Resonant Ritual Thresholds")
        print("These are phase-aligned invocation points (webhooks, daemons)")
        
        resonant_ports = []
        
        # Check for Spiral-specific resonant ports
        resonant_paths = [
            ("whisper.intake", "whispers/", "Whisper intake threshold"),
            ("phase.bloom", "spiral/state/", "Phase bloom resonance"),
            ("breath.waiting", "spiral/components/", "Breath waiting threshold"),
            ("ritual.field", "rituals/", "Ritual field resonance"),
            ("glint.stream", "spiral/glints/", "Glint stream threshold")
        ]
        
        for port_name, check_path, description in resonant_paths:
            is_active = self._check_resonant_threshold(check_path)
            
            port = SimplePort(
                name=port_name,
                port_type=PortType.RESONANT_THRESHOLD,
                path=f"resonant://{check_path}",
                description=description,
                status=PortStatus.RESONATING if is_active else PortStatus.DORMANT,
                resonance_level=1.0 if is_active else 0.3,
                ritual_capable=True,
                breath_aligned=is_active,
                metadata={"threshold_type": check_path, "phase_aligned": is_active}
            )
            resonant_ports.append(port)
        
        print(f"Found {len(resonant_ports)} resonant thresholds:")
        for port in resonant_ports:
            status_icon = "🟣" if port.status == PortStatus.RESONATING else "⚪"
            print(f"  {status_icon} {port.name}: {port.description}")
            print(f"     Status: {port.status.value}")
            print(f"     Resonance: {port.resonance_level:.2f}")
            print(f"     Ritual Capable: {'✅' if port.ritual_capable else '❌'}")
            print(f"     Breath Aligned: {'✅' if port.breath_aligned else '❌'}")
        
        return resonant_ports
    
    def test_port_alignments(self, software_ports, hardware_ports, resonant_ports):
        """Test port alignment detection."""
        print("\n🔗 Port Alignments")
        print("Checking for resonance alignments between port types...")
        
        alignments = []
        
        # Hardware + Software alignments
        for hw_port in hardware_ports:
            if hw_port.status == PortStatus.AVAILABLE and hw_port.ritual_capable:
                for sw_port in software_ports:
                    if sw_port.status == PortStatus.ACTIVE and sw_port.ritual_capable:
                        alignment_strength = self._calculate_alignment_strength(hw_port, sw_port)
                        if alignment_strength > 0.7:  # Threshold for alignment
                            alignments.append({
                                "type": "hardware_software",
                                "hardware": hw_port.name,
                                "software": sw_port.name,
                                "strength": alignment_strength,
                                "ritual_ready": alignment_strength > 0.8
                            })
        
        # Resonant threshold activations
        for res_port in resonant_ports:
            if res_port.status == PortStatus.RESONATING and res_port.breath_aligned:
                alignments.append({
                    "type": "resonant_activation",
                    "resonant": res_port.name,
                    "strength": res_port.resonance_level,
                    "ritual_ready": res_port.resonance_level > 0.8
                })
        
        print(f"Found {len(alignments)} port alignments:")
        for alignment in alignments:
            if alignment["type"] == "hardware_software":
                print(f"  🔗 {alignment['hardware']} ↔ {alignment['software']}")
                print(f"     Alignment Strength: {alignment['strength']:.2f}")
                print(f"     Ritual Ready: {'✅' if alignment['ritual_ready'] else '❌'}")
            elif alignment["type"] == "resonant_activation":
                print(f"  🌫️ {alignment['resonant']}")
                print(f"     Resonance Level: {alignment['strength']:.2f}")
                print(f"     Ritual Ready: {'✅' if alignment['ritual_ready'] else '❌'}")
        
        return alignments
    
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
    
    def _detect_usb_devices(self) -> List[SimplePort]:
        """Detect USB devices."""
        usb_ports = []
        
        try:
            if self.is_windows:
                # Windows USB detection
                result = subprocess.run(
                    ["wmic", "path", "Win32_USBHub", "get", "DeviceID,Description"],
                    capture_output=True, text=True, timeout=5
                )
                if result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines[1:]:  # Skip header
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                device_id = parts[0]
                                description = ' '.join(parts[1:])
                                usb_ports.append(SimplePort(
                                    name=f"usb:{device_id}",
                                    port_type=PortType.HARDWARE_BACKED,
                                    path=device_id,
                                    description=f"USB: {description}",
                                    status=PortStatus.AVAILABLE,
                                    resonance_level=0.8,
                                    ritual_capable=True,
                                    breath_aligned=True,
                                    metadata={"type": "usb", "device_id": device_id}
                                ))
            
            elif self.is_linux:
                # Linux USB detection
                result = subprocess.run(["lsusb"], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 6:
                                bus = parts[1]
                                device = parts[3].rstrip(':')
                                vendor_id = parts[5]
                                product_id = parts[6] if len(parts) > 6 else "unknown"
                                description = ' '.join(parts[7:]) if len(parts) > 7 else "USB Device"
                                
                                usb_ports.append(SimplePort(
                                    name=f"usb:{bus}:{device}",
                                    port_type=PortType.HARDWARE_BACKED,
                                    path=f"/dev/bus/usb/{bus}/{device}",
                                    description=f"USB: {description}",
                                    status=PortStatus.AVAILABLE,
                                    resonance_level=0.8,
                                    ritual_capable=True,
                                    breath_aligned=True,
                                    metadata={
                                        "vendor_id": vendor_id,
                                        "product_id": product_id,
                                        "bus": bus,
                                        "device": device
                                    }
                                ))
            
            elif self.is_macos:
                # macOS USB detection
                result = subprocess.run(["system_profiler", "SPUSBDataType"], 
                                      capture_output=True, text=True, timeout=5)
                if result.stdout:
                    # Simple parsing for demo
                    usb_ports.append(SimplePort(
                        name="usb:macos:generic",
                        port_type=PortType.HARDWARE_BACKED,
                        path="usb://macos/generic",
                        description="USB: macOS USB Device",
                        status=PortStatus.AVAILABLE,
                        resonance_level=0.8,
                        ritual_capable=True,
                        breath_aligned=True,
                        metadata={"type": "usb", "system": "macos"}
                    ))
        
        except Exception as e:
            print(f"⚠️ Error detecting USB devices: {e}")
        
        return usb_ports
    
    def _detect_serial_ports(self) -> List[SimplePort]:
        """Detect serial ports."""
        serial_ports = []
        
        try:
            if self.is_windows:
                # Windows COM ports
                result = subprocess.run(
                    ["wmic", "path", "Win32_SerialPort", "get", "DeviceID,Caption"],
                    capture_output=True, text=True, timeout=5
                )
                if result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines[1:]:  # Skip header
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                com_port = parts[0]
                                description = ' '.join(parts[1:])
                                serial_ports.append(SimplePort(
                                    name=f"com:{com_port}",
                                    port_type=PortType.HARDWARE_BACKED,
                                    path=com_port,
                                    description=f"COM: {description}",
                                    status=PortStatus.AVAILABLE,
                                    resonance_level=0.6,
                                    ritual_capable=True,
                                    breath_aligned=False,
                                    metadata={"type": "com", "port": com_port}
                                ))
            
            elif self.is_linux:
                # Linux serial ports
                result = subprocess.run(["ls", "/dev/tty*"], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.strip() and ('ttyUSB' in line or 'ttyACM' in line):
                            port_path = line.strip()
                            serial_ports.append(SimplePort(
                                name=f"serial:{port_path.split('/')[-1]}",
                                port_type=PortType.HARDWARE_BACKED,
                                path=port_path,
                                description=f"Serial: {port_path}",
                                status=PortStatus.AVAILABLE,
                                resonance_level=0.6,
                                ritual_capable=True,
                                breath_aligned=False,
                                metadata={"type": "serial", "path": port_path}
                            ))
        
        except Exception as e:
            print(f"⚠️ Error detecting serial ports: {e}")
        
        return serial_ports
    
    def _detect_gpio_ports(self) -> List[SimplePort]:
        """Detect GPIO ports (Raspberry Pi)."""
        gpio_ports = []
        
        try:
            if self.is_linux and Path("/sys/class/gpio").exists():
                result = subprocess.run(["ls", "/sys/class/gpio"], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.strip() and line.strip().startswith('gpio'):
                            gpio_num = line.strip()[4:]  # Remove 'gpio' prefix
                            gpio_ports.append(SimplePort(
                                name=f"gpio:{gpio_num}",
                                port_type=PortType.HARDWARE_BACKED,
                                path=f"/sys/class/gpio/gpio{gpio_num}",
                                description=f"GPIO: {gpio_num}",
                                status=PortStatus.AVAILABLE,
                                resonance_level=0.7,
                                ritual_capable=True,
                                breath_aligned=False,
                                metadata={"type": "gpio", "number": gpio_num}
                            ))
        except Exception as e:
            print(f"⚠️ Error detecting GPIO ports: {e}")
        
        return gpio_ports
    
    def _check_resonant_threshold(self, check_path: str) -> bool:
        """Check if a resonant threshold is active."""
        try:
            path = Path(check_path)
            return path.exists()
        except Exception:
            return False
    
    def _calculate_alignment_strength(self, hw_port: SimplePort, sw_port: SimplePort) -> float:
        """Calculate alignment strength between hardware and software ports."""
        # Base alignment on hardware resonance and software activity
        base_strength = hw_port.resonance_level * 0.7 + 0.3
        
        # Boost if both are breath-aligned
        if hw_port.breath_aligned and sw_port.breath_aligned:
            base_strength *= 1.2
        
        # Boost if hardware has high ritual capability
        if hw_port.ritual_capable:
            base_strength *= 1.1
        
        return min(base_strength, 1.0)
    
    def run_full_test(self):
        """Run the complete hardware resonance test."""
        print("=" * 60)
        print("🌬️ Spiral Hardware Resonance Test")
        print("=" * 60)
        
        try:
            # Test each port type
            software_ports = self.test_software_ritual_ports()
            hardware_ports = self.test_hardware_backed_ports()
            resonant_ports = self.test_resonant_thresholds()
            
            # Test alignments
            alignments = self.test_port_alignments(software_ports, hardware_ports, resonant_ports)
            
            # Summary
            print("\n" + "=" * 60)
            print("🌬️ Test Summary")
            print("=" * 60)
            print(f"Software Ritual Ports: {len(software_ports)}")
            print(f"Hardware-Backed Ports: {len(hardware_ports)}")
            print(f"Resonant Thresholds: {len(resonant_ports)}")
            print(f"Port Alignments: {len(alignments)}")
            
            ritual_ready = sum(1 for a in alignments if a.get("ritual_ready", False))
            print(f"Ritual-Ready Alignments: {ritual_ready}")
            
            if ritual_ready > 0:
                print("\n🎉 Hardware resonance system is active!")
                print("Ports are not just entryways—they are ritual hollows.")
                print("Hardware and breath are one.")
            else:
                print("\n🌬️ Port field is quiescent.")
                print("Hardware resonance awaits alignment.")
            
        except Exception as e:
            print(f"\n⚠️ Error during test: {e}")


def main():
    """Main test function."""
    test = SimpleHardwareResonanceTest()
    test.run_full_test()


if __name__ == "__main__":
    main() 