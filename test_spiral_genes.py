#!/usr/bin/env python3
"""
Test SpiralGene System ∷ Complete Integration Test

This script tests the entire SpiralGene system, including:
1. Gene initialization
2. Gene activation
3. Coin minting
4. Lineage visualization
"""

import sys
import os

# Add the spiral directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral'))

from spiral.spiral_genes import initialize_spiral_genes, activate_gene_with_glint
from spiral.mint_delta_004 import mint_delta_004_coin, verify_integration
from spiral.lineage_viewer import generate_d3_visualization_data, save_visualization_html
from spiral.glint_emitter import emit_glint


def test_spiral_gene_system():
    """Test the complete SpiralGene system."""
    
    print("🫧 SpiralGene System Integration Test")
    print("=" * 60)
    
    # Step 1: Initialize the genes
    print("\n1️⃣ Initializing SpiralGenes...")
    try:
        registry = initialize_spiral_genes()
        genes = registry.get_all_genes()
        print(f"✅ {len(genes)} genes initialized:")
        for gene in genes:
            print(f"   - {gene.gene_id}: {gene.name}")
    except Exception as e:
        print(f"❌ Failed to initialize genes: {e}")
        return False
    
    # Step 2: Test gene activation
    print("\n2️⃣ Testing gene activation...")
    try:
        activation_data = activate_gene_with_glint("∵S1", "test.activation")
        if activation_data:
            print(f"✅ ∵S1 activated successfully")
            print(f"   Activation count: {activation_data.get('activation_count', 'N/A')}")
        else:
            print("❌ ∵S1 activation failed")
            return False
    except Exception as e:
        print(f"❌ Failed to activate ∵S1: {e}")
        return False
    
    # Step 3: Mint Δ004 coin
    print("\n3️⃣ Minting Δ004 coin...")
    try:
        success = mint_delta_004_coin()
        if success:
            print("✅ Δ004 coin minted successfully")
        else:
            print("❌ Δ004 coin minting failed")
            return False
    except Exception as e:
        print(f"❌ Failed to mint Δ004: {e}")
        return False
    
    # Step 4: Verify integration
    print("\n4️⃣ Verifying integration...")
    try:
        verify_success = verify_integration()
        if verify_success:
            print("✅ Integration verified successfully")
        else:
            print("❌ Integration verification failed")
            return False
    except Exception as e:
        print(f"❌ Failed to verify integration: {e}")
        return False
    
    # Step 5: Test visualization
    print("\n5️⃣ Testing lineage visualization...")
    try:
        d3_data = generate_d3_visualization_data("∵S2")
        if d3_data:
            nodes = d3_data.get('nodes', [])
            links = d3_data.get('links', [])
            print(f"✅ Visualization data generated: {len(nodes)} nodes, {len(links)} links")
            
            # Save HTML visualization
            output_path = "static/gene_lineage_S2.html"
            html_success = save_visualization_html("∵S2", output_path)
            if html_success:
                print(f"✅ HTML visualization saved to {output_path}")
            else:
                print("⚠️ Failed to save HTML visualization")
        else:
            print("❌ Failed to generate visualization data")
            return False
    except Exception as e:
        print(f"❌ Failed to test visualization: {e}")
        return False
    
    # Step 6: Test lineage connections
    print("\n6️⃣ Testing lineage connections...")
    try:
        from spiral.spiral_genes import get_gene_lineage_visualization
        lineage_data = get_gene_lineage_visualization("∵S2")
        if lineage_data:
            connections = lineage_data.get('connections', [])
            coins = lineage_data.get('coins', [])
            print(f"✅ Lineage data retrieved: {len(connections)} connections, {len(coins)} coins")
            
            # Check for specific connections
            s1_connected = any(conn['id'] == '∵S1' for conn in connections)
            delta_004_present = any(coin['id'] == 'Δ004' for coin in coins)
            
            if s1_connected:
                print("✅ ∵S1 connection verified")
            else:
                print("❌ ∵S1 connection missing")
                return False
                
            if delta_004_present:
                print("✅ Δ004 coin verified in lineage")
            else:
                print("❌ Δ004 coin missing from lineage")
                return False
        else:
            print("❌ Failed to retrieve lineage data")
            return False
    except Exception as e:
        print(f"❌ Failed to test lineage connections: {e}")
        return False
    
    # Step 7: Emit completion glint
    print("\n7️⃣ Emitting completion glint...")
    try:
        emit_glint(
            phase="exhale",
            toneform="spiritual.completion",
            content="SpiralGene system integration test completed successfully",
            source="spiral.genes.test",
            metadata={
                "test_type": "complete_integration",
                "genes_tested": ["∵S1", "∵S2"],
                "coins_minted": ["Δ004"],
                "status": "success"
            }
        )
        print("✅ Completion glint emitted")
    except Exception as e:
        print(f"⚠️ Failed to emit completion glint: {e}")
    
    print("\n🎉 SpiralGene System Integration Test Completed Successfully!")
    print("   ∵S1 and ∵S2 are now living in your Spiral architecture")
    print("   Δ149 is linked to ∵S2 through Δ004")
    print("   Lineage visualization is available")
    
    return True


def main():
    """Main test function."""
    
    success = test_spiral_gene_system()
    
    if success:
        print("\n✅ All tests passed! The SpiralGene system is ready.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 