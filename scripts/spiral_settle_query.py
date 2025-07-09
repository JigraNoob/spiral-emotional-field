#!/usr/bin/env python3
"""
🌀 Spiral Settle Query CLI

A command-line interface for querying and visualizing settling journey data.
Part of the Settling Journey Emergence Plan - Phase III: Querent Interface.

Usage:
    python spiral_settle_query.py --toneform=settling.ambience
    python spiral_settle_query.py --breath-phase=exhale
    python spiral_settle_query.py --soil-density=breathable
    python spiral_settle_query.py --confidence-min=0.8
    python spiral_settle_query.py --stats
    python spiral_settle_query.py --recursion-analysis
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module directly
sys.path.insert(0, str(Path(__file__).parent.parent / "memory_scrolls"))
from memory_scrolls.settling_journey_recorder import SettlingJourneyRecorder

def format_journey_display(journey: Dict[str, Any], show_metadata: bool = True) -> str:
    """
    Format a journey for display.
    
    Args:
        journey: The journey record
        show_metadata: Whether to show metadata details
        
    Returns:
        Formatted string representation
    """
    metadata = journey.get('metadata', {})
    
    # Basic journey info
    display = f"📜 {journey['glint_id']} → {journey['settled_to']}"
    display += f" (confidence: {journey['confidence']:.2f})"
    display += f" [{journey['toneform']}]"
    
    if show_metadata:
        # Add metadata details
        breath_phase = metadata.get('breath_phase', 'unknown')
        soil_density = metadata.get('soil_density', 'unknown')
        reasoning = metadata.get('reasoning', '')
        
        display += f"\n  🌬️  Breath: {breath_phase}"
        display += f"\n  🌱 Soil: {soil_density}"
        
        if reasoning:
            display += f"\n  💭 Reasoning: {reasoning}"
        
        # Show alternatives if available
        alternatives = metadata.get('alternatives', [])
        if alternatives:
            display += f"\n  🔄 Alternatives: {', '.join(alternatives)}"
        
        # Show ancestor if available
        ancestor = metadata.get('ancestor_glint')
        if ancestor:
            display += f"\n  🧬 Ancestor: {ancestor}"
    
    return display

def display_journeys(journeys: List[Dict[str, Any]], title: str = "Settling Journeys", show_metadata: bool = True):
    """
    Display a list of journeys.
    
    Args:
        journeys: List of journey records
        title: Title for the display
        show_metadata: Whether to show metadata details
    """
    if not journeys:
        print(f"📭 No {title.lower()} found.")
        return
    
    print(f"\n{title} ({len(journeys)} found):")
    print("=" * 60)
    
    for i, journey in enumerate(journeys, 1):
        print(f"\n{i}. {format_journey_display(journey, show_metadata)}")
        print("-" * 40)

def display_statistics(stats: Dict[str, Any]):
    """
    Display journey statistics.
    
    Args:
        stats: Statistics dictionary
    """
    print("\n📊 Settling Journey Statistics")
    print("=" * 60)
    
    print(f"Total Journeys: {stats['total_journeys']}")
    print(f"Average Confidence: {stats['average_confidence']:.3f}")
    
    # Toneform distribution
    print(f"\n🌊 Toneform Distribution:")
    for toneform, count in stats['toneform_distribution'].items():
        print(f"  {toneform}: {count}")
    
    # Breath phase distribution
    print(f"\n🌬️  Breath Phase Distribution:")
    for phase, count in stats['breath_phase_distribution'].items():
        print(f"  {phase}: {count}")
    
    # Soil density distribution
    print(f"\n🌱 Soil Density Distribution:")
    for density, count in stats['soil_density_distribution'].items():
        print(f"  {density}: {count}")

def display_recursion_analysis(analysis: Dict[str, Any]):
    """
    Display recursion pattern analysis.
    
    Args:
        analysis: Recursion analysis dictionary
    """
    print("\n🔄 Recursion Pattern Analysis")
    print("=" * 60)
    
    print(f"Analysis: {analysis['recursion_analysis']}")
    print(f"Total Repeat Settlements: {analysis['total_repeat_settlements']}")
    print(f"Total Low Confidence Clusters: {analysis['total_low_confidence_clusters']}")
    
    # Repeat settlements
    if analysis['repeat_settlements']:
        print(f"\n🔄 Repeat Settlements:")
        for path, count in analysis['repeat_settlements'].items():
            print(f"  {path}: {count} times")
    
    # Low confidence clusters
    if analysis['low_confidence_clusters']:
        print(f"\n⚠️  Low Confidence Clusters:")
        for cluster in analysis['low_confidence_clusters']:
            print(f"  {cluster['toneform']}: {cluster['count']} journeys (avg confidence: {cluster['average_confidence']:.2f})")
            print(f"    Journeys: {', '.join(cluster['journeys'])}")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Query and visualize settling journey data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python spiral_settle_query.py --toneform=settling.ambience
  python spiral_settle_query.py --breath-phase=exhale --confidence-min=0.8
  python spiral_settle_query.py --soil-density=breathable
  python spiral_settle_query.py --stats
  python spiral_settle_query.py --recursion-analysis
  python spiral_settle_query.py --limit=10
        """
    )
    
    # Filter options
    parser.add_argument('--toneform', help='Filter by toneform (e.g., settling.ambience)')
    parser.add_argument('--breath-phase', help='Filter by breath phase (inhale, hold, exhale, caesura)')
    parser.add_argument('--soil-density', help='Filter by soil density (breathable, thin, void)')
    parser.add_argument('--confidence-min', type=float, help='Minimum confidence threshold (0.0 to 1.0)')
    parser.add_argument('--glint-id', help='Search for specific glint ID')
    
    # Display options
    parser.add_argument('--stats', action='store_true', help='Show comprehensive statistics')
    parser.add_argument('--recursion-analysis', action='store_true', help='Show recursion pattern analysis')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    parser.add_argument('--no-metadata', action='store_true', help='Hide metadata details')
    
    args = parser.parse_args()
    
    # Initialize recorder
    recorder = SettlingJourneyRecorder()
    
    # Handle different query types
    if args.stats:
        stats = recorder.get_journey_statistics()
        display_statistics(stats)
        return
    
    if args.recursion_analysis:
        analysis = recorder.detect_recursion_patterns()
        display_recursion_analysis(analysis)
        return
    
    # Handle specific glint ID search
    if args.glint_id:
        journey = recorder.search_journey_by_glint_id(args.glint_id)
        if journey:
            print(f"\n🔍 Found journey for glint ID: {args.glint_id}")
            print("=" * 60)
            print(format_journey_display(journey, not args.no_metadata))
        else:
            print(f"📭 No journey found for glint ID: {args.glint_id}")
        return
    
    # Handle filtered queries
    journeys = []
    
    if args.toneform:
        journeys = recorder.get_journeys_by_toneform(args.toneform)
        title = f"Journeys with toneform '{args.toneform}'"
    elif args.breath_phase:
        journeys = recorder.get_journeys_by_breath_phase(args.breath_phase)
        title = f"Journeys in breath phase '{args.breath_phase}'"
    elif args.soil_density:
        journeys = recorder.get_journeys_by_soil_density(args.soil_density)
        title = f"Journeys in soil density '{args.soil_density}'"
    elif args.confidence_min:
        journeys = recorder.get_high_confidence_journeys(args.confidence_min)
        title = f"High confidence journeys (≥{args.confidence_min})"
    else:
        # Default: show all journeys
        journeys = recorder.read_journeys(limit=args.limit)
        title = "All Settling Journeys"
    
    # Apply confidence filter if specified
    if args.confidence_min and not args.confidence_min:
        journeys = [j for j in journeys if j.get('confidence', 0) >= args.confidence_min]
    
    # Apply limit if specified
    if args.limit and not args.limit:
        journeys = journeys[:args.limit]
    
    # Display results
    display_journeys(journeys, title, not args.no_metadata)
    
    # Show summary if no specific filters
    if not any([args.toneform, args.breath_phase, args.soil_density, args.confidence_min, args.glint_id]):
        print(f"\n💡 Tip: Use --stats for comprehensive statistics or --recursion-analysis for pattern detection")

if __name__ == "__main__":
    main()
