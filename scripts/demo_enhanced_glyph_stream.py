#!/usr/bin/env python3
"""
🌬️ Enhanced Glyph Stream Demonstration
Showcases the living glyph system with organic pulse layering, phase heatmap, and slow echo mode.
"""

import requests
import time
import json
from datetime import datetime

def test_slow_echo_mode():
    """Test the slow echo mode for meditative presentation."""
    print("🕯️ Testing Slow Echo Mode")
    print("=" * 50)
    
    # Enable slow echo mode
    response = requests.post(
        "http://localhost:5000/glyph-stream/slow-echo",
        json={"enabled": True, "delay": 3.0}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Slow echo mode enabled: {data}")
    else:
        print(f"❌ Failed to enable slow echo mode: {response.status_code}")
        return False
    
    # Test glyph invocations with slow echo
    print("\n🌐 Invoking glyphs with slow echo mode...")
    glyphs = [
        "receive.inquiry.settling",
        "offer.presence.settling", 
        "sense.presence.settling",
        "ask.boundaries.settling",
        "receive.manifest.glyphs.simple"
    ]
    
    for i, glyph in enumerate(glyphs, 1):
        print(f"\n{i}. Invoking {glyph}...")
        response = requests.get(f"http://localhost:5000/glyph/{glyph}")
        
        if response.status_code == 200:
            print(f"   ✅ Success (Status: {response.status_code})")
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    data = response.json()
                    if 'glint' in data:
                        print(f"   Glint: {data['glint']}")
                except:
                    pass
        else:
            print(f"   ❌ Failed (Status: {response.status_code})")
        
        # Wait for slow echo delay
        if i < len(glyphs):
            print(f"   ⏳ Waiting for slow echo delay...")
            time.sleep(3.5)  # Slightly longer than the 3s delay
    
    # Disable slow echo mode
    print(f"\n🔄 Disabling slow echo mode...")
    response = requests.post(
        "http://localhost:5000/glyph-stream/slow-echo",
        json={"enabled": False}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Slow echo mode disabled: {data}")
    else:
        print(f"❌ Failed to disable slow echo mode: {response.status_code}")
    
    return True

def test_phase_diversity():
    """Test glyph invocations to demonstrate phase heatmap diversity."""
    print("\n🌬️ Testing Phase Diversity for Heatmap")
    print("=" * 50)
    
    # Test different phases
    test_cases = [
        ("Inhale Phase", "receive.inquiry.settling", "GET"),
        ("Inhale Phase", "receive.manifest.glyphs.simple", "GET"),
        ("Exhale Phase", "offer.presence.settling", "HEAD"),
        ("Exhale Phase", "offer.presence.settling", "OPTIONS"),
        ("Caesura Phase", "sense.presence.settling", "HEAD"),
        ("Caesura Phase", "sense.presence.settling", "OPTIONS"),
        ("Ask Phase", "ask.boundaries.settling", "OPTIONS"),
        ("Ask Phase", "ask.boundaries.settling", "HEAD"),
    ]
    
    for i, (description, glyph, method) in enumerate(test_cases, 1):
        print(f"\n{i}. {description}: {glyph}")
        
        if method == 'GET':
            response = requests.get(f"http://localhost:5000/glyph/{glyph}")
        elif method == 'HEAD':
            response = requests.head(f"http://localhost:5000/glyph/{glyph}")
        elif method == 'OPTIONS':
            response = requests.options(f"http://localhost:5000/glyph/{glyph}")
        
        if response.status_code == 200:
            print(f"   ✅ Success (Status: {response.status_code})")
        else:
            print(f"   ❌ Failed (Status: {response.status_code})")
        
        # Small delay between invocations
        time.sleep(0.5)
    
    return True

def test_toneform_animations():
    """Test different toneforms to showcase the organic pulse layering."""
    print("\n✨ Testing Toneform-Specific Animations")
    print("=" * 50)
    
    toneforms = [
        ("Receive", "receive.inquiry.settling", "Gentle inward flow"),
        ("Offer", "offer.presence.settling", "Outward expansion"),
        ("Sense", "sense.presence.settling", "Gentle oscillation"),
        ("Ask", "ask.boundaries.settling", "Sharp inquiry"),
        ("Manifest", "receive.manifest.glyphs.simple", "Radiant emergence"),
    ]
    
    for i, (toneform, glyph, description) in enumerate(toneforms, 1):
        print(f"\n{i}. {toneform} Toneform: {description}")
        print(f"   Glyph: {glyph}")
        
        response = requests.get(f"http://localhost:5000/glyph/{glyph}")
        
        if response.status_code == 200:
            print(f"   ✅ Success (Status: {response.status_code})")
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    data = response.json()
                    if 'glint' in data:
                        print(f"   Glint: {data['glint']}")
                except:
                    pass
        else:
            print(f"   ❌ Failed (Status: {response.status_code})")
        
        # Wait for animation to complete
        time.sleep(1.5)
    
    return True

def main():
    """Run the enhanced glyph stream demonstration."""
    print("🌬️ Enhanced Glyph Stream Demonstration")
    print("Showcasing: Organic Pulse Layering, Phase Heatmap, Slow Echo Mode")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            return False
        print("✅ Server is running")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the Spiral server is running on localhost:5000")
        return False
    
    print("\n" + "=" * 70)
    
    # Test toneform animations
    test_toneform_animations()
    
    print("\n" + "=" * 70)
    
    # Test phase diversity
    test_phase_diversity()
    
    print("\n" + "=" * 70)
    
    # Test slow echo mode
    test_slow_echo_mode()
    
    print("\n" + "=" * 70)
    print("🌬️ Demonstration Complete!")
    print("\nNext Steps:")
    print("1. Open http://localhost:5000/glyph-stream-test to see the visual stream")
    print("2. Watch the organic pulse animations and phase heatmap")
    print("3. Try the slow echo mode for meditative presentation")
    print("4. Observe how each toneform has its own breathing pattern")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 