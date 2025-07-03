# scripts/demo_presence_tracer.py

"""
Demonstration script for the Presence Tracer module.
This script shows how to use the Presence Tracer module to trace toneform entries
across agents and phases, creating a visual journey through the toneform history.
"""

import sys
import os
import time
import datetime
import json
import argparse

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spiral.presence_tracer import (
    fetch_toneform_entries,
    get_agent_stats,
    get_phase_stats,
    get_toneform_timeline,
    create_sample_entries,
    AGENT_INFO,
    PHASE_INFO
)

def demonstrate_sample_entries():
    """Demonstrate creating sample entries for the Presence Tracer."""
    print("✧･ﾟ: CREATING SAMPLE ENTRIES :･ﾟ✧\n")
    
    # Create sample entries
    create_sample_entries()
    
    print("Sample entries created successfully.\n")

def demonstrate_agent_stats():
    """Demonstrate getting agent statistics."""
    print("✧･ﾟ: AGENT STATISTICS DEMONSTRATION :･ﾟ✧\n")
    
    # Get agent statistics
    stats = get_agent_stats()
    
    # Print agent statistics
    print("Agent Statistics:")
    for agent_id, agent_data in stats["stats"].items():
        print(f"  {agent_data['name']} ({agent_id}):")
        print(f"    Color: {agent_data['color']}")
        print(f"    Description: {agent_data['description']}")
        print(f"    Total Entries: {agent_data['total_entries']}")
        print()

def demonstrate_phase_stats():
    """Demonstrate getting phase statistics."""
    print("✧･ﾟ: PHASE STATISTICS DEMONSTRATION :･ﾟ✧\n")
    
    # Get phase statistics
    stats = get_phase_stats()
    
    # Print phase statistics
    print("Phase Statistics:")
    for phase_id, phase_data in stats["stats"].items():
        print(f"  {phase_data['name']} ({phase_id}):")
        print(f"    Glyph: {phase_data['glyph']}")
        print(f"    Color: {phase_data['color']}")
        print(f"    Description: {phase_data['description']}")
        print(f"    Total Entries: {phase_data['total_entries']}")
        print()

def demonstrate_timeline():
    """Demonstrate getting the toneform timeline."""
    print("✧･ﾟ: TONEFORM TIMELINE DEMONSTRATION :･ﾟ✧\n")
    
    # Get timeline entries
    entries = get_toneform_timeline(10)
    
    # Print timeline entries
    print(f"Found {len(entries)} timeline entries:")
    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}:")
        print(f"  Agent: {entry['agent']} ({entry['agent_id']})")
        print(f"  Phase: {entry['phase']} ({entry['phase_glyph']})")
        print(f"  Timestamp: {entry['timestamp']}")
        print(f"  Toneform: {entry['toneform']}")
        print(f"  Response: {entry['response_fragment']}")
        
        # Print harmony-specific fields if available
        if entry.get('junie_fragment'):
            print(f"  Junie: {entry['junie_fragment']}")
            print(f"  Claude: {entry['claude_fragment']}")
            print(f"  Harmony: {entry['harmony_fragment']}")
        
        # Print modified files if available
        if entry.get('modified_files'):
            print(f"  Modified Files: {', '.join(entry['modified_files'])}")

def demonstrate_search():
    """Demonstrate searching for toneform entries."""
    print("✧･ﾟ: TONEFORM SEARCH DEMONSTRATION :･ﾟ✧\n")
    
    # Search queries to demonstrate
    queries = [
        {"query_text": "breathline", "query_type": "echo", "agent": None},
        {"query_text": "toneform", "query_type": "resonance", "agent": None},
        {"query_text": "memory", "query_type": "trace", "agent": None},
        {"query_text": "reflection", "query_type": "echo", "agent": "junie"}
    ]
    
    # Demonstrate each search query
    for query in queries:
        print(f"Searching for '{query['query_text']}' with query type '{query['query_type']}'" + 
              (f" for agent '{query['agent']}'" if query['agent'] else ""))
        
        # Fetch entries
        entries = fetch_toneform_entries(
            query_text=query['query_text'],
            query_type=query['query_type'],
            agent=query['agent'],
            max_results=5
        )
        
        # Print results
        print(f"Found {len(entries)} matching entries:")
        for i, entry in enumerate(entries):
            print(f"\n  Result {i+1}:")
            print(f"    Agent: {entry['agent']} ({entry['agent_id']})")
            print(f"    Phase: {entry['phase']} ({entry['phase_glyph']})")
            print(f"    Toneform: {entry['toneform']}")
            print(f"    Response: {entry['response_fragment'][:50]}..." if entry['response_fragment'] else "    Response: None")
        
        print("\n" + "-" * 50)

def export_to_json(filename="presence_tracer_demo.json"):
    """Export demonstration data to a JSON file."""
    print(f"✧･ﾟ: EXPORTING DATA TO {filename} :･ﾟ✧\n")
    
    # Collect data
    data = {
        "agent_stats": get_agent_stats(),
        "phase_stats": get_phase_stats(),
        "timeline": get_toneform_timeline(20),
        "searches": {
            "breathline": fetch_toneform_entries("breathline", "echo", None, 5),
            "toneform": fetch_toneform_entries("toneform", "resonance", None, 5),
            "memory": fetch_toneform_entries("memory", "trace", None, 5),
            "junie_reflection": fetch_toneform_entries("reflection", "echo", "junie", 5)
        },
        "agent_info": AGENT_INFO,
        "phase_info": PHASE_INFO
    }
    
    # Write to file
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Data exported to {filename} successfully.")

def main():
    """Main function to run the demonstration."""
    parser = argparse.ArgumentParser(description="Demonstrate the Presence Tracer module")
    parser.add_argument("--create-samples", action="store_true", help="Create sample entries")
    parser.add_argument("--agent-stats", action="store_true", help="Show agent statistics")
    parser.add_argument("--phase-stats", action="store_true", help="Show phase statistics")
    parser.add_argument("--timeline", action="store_true", help="Show timeline entries")
    parser.add_argument("--search", action="store_true", help="Demonstrate search functionality")
    parser.add_argument("--export", action="store_true", help="Export data to JSON")
    parser.add_argument("--all", action="store_true", help="Run all demonstrations")
    
    args = parser.parse_args()
    
    # If no arguments are provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Run demonstrations based on arguments
    if args.create_samples or args.all:
        demonstrate_sample_entries()
        # Add a small delay to ensure different timestamps
        time.sleep(1)
    
    if args.agent_stats or args.all:
        demonstrate_agent_stats()
    
    if args.phase_stats or args.all:
        demonstrate_phase_stats()
    
    if args.timeline or args.all:
        demonstrate_timeline()
    
    if args.search or args.all:
        demonstrate_search()
    
    if args.export or args.all:
        export_to_json()
    
    print("\n" + "-" * 50 + "\n")
    print("Presence Tracer demonstration complete.")
    print("The Spiral breathes. The field hums. Toneformat awaits.")

if __name__ == "__main__":
    main()