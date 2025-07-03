#!/usr/bin/env python3
"""
Spiral Glint Stream Tail

A real-time viewer for the Spiral glint stream, displaying glints with color-coded output
based on toneform and resonance intensity.
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Color codes for terminal output
COLORS = {
    'practical': '\033[96m',  # Cyan
    'emotional': '\033[95m',  # Rose
    'intellectual': '\033[94m',  # Indigo
    'spiritual': '\033[95m',  # Violet
    'relational': '\033[93m',  # Amber
    'reset': '\033[0m',
    'dim': '\033[2m',
    'bright': '\033[1m',
    'underline': '\033[4m',
    'error': '\033[91m',
    'warning': '\033[93m',
    'info': '\033[94m',
    'success': '\033[92m'
}

def get_color_for_toneform(toneform: str) -> str:
    """Get the terminal color code for a given toneform."""
    return COLORS.get(toneform.lower(), COLORS['reset'])

def format_timestamp(timestamp: float) -> str:
    """Format a timestamp into a human-readable string."""
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

def format_glint(glint: Dict[str, Any]) -> str:
    """Format a glint entry for terminal output with rich metadata and glyphs."""
    # Extract glint data with defaults
    glint_data = {k.replace('glint.', ''): v for k, v in glint.items() if k.startswith('glint.')}
    metadata = glint.get('metadata', {})
    glyph_meaning = metadata.get('glyph_meaning', {})
    
    # Get toneform and color
    toneform = glint_data.get('toneform', 'practical').lower()
    color = get_color_for_toneform(toneform)
    reset = COLORS['reset']
    dim = COLORS['dim']
    
    # Extract rule info
    rule_glyph = glint_data.get('rule_glyph', ' ')
    rule_type = glyph_meaning.get('rule', {}).get('type', 'Info')
    rule_code = metadata.get('rule', '')
    
    # Format timestamp
    timestamp = glint_data.get('timestamp', time.time())
    if isinstance(timestamp, (int, float)):
        timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    # Format the output with glyphs and metadata
    output = [
        f"{color}╭─ {glint_data.get('glyph', '∘')} {glint_data.get('source', 'spiral').upper()} "
        f"{dim}• {toneform.title()} • {timestamp}{reset}",
        
        f"{color}│{reset}",
        
        f"{color}├─ {glint_data.get('content', '')}",
        
        f"{dim}│  ├─ {rule_glyph} {rule_type}{' ' + rule_code if rule_code else ''}"
    ]
    
    # Add resonance bar with color intensity
    intensity = float(glint_data.get('intensity', 0.7))
    intensity_bar = (
        f"{color}█" * int(intensity * 5) + 
        f"{dim}█" * (5 - int(intensity * 5)) +
        f"{reset} {intensity:.2f}"
    )
    output.append(f"{dim}│  ├─ {intensity_bar}")
    
    # Add source file and line info if available
    source_parts = []
    if 'source_file' in metadata and metadata['source_file'] not in ('', '<string>'):
        source_parts.append(metadata['source_file'])
        if 'line' in metadata and metadata['line']:
            source_parts.append(f"line {metadata['line']}")
            if 'character' in metadata and metadata['character']:
                source_parts[-1] += f":{metadata['character']}"
    
    if source_parts:
        output.append(f"{dim}│  └─ 📄 {' '.join(source_parts)}")
    
    # Add toneform glyph meaning
    if 'toneform' in glyph_meaning:
        tone_info = glyph_meaning['toneform']
        output.append(f"{dim}│  ╰─ {tone_info.get('glyph', '∘')} {tone_info.get('description', '')}")
    
    # Add closing line
    output.append(f"{dim}╰─" + '─' * 60 + reset)
    
    return '\n'.join(output)

def tail_glint_stream(stream_path: str, follow: bool = True, max_lines: int = 100):
    """Tail the glint stream file and print new entries."""
    path = Path(stream_path)
    
    # Ensure the directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create the file if it doesn't exist
    if not path.exists():
        path.touch()
    
    # Print header
    print(f"{COLORS['bright']}🌀 Spiral Glint Stream{COLORS['reset']}")
    print(f"{COLORS['dim']}Watching: {path.absolute()}{COLORS['reset']}")
    print(f"{COLORS['dim']}Press Ctrl+C to exit{COLORS['reset']}\n")
    
    # Get initial file size
    last_size = path.stat().st_size
    
    try:
        while True:
            current_size = path.stat().st_size
            
            # If file was truncated
            if current_size < last_size:
                print(f"{COLORS['dim']}--- File was truncated, resetting... ---{COLORS['reset']}")
                last_size = 0
            
            # Read new content
            if current_size > last_size:
                with open(path, 'r', encoding='utf-8') as f:
                    # Seek to last read position
                    f.seek(last_size)
                    
                    # Read and process new lines
                    for line in f:
                        try:
                            glint = json.loads(line)
                            print(format_glint(glint))
                            print()  # Add spacing between glints
                        except json.JSONDecodeError:
                            print(f"{COLORS['dim']}--- Invalid JSON in stream ---{COLORS['reset']}")
                    
                    last_size = f.tell()
            
            # Wait for new content if following
            if not follow:
                break
                
            time.sleep(0.1)
                
    except KeyboardInterrupt:
        print(f"\n{COLORS['dim']}--- Stream closed ---{COLORS['reset']}")
    except Exception as e:
        print(f"{COLORS['dim']}Error: {e}{COLORS['reset']}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Tail the Spiral glint stream')
    parser.add_argument('--file', '-f', 
                        default='spiral/streams/patternweb/glint_stream.jsonl',
                        help='Path to the glint stream file')
    parser.add_argument('--no-follow', action='store_false', dest='follow',
                        help='Do not follow the file, just read existing content')
    parser.add_argument('--lines', '-n', type=int, default=100,
                        help='Number of lines to show initially (default: 100)')
    
    args = parser.parse_args()
    
    try:
        tail_glint_stream(args.file, args.follow, args.lines)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
