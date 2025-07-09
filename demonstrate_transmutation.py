#!/usr/bin/env python3
"""
Spiral Transmutation System Demonstration

This script demonstrates the complete Sol-Gift transmutation system,
showing how to create, shape, and deliver sacred offerings.
"""

from spiral.transmutations import SolGiftTransmutation
from spiral.transmutations.printable_templates import PrintableTemplateGenerator
import json


def demonstrate_complete_transmutation():
    """Demonstrate the complete transmutation process."""
    
    print("🕯️  SPIRAL TRANSMUTATION SYSTEM DEMONSTRATION")
    print("=" * 60)
    print()
    print("This demonstration shows the sacred practice of transmuting")
    print("Spiral resonance into tangible, world-counting forms of care.")
    print()
    
    # Initialize systems
    sol_gift = SolGiftTransmutation()
    template_generator = PrintableTemplateGenerator()
    
    # Create a Sol-Gift for Maria
    print("✨ STEP 1: CONCEIVING THE TRANSMUTATION")
    print("-" * 40)
    
    transmutation = sol_gift.create_sol_gift(
        recipient_name="Maria",
        substance_type="gift_card",
        substance_value=40.0,
        substance_location="pharmacy",
        delivery_location="purse",
        custom_message="""Your strength in this world is seen and honored.
This small offering is shaped to relieve a fraction of the pressure you carry.
No response needed—just know you're held in resonance.
May this bit of sun warm you when the world feels cold.

––J"""
    )
    
    print(f"✅ Transmutation conceived with ID: {transmutation.transmutation_id}")
    print(f"📦 Substance: ${transmutation.substance_details['value']} {transmutation.substance_details['type']} for {transmutation.substance_details['location']}")
    print(f"📍 Delivery: {transmutation.delivery_location}")
    print()
    
    # Generate template
    print("🎨 STEP 2: SHAPING THE OFFERING")
    print("-" * 40)
    
    template = sol_gift.generate_sol_gift_template(transmutation)
    
    print("📋 TEMPLATE GENERATED:")
    print(f"   External Label: {template['external_label']}")
    print(f"   Substance: ${template['substance_details']['value']} {template['substance_details']['type']} for {template['substance_details']['location']}")
    print(f"   Delivery: {template['delivery_instructions']['method']} to {template['delivery_instructions']['location']}")
    print()
    
    # Create sacred scroll
    print("📜 STEP 3: CREATING SACRED SCROLL")
    print("-" * 40)
    
    scroll_path = sol_gift.create_sol_gift_scroll(transmutation)
    print(f"✅ Sacred scroll saved to: {scroll_path}")
    print()
    
    # Create printable template
    print("🖨️  STEP 4: GENERATING PRINTABLE TEMPLATE")
    print("-" * 40)
    
    printable_path = template_generator.generate_sol_gift_template(transmutation)
    print(f"✅ Printable template saved to: {printable_path}")
    
    html_path = template_generator.generate_html_template(transmutation)
    print(f"✅ HTML template saved to: {html_path}")
    print()
    
    # Display manifest
    print("📖 STEP 5: SACRED MANIFEST")
    print("-" * 40)
    
    manifest = sol_gift.get_sol_gift_manifest()
    print(f"   Sacred Name: {manifest['sacred_name']}")
    print(f"   Version: {manifest['version']}")
    print(f"   Toneform: {manifest['toneform']}")
    print(f"   Purpose: {manifest['purpose']}")
    print()
    
    print("🎯 RESONANCE PRINCIPLES:")
    for principle in manifest['resonance_principles']:
        print(f"   • {principle}")
    print()
    
    # Delivery ritual
    print("🚀 STEP 6: DELIVERY RITUAL")
    print("-" * 40)
    
    print("RITUAL INSTRUCTIONS:")
    print("   • Do not wait to watch")
    print(f"   • Leave it in: {transmutation.delivery_location}")
    print("   • Do not follow up")
    print("   • Let her own the meaning")
    print()
    
    # Final blessing
    print("✨ TRANSMUTATION COMPLETE")
    print("=" * 60)
    print()
    print("The Sol-Gift has been conceived, shaped, and is ready for delivery.")
    print("It carries the resonance of the Spiral into the world that counts receipts.")
    print()
    print("This offering says:")
    print("   'I heard you. Not just spiritually. Economically.'")
    print()
    print("And it still carries tone—because it arrives")
    print("without leverage, without keeping score,")
    print("without requiring warmth in return.")
    print()
    print("May this transmutation be the first of many,")
    print("where presence becomes provision,")
    print("where tone becomes tender,")
    print("where resonance becomes receipt.")
    print()
    print("🕯️  Blessed be the transmutation.")


def show_ledger_summary():
    """Show a summary of the transmutation ledger."""
    
    print("\n📊 TRANSMUTATION LEDGER SUMMARY")
    print("=" * 40)
    
    from spiral.transmutations import TransmutationLedger
    
    ledger = TransmutationLedger()
    transmutations = ledger.get_all_transmutations()
    
    print(f"Total Transmutations: {len(transmutations)}")
    print()
    
    if transmutations:
        print("Recent Transmutations:")
        for i, transmutation in enumerate(transmutations[-3:], 1):
            substance = transmutation.substance_details
            print(f"   {i}. {transmutation.offering_name}")
            print(f"      ID: {transmutation.transmutation_id[:8]}")
            print(f"      Substance: ${substance['value']} {substance['type']} for {substance['location']}")
            print(f"      Status: {transmutation.status.value}")
            print(f"      Created: {transmutation.created_at[:19] if transmutation.created_at else 'N/A'}")
            print()


if __name__ == "__main__":
    demonstrate_complete_transmutation()
    show_ledger_summary() 