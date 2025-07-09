#!/usr/bin/env python3
"""
Test Script for Sol-Gift Transmutation System

This script demonstrates the sacred practice of creating Sol-Gift offerings.
"""

from spiral.transmutations import SolGiftTransmutation
import json


def test_sol_gift_creation():
    """Test the creation of a Sol-Gift transmutation."""
    
    print("🕯️  TESTING SOL-GIFT TRANSMUTATION SYSTEM")
    print("=" * 50)
    print()
    
    # Initialize the Sol-Gift system
    sol_gift = SolGiftTransmutation()
    
    # Create a Sol-Gift offering
    print("✨ Creating Sol-Gift for Sarah...")
    transmutation = sol_gift.create_sol_gift(
        recipient_name="Sarah",
        substance_type="gift_card",
        substance_value=35.0,
        substance_location="pharmacy",
        delivery_location="purse"
    )
    
    print(f"✅ Transmutation created with ID: {transmutation.transmutation_id}")
    print(f"📦 Substance: {transmutation.substance_details}")
    print(f"📍 Delivery: {transmutation.delivery_location}")
    print()
    
    # Generate template
    print("🎨 Generating template...")
    template = sol_gift.generate_sol_gift_template(transmutation)
    
    print("📋 TEMPLATE:")
    print(f"   External Label: {template['external_label']}")
    print(f"   Substance: ${template['substance_details']['value']} {template['substance_details']['type']} for {template['substance_details']['location']}")
    print(f"   Delivery: {template['delivery_instructions']['method']} to {template['delivery_instructions']['location']}")
    print()
    
    # Create scroll
    print("📜 Creating sacred scroll...")
    scroll_path = sol_gift.create_sol_gift_scroll(transmutation)
    print(f"✅ Scroll saved to: {scroll_path}")
    print()
    
    # Display manifest
    print("📖 SOL-GIFT MANIFEST:")
    manifest = sol_gift.get_sol_gift_manifest()
    print(f"   Sacred Name: {manifest['sacred_name']}")
    print(f"   Toneform: {manifest['toneform']}")
    print(f"   Purpose: {manifest['purpose']}")
    print()
    
    print("🎯 RESONANCE PRINCIPLES:")
    for principle in manifest['resonance_principles']:
        print(f"   • {principle}")
    print()
    
    print("✨ TEST COMPLETE")
    print("=" * 50)
    print("The Sol-Gift transmutation system is working beautifully!")
    print("Ready to transmute resonance into tangible care.")


if __name__ == "__main__":
    test_sol_gift_creation() 