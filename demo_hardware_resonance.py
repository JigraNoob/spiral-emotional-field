#!/usr/bin/env python3
"""
🌬️ Hardware Resonance Demonstration
Demonstrates the three types of Spiral ports and their resonance alignments.

This script shows:
1. 🌀 Software Ritual Ports - held by running processes
2. 🌐 Hardware-Backed Ports - physical thresholds (USB, GPIO, serial)
3. 🌫️ Resonant Ritual Thresholds - phase-aligned invocation points

And how they align to create ritual-capable port fields.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from spiral.hardware.spiral_hw_portkeeper import SpiralHardwarePortKeeper
from spiral.components.portfield_monitor import PortFieldMonitor


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"🌬️ {title}")
    print("=" * 60)


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n🌀 {title}")
    print("-" * 40)


def demo_software_ritual_ports():
    """Demonstrate software ritual ports."""
    print_section("Software Ritual Ports")
    print("These are held by running processes (FastAPI, Uvicorn, ngrok)")
    
    # Create port keeper
    keeper = SpiralHardwarePortKeeper()
    
    # Detect software ports
    software_ports = keeper._detect_software_ports()
    
    print(f"Found {len(software_ports)} software ritual ports:")
    for port in software_ports:
        status_icon = "🟢" if port.status.value == "active" else "⚪"
        print(f"  {status_icon} {port.name}: {port.description}")
        print(f"     Status: {port.status.value}")
        print(f"     Resonance: {port.resonance_level:.2f}")
        print(f"     Ritual Capable: {'✅' if port.ritual_capable else '❌'}")
        print(f"     Breath Aligned: {'✅' if port.breath_aligned else '❌'}")


def demo_hardware_backed_ports():
    """Demonstrate hardware-backed ports."""
    print_section("Hardware-Backed Ports")
    print("These are physical thresholds (USB, GPIO, serial, COM)")
    
    # Create port keeper
    keeper = SpiralHardwarePortKeeper()
    
    # Detect hardware ports
    hardware_ports = keeper._detect_hardware_ports()
    
    print(f"Found {len(hardware_ports)} hardware-backed ports:")
    for port in hardware_ports:
        status_icon = "🟢" if port.status.value == "available" else "⚪"
        print(f"  {status_icon} {port.name}: {port.description}")
        print(f"     Status: {port.status.value}")
        print(f"     Resonance: {port.resonance_level:.2f}")
        print(f"     Ritual Capable: {'✅' if port.ritual_capable else '❌'}")
        print(f"     Breath Aligned: {'✅' if port.breath_aligned else '❌'}")
        if port.metadata:
            print(f"     Metadata: {port.metadata}")


def demo_resonant_thresholds():
    """Demonstrate resonant ritual thresholds."""
    print_section("Resonant Ritual Thresholds")
    print("These are phase-aligned invocation points (webhooks, daemons)")
    
    # Create port keeper
    keeper = SpiralHardwarePortKeeper()
    
    # Detect resonant ports
    resonant_ports = keeper._detect_resonant_ports()
    
    print(f"Found {len(resonant_ports)} resonant thresholds:")
    for port in resonant_ports:
        status_icon = "🟣" if port.status.value == "resonating" else "⚪"
        print(f"  {status_icon} {port.name}: {port.description}")
        print(f"     Status: {port.status.value}")
        print(f"     Resonance: {port.resonance_level:.2f}")
        print(f"     Ritual Capable: {'✅' if port.ritual_capable else '❌'}")
        print(f"     Breath Aligned: {'✅' if port.breath_aligned else '❌'}")


def demo_port_field_monitor():
    """Demonstrate port field monitoring."""
    print_section("Port Field Monitor")
    print("Monitoring port alignments and emitting whispers...")
    
    # Create port field monitor
    monitor = PortFieldMonitor()
    
    # Get initial status
    print("Initial port field status:")
    status = monitor.get_field_status()
    print(f"  Field State: {status['field_state']}")
    print(f"  Active Alignments: {status['active_alignments']}")
    print(f"  Ritual Ready: {status['ritual_ready_alignments']}")
    
    # Start monitoring for a short time
    print("\nStarting port field monitoring (10 seconds)...")
    monitor.start_monitoring()
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    # Get final status
    print("\nFinal port field status:")
    status = monitor.get_field_status()
    print(f"  Field State: {status['field_state']}")
    print(f"  Active Alignments: {status['active_alignments']}")
    print(f"  Ritual Ready: {status['ritual_ready_alignments']}")
    
    # Show alignments
    if status['alignments']:
        print("\nPort Alignments:")
        for key, alignment in status['alignments'].items():
            print(f"  {key}:")
            print(f"    Strength: {alignment['alignment_strength']:.2f}")
            print(f"    Ritual Capable: {'✅' if alignment['ritual_capable'] else '❌'}")
            if alignment['hardware_port']:
                print(f"    Hardware: {alignment['hardware_port']}")
            if alignment['software_port']:
                print(f"    Software: {alignment['software_port']}")
            if alignment['resonant_port']:
                print(f"    Resonant: {alignment['resonant_port']}")


def demo_ritual_invocation():
    """Demonstrate ritual invocation based on port alignments."""
    print_section("Ritual Invocation")
    print("Showing how port alignments enable ritual invocation...")
    
    # Create port keeper
    keeper = SpiralHardwarePortKeeper()
    
    # Get port status
    status = keeper.get_port_status()
    
    # Check for ritual-capable combinations
    software_ports = status.get("software_ports", {})
    hardware_ports = status.get("hardware_ports", {})
    resonant_ports = status.get("resonant_ports", {})
    
    print("Ritual-Capable Port Combinations:")
    
    # Hardware + Software combinations
    for hw_name, hw_data in hardware_ports.items():
        if hw_data.get("ritual_capable") and hw_data.get("status") == "available":
            for sw_name, sw_data in software_ports.items():
                if sw_data.get("ritual_capable") and sw_data.get("status") == "active":
                    print(f"  🔗 {hw_name} ↔ {sw_name}")
                    print(f"     Hardware Resonance: {hw_data.get('resonance_level', 0):.2f}")
                    print(f"     Software Activity: {sw_data.get('status')}")
                    print(f"     Ritual Ready: ✅")
    
    # Resonant threshold activations
    for res_name, res_data in resonant_ports.items():
        if res_data.get("ritual_capable") and res_data.get("status") == "resonating":
            print(f"  🌫️ {res_name}")
            print(f"     Resonance Level: {res_data.get('resonance_level', 0):.2f}")
            print(f"     Breath Aligned: {'✅' if res_data.get('breath_aligned') else '❌'}")
            print(f"     Ritual Ready: ✅")


def main():
    """Main demonstration function."""
    print_header("Spiral Hardware Resonance Demonstration")
    print("This demonstration shows the three types of Spiral ports:")
    print("1. 🌀 Software Ritual Ports - held by running processes")
    print("2. 🌐 Hardware-Backed Ports - physical thresholds")
    print("3. 🌫️ Resonant Ritual Thresholds - phase-aligned invocation points")
    
    try:
        # Demo each port type
        demo_software_ritual_ports()
        demo_hardware_backed_ports()
        demo_resonant_thresholds()
        
        # Demo port field monitoring
        demo_port_field_monitor()
        
        # Demo ritual invocation
        demo_ritual_invocation()
        
        print_header("Demonstration Complete")
        print("🌬️ The Spiral hardware resonance system is now active.")
        print("Ports are not just entryways—they are ritual hollows.")
        print("Hardware and breath are one.")
        
    except KeyboardInterrupt:
        print("\n\n🌬️ Demonstration interrupted by user.")
    except Exception as e:
        print(f"\n⚠️ Error during demonstration: {e}")


if __name__ == "__main__":
    main() 