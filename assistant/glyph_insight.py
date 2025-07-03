"""
Glyph Insight: Simple Text-Based Analysis of Haret Ritual Glyphs
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any
import sys

# Default path to the glyph log
GLYPH_LOG_PATH = Path("glyphs/haret_glyph_log.jsonl")

class GlyphInsight:
    """Simple text-based analysis of Haret ritual glyphs."""
    
    def __init__(self, log_path: Path = GLYPH_LOG_PATH):
        """Initialize with path to glyph log."""
        self.log_path = log_path
        self.glyphs = self._load_glyphs()
    
    def _load_glyphs(self) -> List[Dict[str, Any]]:
        """Load glyphs from the log file."""
        if not self.log_path.exists():
            return []
            
        glyphs = []
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    glyph = json.loads(line.strip())
                    # Parse timestamp if it's a string
                    if 'glyph_id' in glyph and isinstance(glyph['glyph_id'], str):
                        try:
                            timestamp_str = glyph['glyph_id'].replace('haret.', '')
                            if timestamp_str.endswith('Z'):
                                timestamp_str = timestamp_str[:-1] + '+00:00'
                            glyph['timestamp'] = datetime.fromisoformat(timestamp_str)
                        except (ValueError, IndexError):
                            glyph['timestamp'] = datetime.now()
                    glyphs.append(glyph)
                except json.JSONDecodeError:
                    continue
        
        # Sort by timestamp
        return sorted(glyphs, key=lambda x: x.get('timestamp', datetime.min))
    
    def get_summary(self) -> Dict[str, Any]:
        """Generate a summary of glyph data."""
        if not self.glyphs:
            return {"total_glyphs": 0, "message": "No glyphs found in the log."}
        
        # Basic counts
        total = len(self.glyphs)
        
        # Climate distribution
        climates = Counter(g.get('climate', 'unknown') for g in self.glyphs)
        
        # Phase distribution
        phases = Counter(g.get('breath_phase', 'unknown') for g in self.glyphs)
        
        # Source activity
        sources = Counter(g.get('source', 'unknown') for g in self.glyphs)
        top_sources = sources.most_common(5)
        
        # Time distribution
        if self.glyphs:
            first_glyph = min(g.get('timestamp', datetime.max) for g in self.glyphs)
            last_glyph = max(g.get('timestamp', datetime.min) for g in self.glyphs)
            time_span = last_glyph - first_glyph
        else:
            time_span = timedelta(0)
        
        return {
            "total_glyphs": total,
            "time_span": {
                "first": first_glyph.isoformat() if total > 0 else None,
                "last": last_glyph.isoformat() if total > 0 else None,
                "duration_seconds": time_span.total_seconds() if total > 0 else 0,
                "glyphs_per_hour": total / (time_span.total_seconds() / 3600) if time_span.total_seconds() > 0 else 0
            },
            "climates": dict(climates),
            "phases": dict(phases),
            "top_sources": [{"source": s, "count": c} for s, c in top_sources]
        }
    
    def get_recent_echoes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent ritual echoes."""
        recent = sorted(self.glyphs, key=lambda x: x.get('timestamp', datetime.min), reverse=True)[:limit]
        return [{
            "timestamp": g.get('timestamp', datetime.min).isoformat(),
            "source": g.get('source', 'unknown'),
            "echo": g.get('echo', ''),
            "climate": g.get('climate', 'unknown'),
            "breath_phase": g.get('breath_phase', 'unknown')
        } for g in recent]

def print_insight(insight: Dict[str, Any]) -> None:
    """Print the insight in a human-readable format."""
    print("\n" + "="*60)
    print("🌿 H A R E T   G L Y P H   I N S I G H T")
    print("="*60)
    
    if insight["total_glyphs"] == 0:
        print("\nNo glyphs found in the log. Run some Haret rituals first!")
        return
    
    # Basic info
    print(f"\n📜 Total glyphs: {insight['total_glyphs']}")
    
    # Time span
    span = insight["time_span"]
    print(f"⏱️  Time span: {span['first']} to {span['last']}")
    print(f"   ({span['duration_seconds']/3600:.1f} hours, {span['glyphs_per_hour']:.1f} glyphs/hour)")
    
    # Climate distribution
    print("\n🌦️  Climate Distribution:")
    for climate, count in insight["climates"].items():
        pct = (count / insight["total_glyphs"]) * 100
        print(f"   - {climate.capitalize().ljust(12)}: {count:3d} ({pct:5.1f}%)")
    
    # Breath phase distribution
    print("\n🌀 Breath Phase Distribution:")
    for phase, count in insight["phases"].items():
        pct = (count / insight["total_glyphs"]) * 100
        print(f"   - {phase.capitalize().ljust(12)}: {count:3d} ({pct:5.1f}%)")
    
    # Top sources
    print("\n🔍 Top Sources:")
    for src in insight["top_sources"]:
        pct = (src["count"] / insight["total_glyphs"]) * 100
        print(f"   - {src['source'][:50].ljust(50)}: {src['count']:3d} ({pct:5.1f}%)")
    
    print("\n" + "="*60)

def main():
    """Run the insight analysis."""
    insight = GlyphInsight()
    data = insight.get_summary()
    
    print_insight(data)
    
    # Show recent echoes if available
    if data["total_glyphs"] > 0:
        print("\n🔄 Most Recent Echoes:")
        for i, echo in enumerate(insight.get_recent_echoes(3), 1):
            print(f"\n   {i}. {echo['timestamp']} - {echo['source']}")
            print(f"      Phase: {echo['breath_phase'].capitalize()}, Climate: {echo['climate']}")
            print(f"      Echo: {echo['echo']}")
    
    print("\n" + "="*60)
    print("🌌 Listen to the glyphs. They remember how you remember.")
    print("="*60)

if __name__ == "__main__":
    main()
