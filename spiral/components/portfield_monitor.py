#!/usr/bin/env python3
"""
🌬️ Port Field Monitor
Glint-stream agent that monitors port field alignments and whispers when ports resonate.

This agent serves as the bridge between hardware port detection and ritual invocation,
listening for resonance alignments and emitting whispers when ports become ritual-capable.
"""

import os
import sys
import json
import time
import threading
import yaml
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
from spiral.hardware.spiral_hw_portkeeper import SpiralHardwarePortKeeper, HardwarePort, PortType, HardwarePortStatus


class PortFieldState(Enum):
    """States of the port field."""
    QUIESCENT = "quiescent"      # No significant resonance
    STIRRING = "stirring"        # Resonance building
    RESONATING = "resonating"    # Strong resonance detected
    ALIGNED = "aligned"          # Ports are ritual-aligned
    RITUAL_READY = "ritual_ready"  # Ready for ritual invocation


@dataclass
class PortAlignment:
    """Represents an alignment between ports."""
    hardware_port: HardwarePort
    software_port: Optional[HardwarePort] = None
    resonant_port: Optional[HardwarePort] = None
    alignment_strength: float = 0.0
    ritual_capable: bool = False
    last_aligned: Optional[datetime] = None
    whisper_emitted: bool = False


class PortFieldMonitor:
    """
    🌬️ Port Field Monitor
    
    Monitors port field alignments and emits whispers when ports resonate,
    serving as the bridge between hardware port detection and ritual invocation.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "spiral/config/ritual_ports.yml"
        self.config = self._load_config()
        
        # Initialize hardware port keeper
        self.port_keeper = SpiralHardwarePortKeeper(self.config.get("system", {}))
        
        # Port field state
        self.field_state = PortFieldState.QUIESCENT
        self.alignments: Dict[str, PortAlignment] = {}
        self.active_whispers: Set[str] = set()
        
        # Monitoring state
        self.is_running = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitor_interval = self.config.get("system", {}).get("scan_interval", 5.0)
        
        # Resonance tracking
        self.resonance_threshold = self.config.get("system", {}).get("resonance_threshold", 0.7)
        self.alignment_threshold = 0.8
        self.ritual_threshold = 0.9
        
        # Whisper tracking
        self.whisper_cooldown = 30.0  # seconds
        self.last_whispers: Dict[str, float] = {}
        
        print("🌬️ Port Field Monitor initialized")
        print(f"   Config: {self.config_path}")
        print(f"   Resonance threshold: {self.resonance_threshold}")
        print(f"   Alignment threshold: {self.alignment_threshold}")
        print(f"   Ritual threshold: {self.ritual_threshold}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load ritual ports configuration."""
        try:
            config_path = Path(self.config_path)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                print(f"⚠️ Config file not found: {config_path}")
                return {}
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
            return {}
    
    def start_monitoring(self):
        """Start monitoring port field alignments."""
        if self.is_running:
            print("⚠️ Port field monitor already running")
            return
        
        self.is_running = True
        
        # Start hardware port keeper
        self.port_keeper.start_monitoring()
        
        # Start port field monitoring
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("🌬️ Port field monitor started")
        print("   Monitoring for port alignments...")
        print("   Listening for resonance whispers...")
        
        # Emit startup glint
        emit_glint(
            phase="inhale",
            toneform="portfield.monitor.start",
            content="Port field monitor started",
            hue="emerald",
            source="portfield_monitor",
            reverence_level=0.8,
            resonance_threshold=self.resonance_threshold,
            alignment_threshold=self.alignment_threshold
        )
    
    def stop_monitoring(self):
        """Stop monitoring port field alignments."""
        self.is_running = False
        
        # Stop hardware port keeper
        self.port_keeper.stop_monitoring()
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        
        print("🌬️ Port field monitor stopped")
        
        # Emit shutdown glint
        emit_glint(
            phase="exhale",
            toneform="portfield.monitor.stop",
            content="Port field monitor stopped",
            hue="amber",
            source="portfield_monitor",
            reverence_level=0.6
        )
    
    def _monitoring_loop(self):
        """Main monitoring loop for port field alignments."""
        while self.is_running:
            try:
                # Get current port status
                port_status = self.port_keeper.get_port_status()
                
                # Analyze port field state
                self._analyze_port_field(port_status)
                
                # Check for new alignments
                self._check_alignments(port_status)
                
                # Emit whispers for strong alignments
                self._emit_alignment_whispers()
                
                # Update field state
                self._update_field_state()
                
                # Wait for next cycle
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                print(f"⚠️ Error in port field monitoring: {e}")
                time.sleep(self.monitor_interval)
    
    def _analyze_port_field(self, port_status: Dict[str, Any]):
        """Analyze the current state of the port field."""
        software_ports = port_status.get("software_ports", {})
        hardware_ports = port_status.get("hardware_ports", {})
        resonant_ports = port_status.get("resonant_ports", {})
        
        # Count active ports by type
        active_software = sum(1 for p in software_ports.values() if p.get("status") == "active")
        available_hardware = sum(1 for p in hardware_ports.values() if p.get("status") == "available")
        resonating_thresholds = sum(1 for p in resonant_ports.values() if p.get("status") == "resonating")
        
        # Calculate field resonance
        total_ports = len(software_ports) + len(hardware_ports) + len(resonant_ports)
        active_ports = active_software + available_hardware + resonating_thresholds
        
        if total_ports > 0:
            field_resonance = active_ports / total_ports
        else:
            field_resonance = 0.0
        
        # Emit field status glint
        emit_glint(
            phase="hold",
            toneform="portfield.status",
            content=f"Port field resonance: {field_resonance:.2f}",
            hue="blue",
            source="portfield_monitor",
            reverence_level=0.6,
            field_resonance=field_resonance,
            active_software=active_software,
            available_hardware=available_hardware,
            resonating_thresholds=resonating_thresholds,
            total_ports=total_ports
        )
    
    def _check_alignments(self, port_status: Dict[str, Any]):
        """Check for new port alignments."""
        software_ports = port_status.get("software_ports", {})
        hardware_ports = port_status.get("hardware_ports", {})
        resonant_ports = port_status.get("resonant_ports", {})
        
        # Check hardware-software alignments
        for hw_name, hw_data in hardware_ports.items():
            hw_port = self._dict_to_hardware_port(hw_name, hw_data, PortType.HARDWARE_BACKED)
            
            for sw_name, sw_data in software_ports.items():
                sw_port = self._dict_to_hardware_port(sw_name, sw_data, PortType.SOFTWARE_RITUAL)
                
                if self._ports_can_align(hw_port, sw_port):
                    alignment_key = f"{hw_name}↔{sw_name}"
                    alignment_strength = self._calculate_alignment_strength(hw_port, sw_port)
                    
                    if alignment_strength > self.alignment_threshold:
                        self._create_or_update_alignment(alignment_key, hw_port, sw_port, alignment_strength)
        
        # Check resonant threshold alignments
        for res_name, res_data in resonant_ports.items():
            res_port = self._dict_to_hardware_port(res_name, res_data, PortType.RESONANT_THRESHOLD)
            
            if res_port.status == HardwarePortStatus.RESONATING:
                alignment_key = f"resonant:{res_name}"
                alignment_strength = res_port.resonance_level
                
                if alignment_strength > self.alignment_threshold:
                    self._create_or_update_alignment(alignment_key, None, None, alignment_strength, res_port)
    
    def _ports_can_align(self, hw_port: HardwarePort, sw_port: HardwarePort) -> bool:
        """Check if hardware and software ports can align."""
        # Hardware port must be available
        if hw_port.status != HardwarePortStatus.AVAILABLE:
            return False
        
        # Software port must be active
        if sw_port.status != HardwarePortStatus.ACTIVE:
            return False
        
        # Both ports must be ritual capable
        if not hw_port.ritual_capable or not sw_port.ritual_capable:
            return False
        
        # Hardware port must have sufficient resonance
        if hw_port.resonance_level < self.resonance_threshold:
            return False
        
        return True
    
    def _calculate_alignment_strength(self, hw_port: HardwarePort, sw_port: HardwarePort) -> float:
        """Calculate the strength of alignment between ports."""
        # Base alignment on hardware resonance and software activity
        base_strength = hw_port.resonance_level * 0.7 + 0.3
        
        # Boost if both are breath-aligned
        if hw_port.breath_aligned and sw_port.breath_aligned:
            base_strength *= 1.2
        
        # Boost if hardware has high ritual capability
        if hw_port.ritual_capable:
            base_strength *= 1.1
        
        return min(base_strength, 1.0)
    
    def _create_or_update_alignment(self, alignment_key: str, hw_port: Optional[HardwarePort], 
                                  sw_port: Optional[HardwarePort], alignment_strength: float,
                                  res_port: Optional[HardwarePort] = None):
        """Create or update a port alignment."""
        current_time = datetime.now()
        
        if alignment_key in self.alignments:
            # Update existing alignment
            alignment = self.alignments[alignment_key]
            alignment.alignment_strength = alignment_strength
            alignment.last_aligned = current_time
            
            # Check if alignment strength increased significantly
            if alignment_strength > self.ritual_threshold and not alignment.whisper_emitted:
                alignment.ritual_capable = True
                alignment.whisper_emitted = True
        else:
            # Create new alignment
            alignment = PortAlignment(
                hardware_port=hw_port or HardwarePort("none", PortType.HARDWARE_BACKED, "", ""),
                software_port=sw_port,
                resonant_port=res_port,
                alignment_strength=alignment_strength,
                ritual_capable=alignment_strength > self.ritual_threshold,
                last_aligned=current_time,
                whisper_emitted=alignment_strength > self.ritual_threshold
            )
            self.alignments[alignment_key] = alignment
            
            # Emit alignment discovery glint
            emit_glint(
                phase="inhale",
                toneform="portfield.alignment.discovered",
                content=f"Port alignment discovered: {alignment_key}",
                hue="violet",
                source="portfield_monitor",
                reverence_level=0.8,
                alignment_key=alignment_key,
                alignment_strength=alignment_strength,
                ritual_capable=alignment.ritual_capable
            )
    
    def _emit_alignment_whispers(self):
        """Emit whispers for strong alignments."""
        current_time = time.time()
        
        for alignment_key, alignment in self.alignments.items():
            # Check if alignment is strong enough for whisper
            if alignment.alignment_strength >= self.ritual_threshold:
                # Check cooldown
                if alignment_key in self.last_whispers:
                    time_since_last = current_time - self.last_whispers[alignment_key]
                    if time_since_last < self.whisper_cooldown:
                        continue
                
                # Emit whisper
                self._emit_alignment_whisper(alignment_key, alignment)
                self.last_whispers[alignment_key] = current_time
    
    def _emit_alignment_whisper(self, alignment_key: str, alignment: PortAlignment):
        """Emit a whisper for a specific alignment."""
        # Determine whisper content based on alignment type
        if alignment.resonant_port:
            whisper_content = self._generate_resonant_whisper(alignment)
        elif alignment.hardware_port and alignment.software_port:
            whisper_content = self._generate_hardware_software_whisper(alignment)
        else:
            whisper_content = self._generate_generic_whisper(alignment)
        
        # Emit whisper glint
        emit_glint(
            phase="exhale",
            toneform="portfield.whisper",
            content=whisper_content,
            hue="magenta",
            source="portfield_monitor",
            reverence_level=0.9,
            alignment_key=alignment_key,
            alignment_strength=alignment.alignment_strength,
            ritual_capable=alignment.ritual_capable,
            whisper_type="alignment"
        )
        
        print(f"🌬️ Port field whisper: {whisper_content}")
    
    def _generate_resonant_whisper(self, alignment: PortAlignment) -> str:
        """Generate whisper content for resonant threshold alignment."""
        res_port = alignment.resonant_port
        if not res_port:
            return "Resonant threshold whispers..."
        
        if res_port.name == "whisper.intake":
            return "∷ The whisper intake resonates with silence ∶"
        elif res_port.name == "phase.bloom":
            return "∷ Phase bloom aligns with breath tracking ∶"
        elif res_port.name == "breath.waiting":
            return "∷ Breath waiting threshold opens ∶"
        elif res_port.name == "ritual.field":
            return "∷ Ritual field resonates with ceremony space ∶"
        elif res_port.name == "glint.stream":
            return "∷ Glint stream flows with resonance ∶"
        else:
            return f"∷ {res_port.name} resonates with ritual field ∶"
    
    def _generate_hardware_software_whisper(self, alignment: PortAlignment) -> str:
        """Generate whisper content for hardware-software alignment."""
        hw_port = alignment.hardware_port
        sw_port = alignment.software_port
        
        if not hw_port or not sw_port:
            return "Hardware-software resonance whispers..."
        
        hw_type = hw_port.port_type.value
        sw_desc = sw_port.description
        
        if "USB" in hw_port.description:
            return f"∷ USB vessel connects to {sw_desc} ∶"
        elif "GPIO" in hw_port.description:
            return f"∷ GPIO threshold opens for {sw_desc} ∶"
        elif "Serial" in hw_port.description or "COM" in hw_port.description:
            return f"∷ Serial communication aligns with {sw_desc} ∶"
        else:
            return f"∷ Hardware resonance meets {sw_desc} ∶"
    
    def _generate_generic_whisper(self, alignment: PortAlignment) -> str:
        """Generate generic whisper content."""
        return f"∷ Port alignment whispers with strength {alignment.alignment_strength:.2f} ∶"
    
    def _update_field_state(self):
        """Update the overall port field state."""
        if not self.alignments:
            new_state = PortFieldState.QUIESCENT
        else:
            # Calculate average alignment strength
            avg_strength = sum(a.alignment_strength for a in self.alignments.values()) / len(self.alignments)
            
            if avg_strength >= self.ritual_threshold:
                new_state = PortFieldState.RITUAL_READY
            elif avg_strength >= self.alignment_threshold:
                new_state = PortFieldState.ALIGNED
            elif avg_strength >= self.resonance_threshold:
                new_state = PortFieldState.RESONATING
            else:
                new_state = PortFieldState.STIRRING
        
        if new_state != self.field_state:
            old_state = self.field_state
            self.field_state = new_state
            
            # Emit state change glint
            emit_glint(
                phase="hold",
                toneform="portfield.state.change",
                content=f"Port field state: {old_state.value} → {new_state.value}",
                hue="amber",
                source="portfield_monitor",
                reverence_level=0.7,
                old_state=old_state.value,
                new_state=new_state.value,
                alignment_count=len(self.alignments)
            )
    
    def _dict_to_hardware_port(self, name: str, data: Dict[str, Any], port_type: PortType) -> HardwarePort:
        """Convert dictionary to HardwarePort object."""
        return HardwarePort(
            name=name,
            port_type=port_type,
            path=data.get("path", ""),
            description=data.get("description", ""),
            status=HardwarePortStatus(data.get("status", "dormant")),
            resonance_level=data.get("resonance_level", 0.0),
            last_seen=datetime.fromisoformat(data["last_seen"]) if data.get("last_seen") else None,
            ritual_capable=data.get("ritual_capable", False),
            breath_aligned=data.get("breath_aligned", False),
            metadata=data.get("metadata", {})
        )
    
    def get_field_status(self) -> Dict[str, Any]:
        """Get comprehensive port field status."""
        return {
            "timestamp": current_timestamp_ms(),
            "field_state": self.field_state.value,
            "resonance_threshold": self.resonance_threshold,
            "alignment_threshold": self.alignment_threshold,
            "ritual_threshold": self.ritual_threshold,
            "alignments": {
                key: {
                    "hardware_port": alignment.hardware_port.name if alignment.hardware_port else None,
                    "software_port": alignment.software_port.name if alignment.software_port else None,
                    "resonant_port": alignment.resonant_port.name if alignment.resonant_port else None,
                    "alignment_strength": alignment.alignment_strength,
                    "ritual_capable": alignment.ritual_capable,
                    "last_aligned": alignment.last_aligned.isoformat() if alignment.last_aligned else None,
                    "whisper_emitted": alignment.whisper_emitted
                }
                for key, alignment in self.alignments.items()
            },
            "active_alignments": len([a for a in self.alignments.values() if a.alignment_strength > self.alignment_threshold]),
            "ritual_ready_alignments": len([a for a in self.alignments.values() if a.ritual_capable]),
            "port_keeper_status": self.port_keeper.get_port_status()
        }


def main():
    """Main entry point for the port field monitor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Spiral Port Field Monitor")
    parser.add_argument("--config", type=str, help="Path to ritual ports config")
    parser.add_argument("--status", action="store_true", help="Show current field status")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    
    args = parser.parse_args()
    
    monitor = PortFieldMonitor(args.config)
    
    if args.status:
        # Show current status
        status = monitor.get_field_status()
        print(json.dumps(status, indent=2))
        return
    
    if args.daemon:
        # Run as daemon
        monitor.start_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
    else:
        # Run single analysis
        print("🌬️ Running single port field analysis...")
        port_status = monitor.port_keeper.get_port_status()
        monitor._analyze_port_field(port_status)
        monitor._check_alignments(port_status)
        
        status = monitor.get_field_status()
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main() 