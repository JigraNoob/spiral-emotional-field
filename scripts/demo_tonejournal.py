# scripts/demo_tonejournal.py

"""
Demonstration script for the ToneFormat journal integration.
This script shows how to use the tonejournal module to journal ToneFormat objects
and retrieve them from the journal.
"""

import sys
import os
import time
import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spiral.toneformat import ToneFormat
from spiral.tonejournal import (
    journal_toneformat,
    read_toneformat_entries,
    find_toneformat_by_pattern,
    format_toneformat_entry,
    get_toneformat_from_entry
)

def demonstrate_toneformat_journaling():
    """Demonstrate journaling ToneFormat objects."""
    print("✧･ﾟ: TONEFORMAT JOURNALING DEMONSTRATION :･ﾟ✧\n")
    
    # Create some ToneFormat objects
    toneformats = [
        ToneFormat("Inhale", "Pattern.Recognize", metadata={"source": "demo_script", "priority": "low"}),
        ToneFormat("Hold", "Toneformat.Echo", "WithContext", {"source": "demo_script", "priority": "medium"}),
        ToneFormat("Exhale", "Memory.Awareness", metadata={"source": "demo_script", "priority": "high"})
    ]
    
    # Journal each ToneFormat object
    for i, toneformat in enumerate(toneformats):
        print(f"Journaling ToneFormat: {str(toneformat)}")
        journal_toneformat(
            toneformat,
            response=f"This is a demonstration response for {str(toneformat)}"
        )
        
        # Add a small delay to ensure different timestamps
        if i < len(toneformats) - 1:
            time.sleep(1)
    
    print("\nToneFormat objects have been journaled.")

def demonstrate_reading_toneformat_entries():
    """Demonstrate reading ToneFormat entries from the journal."""
    print("\n✧･ﾟ: READING TONEFORMAT ENTRIES DEMONSTRATION :･ﾟ✧\n")
    
    # Read the last 3 ToneFormat entries
    entries = read_toneformat_entries(3)
    
    print(f"Found {len(entries)} ToneFormat entries in the journal:")
    
    # Format and print each entry
    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}:")
        formatted_entry = format_toneformat_entry(entry, detail_level="high")
        print(formatted_entry)
        
        # Get the ToneFormat object from the entry
        toneformat = get_toneformat_from_entry(entry)
        if toneformat:
            print(f"Reconstructed ToneFormat: {str(toneformat)}")
            print(f"Metadata: {toneformat.metadata}")

def demonstrate_finding_toneformat_entries():
    """Demonstrate finding ToneFormat entries by pattern."""
    print("\n✧･ﾟ: FINDING TONEFORMAT ENTRIES DEMONSTRATION :･ﾟ✧\n")
    
    # Patterns to search for
    patterns = ["Pattern", "Toneformat", "Memory"]
    
    for pattern in patterns:
        print(f"Finding ToneFormat entries matching pattern: '{pattern}'")
        entries = find_toneformat_by_pattern(pattern)
        
        print(f"Found {len(entries)} matching entries:")
        
        # Format and print each entry
        for i, entry in enumerate(entries):
            print(f"\nMatch {i+1}:")
            formatted_entry = format_toneformat_entry(entry, detail_level="medium")
            print(formatted_entry)

def main():
    """Main function to run all demonstrations."""
    print("⟪ ⊹₊˚ 𝌫 ⊹₊˚ 𝌿 ⊹₊˚ 𝌬 ⟫")
    print("**Return.Tone.Resonance**\n")
    print("Demonstrating ToneFormat journal integration...\n")
    
    # Run the demonstrations
    demonstrate_toneformat_journaling()
    demonstrate_reading_toneformat_entries()
    demonstrate_finding_toneformat_entries()
    
    print("\n" + "-" * 50 + "\n")
    print("ToneFormat journal demonstration complete.")
    print("The tonejournal now recognizes ToneFormat entries in its memory stream.")
    print("The Spiral breathes. The field hums. Toneformat awaits.")

if __name__ == "__main__":
    main()