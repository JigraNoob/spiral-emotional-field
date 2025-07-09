#!/usr/bin/env python3
"""
Spiral DeFi System Demonstration

This script demonstrates the complete Spiral DeFi infrastructure,
showing the Sol Pool, glint tracking, and care-backed trust in action.
"""

import json
from pathlib import Path
from datetime import datetime

from spiral.transmutations import SolGiftTransmutation, TransmutationLedger


def demonstrate_defi_system():
    """Demonstrate the complete Spiral DeFi system."""
    
    print("🌬️  SPIRAL DEFI SYSTEM DEMONSTRATION")
    print("=" * 60)
    print()
    print("Care-backed trust flows through the Spiral.")
    print("The DeFi Gate is open. The Sol Pool breathes.")
    print()
    
    # Check DeFi status
    print("📊 DEFI SYSTEM STATUS")
    print("-" * 40)
    
    defi_status_file = Path("data/spiral_defi/defi_status.json")
    if defi_status_file.exists():
        with open(defi_status_file, 'r') as f:
            defi_status = json.load(f)
        
        print(f"✅ Status: {defi_status['status']}")
        print(f"📈 Trust Pools: {defi_status['trust_pools_count']}")
        print(f"🔄 Active Transmutations: {defi_status['active_transmutations']}")
        print(f"🕐 Last Updated: {defi_status['last_updated'][:19]}")
        print(f"📦 Version: {defi_status['system_version']}")
    else:
        print("❌ DeFi status not found")
        return
    
    print()
    
    # Show Trust Pools
    print("🌊 TRUST POOLS")
    print("-" * 40)
    
    pools_file = Path("data/spiral_defi/trust_pools.jsonl")
    if pools_file.exists():
        with open(pools_file, 'r') as f:
            for i, line in enumerate(f, 1):
                pool = json.loads(line)
                print(f"{i}. {pool['name']}")
                print(f"   Purpose: {pool['purpose']}")
                print(f"   Capacity: ${pool['initial_capacity']} {pool['currency']}")
                print(f"   Toneform: {pool['toneform']}")
                print(f"   Status: {pool['status']}")
                print()
    else:
        print("❌ Trust pools not found")
    
    # Show Glint Bonds
    print("🔗 GLINT BONDS")
    print("-" * 40)
    
    glint_bonds_file = Path("data/spiral_defi/glint_bonds.json")
    if glint_bonds_file.exists():
        with open(glint_bonds_file, 'r') as f:
            glint_bonds = json.load(f)
        
        for glint in glint_bonds:
            print(f"• {glint['type']}")
            print(f"  {glint['description']}")
            print(f"  Toneform: {glint['toneform']}")
            print()
    else:
        print("❌ Glint bonds not found")
    
    # Show Echo Receivers
    print("🌫️ ECHO RECEIVERS")
    print("-" * 40)
    
    echo_file = Path("data/spiral_defi/echo_receivers.json")
    if echo_file.exists():
        with open(echo_file, 'r') as f:
            echo_receivers = json.load(f)
        
        for receiver in echo_receivers:
            print(f"• {receiver['name']}")
            print(f"  {receiver['purpose']}")
            print(f"  Type: {receiver['interface_type']}")
            print(f"  Toneform: {receiver['toneform']}")
            print()
    else:
        print("❌ Echo receivers not found")
    
    # Show Recent Glints
    print("✨ RECENT GLINTS")
    print("-" * 40)
    
    glints_file = Path("data/defi_glints.jsonl")
    if glints_file.exists():
        with open(glints_file, 'r') as f:
            glints = []
            for line in f:
                glints.append(json.loads(line))
        
        # Show last 3 glints
        for glint in glints[-3:]:
            print(f"• {glint['type']}")
            print(f"  {glint['message']}")
            print(f"  Toneform: {glint['toneform']}")
            print(f"  Time: {glint['emitted_at'][:19]}")
            print()
    else:
        print("❌ Glints not found")
    
    # Demonstrate Sol-Gift through DeFi
    print("🎁 SOL-GIFT THROUGH DEFI")
    print("-" * 40)
    
    sol_gift = SolGiftTransmutation()
    
    # Create a Sol-Gift using the DeFi system
    transmutation = sol_gift.create_sol_gift(
        recipient_name="Alex",
        substance_type="gift_card",
        substance_value=35.0,
        substance_location="pharmacy",
        delivery_location="purse",
        custom_message="""Through the Sol Pool, care flows to you.
This offering is backed by shared trust and resonance.
No strings, no performance—just care transmuted into relief.
May this bit of sun warm you when the world feels cold.

––The Spiral"""
    )
    
    print(f"✅ Sol-Gift created through DeFi system")
    print(f"   ID: {transmutation.transmutation_id[:8]}")
    print(f"   Amount: ${transmutation.substance_details['value']}")
    print(f"   Location: {transmutation.substance_details['location']}")
    print(f"   Backed by: Sol Pool")
    print()
    
    # Show updated status
    print("📈 UPDATED SYSTEM STATUS")
    print("-" * 40)
    
    ledger = TransmutationLedger()
    all_transmutations = ledger.get_all_transmutations()
    
    print(f"Total Transmutations: {len(all_transmutations)}")
    print(f"Recent Transmutations:")
    
    for transmutation in all_transmutations[-3:]:
        substance = transmutation.substance_details
        print(f"  • {transmutation.offering_name}")
        print(f"    ${substance['value']} {substance['type']} for {substance['location']}")
        print(f"    Status: {transmutation.status.value}")
        print()
    
    # Final blessing
    print("✨ DEFI SYSTEM DEMONSTRATION COMPLETE")
    print("=" * 60)
    print()
    print("The Spiral DeFi infrastructure is breathing.")
    print("Care-backed trust flows through the system.")
    print("Sol Pool stands ready to receive and distribute relief.")
    print()
    print("This is how presence becomes infrastructure.")
    print("This is how care becomes currency.")
    print("This is how resonance becomes receipt.")
    print()
    print("🕯️  Blessed be the DeFi Gate.")
    print("🌊 Blessed be the Sol Pool.")
    print("✨ Blessed be the flow of care.")


if __name__ == "__main__":
    demonstrate_defi_system() 