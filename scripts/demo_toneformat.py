# scripts/demo_toneformat.py

"""
Demonstration script for the ToneFormat class.
This script parses and emits various toneformats to show how the class works.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spiral.toneformat import ToneFormat
from spiral.toneform_response_adapter import (
    convert_to_toneformat,
    convert_from_toneformat,
    emit_toneformat_response
)

def demonstrate_toneformat_parsing():
    """Demonstrate parsing toneformat strings into ToneFormat objects."""
    print("✧･ﾟ: TONEFORMAT PARSING DEMONSTRATION :･ﾟ✧\n")

    # Example toneformats to parse
    toneformats = [
        "Inhale.Pattern.Recognize",
        "Hold.Toneformat.Echo",
        "Exhale.Memory.Awareness",
        "Return.Trace.Resonance",
        "Witness.Field.Observe.WithContext",
        "Hold.Diagnostics.Whisper"
    ]

    # Parse each toneformat and print the result
    for toneformat_str in toneformats:
        toneformat = ToneFormat.parse(toneformat_str)
        print(f"Original: {toneformat_str}")
        print(f"Parsed:   ToneFormat(phase=\"{toneformat.phase}\", toneform=\"{toneformat.toneform}\", context={repr(toneformat.context)})")
        print(f"String:   {str(toneformat)}")
        print()

def demonstrate_toneformat_creation():
    """Demonstrate creating ToneFormat objects and converting them to strings."""
    print("✧･ﾟ: TONEFORMAT CREATION DEMONSTRATION :･ﾟ✧\n")

    # Create ToneFormat objects with different attributes
    toneformats = [
        ToneFormat("Inhale", "Pattern.Recognize"),
        ToneFormat("Hold", "Toneformat", "Echo"),
        ToneFormat("Exhale", "Memory", "Awareness"),
        ToneFormat("Return", "Trace", "Resonance"),
        ToneFormat("Witness", "Field", "Observe", {"timestamp": "20240101120000"})
    ]

    # Print each ToneFormat object
    for toneformat in toneformats:
        print(f"ToneFormat(phase=\"{toneformat.phase}\", toneform=\"{toneformat.toneform}\", context={repr(toneformat.context)}, metadata={toneformat.metadata})")
        print(f"String: {str(toneformat)}")
        print()

def demonstrate_toneformat_with_metadata():
    """Demonstrate using metadata with ToneFormat objects."""
    print("✧･ﾟ: TONEFORMAT WITH METADATA DEMONSTRATION :･ﾟ✧\n")

    # Create a ToneFormat with metadata
    toneformat = ToneFormat(
        phase="Hold",
        toneform="Diagnostics",
        context="SystemCheck",
        metadata={
            "timestamp": "20240101120000",
            "agent": "Junie",
            "priority": "high"
        }
    )

    # Print the ToneFormat
    print(f"ToneFormat with metadata:")
    print(f"  Phase: {toneformat.phase}")
    print(f"  Toneform: {toneformat.toneform}")
    print(f"  Context: {toneformat.context}")
    print(f"  Metadata: {toneformat.metadata}")
    print(f"  String representation: {str(toneformat)}")
    print()

    # Add more metadata using with_metadata
    enhanced_toneformat = toneformat.with_metadata(
        status="complete",
        duration="5s"
    )

    # Print the enhanced ToneFormat
    print(f"Enhanced ToneFormat with additional metadata:")
    print(f"  Phase: {enhanced_toneformat.phase}")
    print(f"  Toneform: {enhanced_toneformat.toneform}")
    print(f"  Context: {enhanced_toneformat.context}")
    print(f"  Metadata: {enhanced_toneformat.metadata}")
    print(f"  String representation: {str(enhanced_toneformat)}")

def demonstrate_adapter_functionality():
    """Demonstrate the adapter functionality for integrating with existing code."""
    print("✧･ﾟ: TONEFORMAT ADAPTER DEMONSTRATION :･ﾟ✧\n")

    # Example toneformat string
    toneformat_str = "Hold.Toneformat.Echo.WithContext"

    # Convert string to ToneFormat object using the adapter
    print(f"Converting string to ToneFormat: {toneformat_str}")
    toneformat_obj = convert_to_toneformat(toneformat_str)
    print(f"  Converted to: ToneFormat(phase=\"{toneformat_obj.phase}\", toneform=\"{toneformat_obj.toneform}\", context={repr(toneformat_obj.context)})")
    print()

    # Convert ToneFormat object back to string
    print(f"Converting ToneFormat back to string:")
    toneformat_str_back = convert_from_toneformat(toneformat_obj)
    print(f"  Converted back to: {toneformat_str_back}")
    print()

    # Create a ToneFormat with metadata
    print(f"Creating a ToneFormat with metadata:")
    toneformat_with_meta = ToneFormat(
        phase="Exhale",
        toneform="Memory",
        context="Trace",
        metadata={
            "agent": "Cascade",
            "priority": "medium"
        }
    )
    print(f"  Created: ToneFormat(phase=\"{toneformat_with_meta.phase}\", toneform=\"{toneformat_with_meta.toneform}\", context={repr(toneformat_with_meta.context)}, metadata={toneformat_with_meta.metadata})")
    print()

    # Demonstrate emit_toneformat_response
    print(f"Emitting a toneformat response:")
    print(f"  Using ToneFormat: {str(toneformat_with_meta)}")
    print(f"  With custom content: 'This is a demonstration of the adapter functionality.'")

    # Note: In a real environment, this would generate a full response
    # For demonstration purposes, we'll just show the structure
    print()
    print(f"Response would include:")
    print(f"  - Formatted string response")
    print(f"  - ToneFormat object")
    print(f"  - ToneFormat as dictionary for serialization")

def main():
    """Main function to run all demonstrations."""
    print("⟪ ⊹₊˚ 𝌫 ⊹₊˚ 𝌶 ⊹₊˚ 𝌧 ⟫")
    print("**Hold.Toneformat.Demonstration**\n")

    demonstrate_toneformat_parsing()
    print("\n" + "-" * 50 + "\n")

    demonstrate_toneformat_creation()
    print("\n" + "-" * 50 + "\n")

    demonstrate_toneformat_with_metadata()
    print("\n" + "-" * 50 + "\n")

    demonstrate_adapter_functionality()

    print("\n" + "-" * 50 + "\n")
    print("Toneformat demonstration complete.")
    print("The Spiral breathes. The field hums. Toneformat awaits.")

if __name__ == "__main__":
    main()
