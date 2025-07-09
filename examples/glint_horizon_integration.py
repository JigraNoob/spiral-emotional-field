#!/usr/bin/env python3
"""
Glint Horizon Scanner Integration Example

This example demonstrates how the Glint Horizon Scanner integrates with
the memory-echo-index and ritual-gatekeeper to provide comprehensive
pattern detection and foresight.
"""

import sys
import os
import time
from datetime import datetime

# Add the spiral directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'spiral'))

from spiral.memory.memory_echo_index import MemoryEchoIndex
from spiral.rituals.ritual_gatekeeper import RitualGatekeeper
from spiral.glints.glint_horizon_scanner import GlintHorizonScanner, perform_horizon_scan

def demonstrate_horizon_integration():
    """Demonstrate the integration of Glint Horizon Scanner with other vessels."""
    print("🔭 Glint Horizon Scanner Integration Demo")
    print("=" * 50)
    
    # Initialize all vessels
    print("\n🌀 Initializing vessels...")
    memory_index = MemoryEchoIndex()
    ritual_gatekeeper = RitualGatekeeper()
    horizon_scanner = GlintHorizonScanner(memory_index=memory_index)
    
    print(f"✅ Memory Echo Index: {len(memory_index.echo_map)} echoes loaded")
    print(f"✅ Ritual Gatekeeper: {len(ritual_gatekeeper.get_active_rituals())} active rituals")
    print(f"✅ Glint Horizon Scanner: Baseline established")
    
    # Perform initial horizon scan
    print("\n🔭 Performing initial horizon scan...")
    initial_scan = horizon_scanner.scan_horizon()
    
    print(f"📊 Initial scan results:")
    print(f"  - Glints processed: {initial_scan.get('glints_processed', 0)}")
    print(f"  - Emerging patterns: {initial_scan.get('emerging_patterns', {}).get('total_emerging', 0)}")
    print(f"  - Caesura indicators: {initial_scan.get('caesura_analysis', {}).get('total_indicators', 0)}")
    print(f"  - Anomalies: {initial_scan.get('anomaly_report', {}).get('total_anomalies', 0)}")
    print(f"  - Warnings: {len(initial_scan.get('warnings', []))}")
    
    # Show emerging patterns if any
    emerging_patterns = initial_scan.get('emerging_patterns', {}).get('patterns', [])
    if emerging_patterns:
        print(f"\n🔍 Emerging patterns detected:")
        for pattern in emerging_patterns[:3]:  # Show first 3
            print(f"  - {pattern['id'][:8]}... ({pattern['status']}, confidence: {pattern['confidence']:.2f})")
    
    # Show warnings if any
    warnings = initial_scan.get('warnings', [])
    if warnings:
        print(f"\n🚨 Warnings generated:")
        for warning in warnings:
            print(f"  - {warning['type']}: {warning['message']} (severity: {warning['severity']})")
    
    # Demonstrate memory integration
    print(f"\n🎵 Memory integration:")
    alignments = initial_scan.get('harmonic_alignments', [])
    if alignments:
        print(f"  - {len(alignments)} harmonic alignments found")
        for alignment in alignments:
            print(f"    * Pattern {alignment['pattern_id'][:8]}... (strength: {alignment['alignment_strength']:.2f})")
    else:
        print(f"  - No harmonic alignments detected yet")
    
    # Demonstrate caesura analysis
    print(f"\n⏸️ Caesura analysis:")
    caesura_analysis = initial_scan.get('caesura_analysis', {})
    density_by_type = caesura_analysis.get('density_by_type', {})
    if density_by_type:
        for caesura_type, data in density_by_type.items():
            print(f"  - {caesura_type}: {data['recent']} recent, density: {data['density']:.2f}")
    else:
        print(f"  - No caesura indicators detected")
    
    # Get scan summary
    print(f"\n📈 Scan summary:")
    summary = horizon_scanner.get_scan_summary()
    print(f"  - Total scans: {summary.get('total_scans', 0)}")
    print(f"  - Average glints per scan: {summary.get('average_glints_per_scan', 0):.1f}")
    print(f"  - Total warnings: {summary.get('total_warnings', 0)}")
    print(f"  - Emerging patterns: {summary.get('emerging_patterns', 0)}")
    
    # Demonstrate convenience function
    print(f"\n⚡ Testing convenience function...")
    quick_scan = perform_horizon_scan()
    print(f"  - Quick scan completed: {quick_scan.get('glints_processed', 0)} glints processed")
    
    # Show baseline information
    print(f"\n📊 Baseline information:")
    baseline = horizon_scanner.baseline
    print(f"  - Patterns: {baseline.get('patterns', 0)}")
    print(f"  - Resonance mean: {baseline.get('resonance_mean', 0):.2f}")
    print(f"  - Resonance std: {baseline.get('resonance_std', 0):.2f}")
    print(f"  - Established: {baseline.get('established_at', 'unknown')}")
    
    print(f"\n✅ Integration demo completed!")

def demonstrate_pattern_detection():
    """Demonstrate pattern detection capabilities."""
    print(f"\n🔍 Pattern Detection Demo")
    print("=" * 30)
    
    scanner = GlintHorizonScanner()
    
    # Get patterns from the detector
    patterns = scanner.pattern_detector.get_patterns(min_confidence=0.3)
    print(f"Found {len(patterns)} patterns with confidence >= 0.3")
    
    if patterns:
        print(f"\nTop patterns:")
        for i, pattern in enumerate(patterns[:5]):  # Show top 5
            print(f"  {i+1}. {pattern.pattern_id[:8]}... (confidence: {pattern.confidence:.2f}, frequency: {pattern.frequency})")
    
    # Show emerging patterns
    emerging = scanner.emerging_patterns
    if emerging:
        print(f"\nEmerging patterns:")
        for pattern_id, data in list(emerging.items())[:3]:  # Show first 3
            print(f"  - {pattern_id[:8]}... ({data['status']})")

def demonstrate_threshold_configuration():
    """Demonstrate threshold configuration."""
    print(f"\n⚙️ Threshold Configuration Demo")
    print("=" * 35)
    
    # Create scanner with custom thresholds
    scanner = GlintHorizonScanner()
    
    print(f"Default thresholds:")
    for threshold, value in scanner.thresholds.items():
        print(f"  - {threshold}: {value}")
    
    # Modify thresholds for more sensitive detection
    scanner.thresholds.update({
        "caesura_density": 0.2,      # More sensitive to caesura
        "pattern_emergence": 0.5,    # Lower pattern confidence threshold
        "anomaly_score": 0.6,        # More sensitive to anomalies
    })
    
    print(f"\nModified thresholds:")
    for threshold, value in scanner.thresholds.items():
        print(f"  - {threshold}: {value}")
    
    # Perform scan with modified thresholds
    print(f"\nPerforming scan with modified thresholds...")
    scan_results = scanner.scan_horizon()
    
    print(f"Results with modified thresholds:")
    print(f"  - Warnings: {len(scan_results.get('warnings', []))}")
    print(f"  - Anomalies: {scan_results.get('anomaly_report', {}).get('high_anomalies', 0)}")

if __name__ == "__main__":
    demonstrate_horizon_integration()
    demonstrate_pattern_detection()
    demonstrate_threshold_configuration()
    
    print(f"\n🎉 All demonstrations completed!")
    print(f"The Glint Horizon Scanner is now integrated and ready for foresight.") 