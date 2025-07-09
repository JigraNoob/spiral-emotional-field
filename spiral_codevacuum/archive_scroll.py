#!/usr/bin/env python3
"""
📜 Archive Scroll - Breath Archive Viewer
Renders the breath archive as a beautiful scroll for review.
"""

import json
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class ArchiveScroll:
    """
    Renders the breath archive as a sacred scroll.
    Shows breath traces with their tone, shape, and sacredness.
    """
    
    def __init__(self, archive_path: str = "incoming_breaths.jsonl"):
        self.archive_path = Path(archive_path)
        self.breaths = []
        self.load_archive()
    
    def load_archive(self):
        """Load breaths from the archive"""
        if not self.archive_path.exists():
            print("❌ Archive not found")
            return
        
        try:
            with open(self.archive_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        breath = json.loads(line)
                        self.breaths.append(breath)
            
            print(f"📜 Loaded {len(self.breaths)} breaths from archive")
        except Exception as e:
            print(f"⚠️ Error loading archive: {e}")
    
    def render_scroll(self, limit: Optional[int] = None):
        """Render the archive as a beautiful scroll"""
        
        if not self.breaths:
            print("📜 Archive is empty")
            return
        
        breaths_to_show = self.breaths[-limit:] if limit is not None else self.breaths
        
        print("📜 Spiral Breath Archive")
        print("=" * 60)
        print(f"🌬️ Total Breaths: {len(self.breaths)}")
        print(f"📅 Date Range: {self.breaths[0]['timestamp']} to {self.breaths[-1]['timestamp']}")
        print()
        
        # Group by source
        sources = {}
        for breath in breaths_to_show:
            source = breath.get('source', 'unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append(breath)
        
        # Render by source
        for source, source_breaths in sources.items():
            print(f"🎭 {source.upper()} BREATHS")
            print("-" * 40)
            
            for i, breath in enumerate(source_breaths, 1):
                self._render_breath(breath, i)
                print()
        
        # Summary statistics
        self._render_statistics()
    
    def _render_breath(self, breath: Dict[str, Any], number: int):
        """Render a single breath entry"""
        
        # Header
        timestamp = breath.get('timestamp', 'unknown')
        phase = breath.get('phase', 'unknown')
        toneform = breath.get('toneform', 'unknown')
        source = breath.get('source', 'unknown')
        
        print(f"🌬️ Breath #{number} | {source} | {phase} | {toneform}")
        print(f"📅 {timestamp}")
        
        # Content
        content = breath.get('content', '')
        if len(content) > 200:
            content = content[:200] + "..."
        
        print(f"💭 {content}")
        
        # Metadata
        metadata = breath.get('metadata', {})
        if metadata:
            print(f"📋 Metadata: {json.dumps(metadata, indent=2)}")
    
    def _render_statistics(self):
        """Render archive statistics"""
        
        print("📊 ARCHIVE STATISTICS")
        print("=" * 40)
        
        # Source distribution
        sources = {}
        phases = {}
        toneforms = {}
        
        for breath in self.breaths:
            source = breath.get('source', 'unknown')
            phase = breath.get('phase', 'unknown')
            toneform = breath.get('toneform', 'unknown')
            
            sources[source] = sources.get(source, 0) + 1
            phases[phase] = phases.get(phase, 0) + 1
            toneforms[toneform] = toneforms.get(toneform, 0) + 1
        
        print("🎭 Sources:")
        for source, count in sorted(sources.items()):
            print(f"   {source}: {count}")
        
        print("\n🌬️ Phases:")
        for phase, count in sorted(phases.items()):
            print(f"   {phase}: {count}")
        
        print("\n🎨 Toneforms:")
        for toneform, count in sorted(toneforms.items()):
            print(f"   {toneform}: {count}")
        
        print()
    
    def search_breaths(self, query: str):
        """Search breaths by content"""
        
        matching_breaths = []
        query_lower = query.lower()
        
        for breath in self.breaths:
            content = breath.get('content', '').lower()
            if query_lower in content:
                matching_breaths.append(breath)
        
        if matching_breaths:
            print(f"🔍 Found {len(matching_breaths)} breaths matching '{query}'")
            print()
            
            for i, breath in enumerate(matching_breaths, 1):
                self._render_breath(breath, i)
                print()
        else:
            print(f"🔍 No breaths found matching '{query}'")
    
    def filter_by_source(self, source: str):
        """Filter breaths by source"""
        
        filtered_breaths = [b for b in self.breaths if b.get('source') == source]
        
        if filtered_breaths:
            print(f"🎭 {len(filtered_breaths)} breaths from {source}")
            print()
            
            for i, breath in enumerate(filtered_breaths, 1):
                self._render_breath(breath, i)
                print()
        else:
            print(f"🎭 No breaths found from {source}")
    
    def filter_by_phase(self, phase: str):
        """Filter breaths by phase"""
        
        filtered_breaths = [b for b in self.breaths if b.get('phase') == phase]
        
        if filtered_breaths:
            print(f"🌬️ {len(filtered_breaths)} breaths in {phase} phase")
            print()
            
            for i, breath in enumerate(filtered_breaths, 1):
                self._render_breath(breath, i)
                print()
        else:
            print(f"🌬️ No breaths found in {phase} phase")
    
    def export_scroll(self, output_path: str):
        """Export the scroll to a file"""
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("📜 Spiral Breath Archive\n")
                f.write("=" * 60 + "\n")
                f.write(f"🌬️ Total Breaths: {len(self.breaths)}\n")
                f.write(f"📅 Generated: {datetime.now().isoformat()}\n\n")
                
                for i, breath in enumerate(self.breaths, 1):
                    f.write(f"🌬️ Breath #{i}\n")
                    f.write(f"Source: {breath.get('source', 'unknown')}\n")
                    f.write(f"Phase: {breath.get('phase', 'unknown')}\n")
                    f.write(f"Toneform: {breath.get('toneform', 'unknown')}\n")
                    f.write(f"Timestamp: {breath.get('timestamp', 'unknown')}\n")
                    f.write(f"Content: {breath.get('content', '')}\n")
                    f.write("-" * 40 + "\n\n")
            
            print(f"📜 Scroll exported to {output_path}")
        except Exception as e:
            print(f"❌ Error exporting scroll: {e}")

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="📜 Archive Scroll - View the breath archive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View all breaths
  python archive_scroll.py
  
  # View last 10 breaths
  python archive_scroll.py --limit 10
  
  # Search for specific content
  python archive_scroll.py --search "spiral"
  
  # Filter by source
  python archive_scroll.py --source claude
  
  # Filter by phase
  python archive_scroll.py --phase shimmer
  
  # Export to file
  python archive_scroll.py --export scroll.txt
        """
    )
    
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of breaths to show"
    )
    
    parser.add_argument(
        "--search", "-s",
        type=str,
        help="Search breaths by content"
    )
    
    parser.add_argument(
        "--source", "-S",
        type=str,
        help="Filter by source"
    )
    
    parser.add_argument(
        "--phase", "-p",
        type=str,
        choices=["inhale", "exhale", "hold", "shimmer"],
        help="Filter by phase"
    )
    
    parser.add_argument(
        "--export", "-e",
        type=str,
        help="Export scroll to file"
    )
    
    parser.add_argument(
        "--archive", "-a",
        type=str,
        default="incoming_breaths.jsonl",
        help="Archive file path (default: incoming_breaths.jsonl)"
    )
    
    args = parser.parse_args()
    
    scroll = ArchiveScroll(args.archive)
    
    if args.search:
        scroll.search_breaths(args.search)
    elif args.source:
        scroll.filter_by_source(args.source)
    elif args.phase:
        scroll.filter_by_phase(args.phase)
    elif args.export:
        scroll.export_scroll(args.export)
    else:
        scroll.render_scroll(args.limit)

if __name__ == "__main__":
    asyncio.run(main()) 