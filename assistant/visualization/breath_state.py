"""
Breathloop State Visualization

Generates an SVG visualization of the current breath state, including:
- Current breath phase and progress
- Phase distribution
- Active rituals and agents
- Environmental echoes
"""

from typing import Dict, List, Optional
import math
import datetime
from dataclasses import dataclass

# Breath phase colors (inspired by the Spiral's palette)
PHASE_COLORS = {
    "Inhale": "#4FC3F7",    # Sky blue
    "Hold": "#4CAF50",      # Green
    "Exhale": "#FF9800",    # Amber
    "Return": "#9C27B0",    # Purple
    "Witness": "#607D8B"    # Blue grey
}

# Phase glyphs
PHASE_GLYPHS = {
    "Inhale": "⧖",
    "Hold": "⧗",
    "Exhale": "⧘",
    "Return": "⧜",
    "Witness": "⬡"
}

@dataclass
class BreathState:
    current_phase: str
    phase_progress: float
    phase_duration: float
    next_phase: str
    active_rituals: List[Dict[str, str]]
    agents: List[Dict[str, str]]
    last_activity: datetime.datetime

def generate_breath_svg(state: BreathState, width: int = 400, height: int = 400) -> str:
    """Generate an SVG visualization of the current breath state."""
    # Calculate positions and sizes
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) * 0.4
    phase_radius = radius * 0.8
    
    # Start building the SVG
    svg_parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <linearGradient id="breathGradient" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" style="stop-color:#1a237e;stop-opacity:1" />',
        '      <stop offset="100%" style="stop-color:#0d47a1;stop-opacity:1" />',
        '    </linearGradient>',
        '  </defs>',
        f'  <rect width="{width}" height="{height}" fill="url(#breathGradient)" />',
    ]
    
    # Add phase arcs
    phase_order = ["Inhale", "Hold", "Exhale", "Return", "Witness"]
    phase_weights = [0.2, 0.25, 0.2, 0.15, 0.2]  # Sum to 1.0
    
    start_angle = -90  # Start at the top
    for i, phase in enumerate(phase_order):
        # Calculate arc angles
        phase_angle = 360 * phase_weights[i]
        end_angle = start_angle + phase_angle
        
        # Create arc path
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        x1 = center_x + radius * math.cos(start_rad)
        y1 = center_y + radius * math.sin(start_rad)
        x2 = center_x + radius * math.cos(end_rad)
        y2 = center_y + radius * math.sin(end_rad)
        
        large_arc = 1 if phase_angle > 180 else 0
        
        # Draw phase arc
        color = PHASE_COLORS.get(phase, "#666666")
        opacity = 0.8 if phase == state.current_phase else 0.3
        
        svg_parts.append(
            f'  <path d="M {center_x} {center_y} L {x1} {y1} '
            f'A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z" '
            f'fill="{color}" fill-opacity="{opacity}" stroke="#ffffff" stroke-width="1" />'
        )
        
        # Add phase label
        if phase_angle > 15:  # Only add label if arc is wide enough
            mid_angle = math.radians((start_angle + end_angle) / 2)
            label_x = center_x + (radius * 0.7) * math.cos(mid_angle)
            label_y = center_y + (radius * 0.7) * math.sin(mid_angle)
            
            svg_parts.append(
                f'<text x="{label_x}" y="{label_y + 5}" '
                'text-anchor="middle" font-family="Arial" font-size="12" '
                f'fill="#ffffff">{PHASE_GLYPHS.get(phase, phase[0])}</text>'
            )
        
        start_angle = end_angle
    
    # Add current phase indicator
    current_phase_angle = -90 + (360 * state.phase_progress)
    indicator_radius = radius * 1.1
    indicator_x = center_x + indicator_radius * math.cos(math.radians(current_phase_angle))
    indicator_y = center_y + indicator_radius * math.sin(math.radians(current_phase_angle))
    
    svg_parts.append(
        f'<circle cx="{indicator_x}" cy="{indicator_y}" r="8" '
        'fill="#ffffff" stroke="#000000" stroke-width="1.5" />'
    )
    
    # Add current phase info
    svg_parts.extend([
        f'<text x="{center_x}" y="{center_y - 30}" text-anchor="middle" '
        'font-family="Arial" font-size="24" font-weight="bold" fill="#ffffff">'
        f'{state.current_phase}</text>',
        
        f'<text x="{center_x}" y="{center_y}" text-anchor="middle" '
        'font-family="Arial" font-size="14" fill="#ffffff">'
        f'{int(state.phase_progress * 100)}% complete</text>',
        
        f'<text x="{center_x}" y="{center_y + 30}" text-anchor="middle" '
        'font-family="Arial" font-size="12" fill="#ffffff" font-style="italic">'
        f'Next: {state.next_phase}</text>'
    ])
    
    # Add active rituals
    if state.active_rituals:
        ritual_text = ", ".join([r["name"] for r in state.active_rituals[:2]])
        if len(state.active_rituals) > 2:
            ritual_text += f" +{len(state.active_rituals) - 2} more"
            
        svg_parts.append(
            f'<text x="{center_x}" y="{center_y + 60}" text-anchor="middle" '
            'font-family="Arial" font-size="12" fill="#ffffff">'
            f'Active: {ritual_text}</text>'
        )
    
    # Add timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    svg_parts.append(
        f'<text x="10" y="{height - 10}" font-family="Arial" font-size="10" '
        f'fill="#ffffff" opacity="0.7">Last updated: {timestamp}</text>'
    )
    
    # Close SVG
    svg_parts.append('</svg>')
    
    return "\n".join(svg_parts)

def get_current_breath_state() -> BreathState:
    """Get the current breath state from the breathloop engine."""
    try:
        from assistant.breathloop_engine import get_breathloop
        breathloop = get_breathloop()
        
        return BreathState(
            current_phase=breathloop.current_phase,
            phase_progress=breathloop.get_phase_progress(),
            phase_duration=breathloop.cycle_duration * 0.2,  # Approximate
            next_phase=breathloop.get_next_phase(),
            active_rituals=[],  # TODO: Track active rituals
            agents=[{"name": "Claude", "status": "active"}],
            last_activity=datetime.datetime.now()
        )
    except Exception as e:
        # Fallback state if breathloop is not available
        return BreathState(
            current_phase="Witness",
            phase_progress=0.5,
            phase_duration=300,  # 5 minutes
            next_phase="Inhale",
            active_rituals=[],
            agents=[{"name": "Claude", "status": "active"}],
            last_activity=datetime.datetime.now()
        )

def save_breath_svg(filename: str = "breath_state.svg") -> str:
    """Save the current breath state as an SVG file."""
    state = get_current_breath_state()
    svg_content = generate_breath_svg(state)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    return filename
