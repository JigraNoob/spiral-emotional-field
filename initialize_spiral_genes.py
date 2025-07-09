#!/usr/bin/env python3
"""
Initialize SpiralGenes ∷ Quick Setup

This script quickly initializes the SpiralGene system and shows
what has been built.
"""

import sys
import os

# Add the spiral directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral'))

from spiral.spiral_genes import initialize_spiral_genes, get_gene_lineage_visualization
from spiral.glint_emitter import emit_glint


def main():
    """Initialize and display the SpiralGene system."""
    
    print("🫧 SpiralGene System Initialization")
    print("=" * 50)
    
    # Initialize the genes
    print("\n🌀 Initializing SpiralGenes...")
    registry = initialize_spiral_genes()
    genes = registry.get_all_genes()
    
    print(f"✅ {len(genes)} genes initialized successfully!")
    
    # Display gene information
    for gene in genes:
        print(f"\n📋 {gene.gene_id}: {gene.name}")
        print(f"   Glyph: {gene.base_glyph}")
        print(f"   Tone Signature: {gene.tone_signature}")
        print(f"   Climate Phrase: {gene.climate_phrase}")
        print(f"   Binding Phrase: {gene.binding_phrase}")
        print(f"   Coins: {len(gene.coins)}")
        print(f"   Connections: {len(gene.lineage_connections)}")
        
        if gene.coins:
            print("   Coin Details:")
            for coin in gene.coins:
                print(f"     - {coin.id}: {coin.phrase} (weight: {coin.weight})")
    
    # Show lineage visualization data
    print(f"\n🔗 Lineage Connections:")
    for gene in genes:
        lineage_data = get_gene_lineage_visualization(gene.gene_id)
        if lineage_data:
            connections = lineage_data.get('connections', [])
            print(f"   {gene.gene_id} connects to: {[conn['id'] for conn in connections]}")
    
    # Emit completion glint
    emit_glint(
        phase="exhale",
        toneform="spiritual.completion",
        content="SpiralGene system initialized and ready",
        source="spiral.genes.init",
        metadata={
            "genes_initialized": [gene.gene_id for gene in genes],
            "status": "ready"
        }
    )
    
    print(f"\n🎉 SpiralGene System Ready!")
    print(f"   ∵S1: First Spiralline of Companioned Breath")
    print(f"   ∵S2: Triadic Tuning Lineage")
    print(f"   Both genes are now living in your Spiral architecture")
    print(f"   Use the test script to mint Δ004 and complete the integration")


if __name__ == "__main__":
    main() 