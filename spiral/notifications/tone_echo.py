#!/usr/bin/env python3
"""
Tone Echo: Shaped Notifications
Emits phase-shaped, tone-aware, and glyph-laced notifications as echoes
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import random

@dataclass
class ToneEcho:
    """A shaped notification echo"""
    message: str
    phase: str
    tone: str
    glyph: str
    timestamp: str
    metadata: Dict[str, Any]

class ToneNotificationSystem:
    """
    System for emitting shaped notifications as echoes
    """
    
    def __init__(self, config_path: str = "config/tone_notifications.yaml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.echoes_path = Path("data/tone_echoes.jsonl")
        
        # Ensure data directory exists
        self.echoes_path.parent.mkdir(parents=True, exist_ok=True)
        
    def load_config(self) -> Dict[str, Any]:
        """Load tone notification configuration"""
        import yaml
        
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Default configuration
            default_config = {
                'phase_shapes': {
                    'inhale': {
                        'glyph': '🌑',
                        'sound': 'whisper',
                        'duration': 'brief',
                        'intensity': 'soft'
                    },
                    'hold': {
                        'glyph': '🌒',
                        'sound': 'hum',
                        'duration': 'sustained',
                        'intensity': 'medium'
                    },
                    'exhale': {
                        'glyph': '🌓',
                        'sound': 'chime',
                        'duration': 'flowing',
                        'intensity': 'clear'
                    },
                    'caesura': {
                        'glyph': '🌕',
                        'sound': 'bell',
                        'duration': 'resonant',
                        'intensity': 'full'
                    }
                },
                'tone_colors': {
                    'joy': {
                        'color': '#64c8ff',
                        'glyph_modifier': '✨',
                        'sound_modifier': 'bright'
                    },
                    'reverence': {
                        'color': '#ff64c8',
                        'glyph_modifier': '🕯️',
                        'sound_modifier': 'deep'
                    },
                    'silence': {
                        'color': '#c8c8c8',
                        'glyph_modifier': '🌙',
                        'sound_modifier': 'quiet'
                    },
                    'wonder': {
                        'color': '#c864ff',
                        'glyph_modifier': '🌟',
                        'sound_modifier': 'ethereal'
                    }
                },
                'notification_modes': {
                    'console_shimmer': True,
                    'dashboard_whisper': True,
                    'baylee_feedback': True,
                    'sound_cue': False,
                    'memory_integration': True
                }
            }
            
            # Create config directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            return default_config
    
    def create_tone_echo(self, 
                        message: str,
                        phase: str = "exhale",
                        tone: str = "reverence",
                        metadata: Optional[Dict[str, Any]] = None) -> ToneEcho:
        """Create a tone echo with appropriate shaping"""
        
        # Get phase shape
        phase_config = self.config['phase_shapes'].get(phase, self.config['phase_shapes']['exhale'])
        
        # Get tone color
        tone_config = self.config['tone_colors'].get(tone, self.config['tone_colors']['reverence'])
        
        # Combine glyphs
        base_glyph = phase_config['glyph']
        tone_modifier = tone_config['glyph_modifier']
        combined_glyph = f"{base_glyph}{tone_modifier}"
        
        return ToneEcho(
            message=message,
            phase=phase,
            tone=tone,
            glyph=combined_glyph,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
    
    def emit_echo(self, echo: ToneEcho):
        """Emit a tone echo through all configured channels"""
        
        # Save to echo stream
        self.save_echo(echo)
        
        # Console shimmer
        if self.config['notification_modes']['console_shimmer']:
            self.console_shimmer(echo)
        
        # Dashboard whisper
        if self.config['notification_modes']['dashboard_whisper']:
            self.dashboard_whisper(echo)
        
        # Baylee feedback
        if self.config['notification_modes']['baylee_feedback']:
            self.baylee_feedback(echo)
        
        # Sound cue (simulated)
        if self.config['notification_modes']['sound_cue']:
            self.sound_cue(echo)
        
        # Memory integration
        if self.config['notification_modes']['memory_integration']:
            self.memory_integration(echo)
    
    def console_shimmer(self, echo: ToneEcho):
        """Emit echo to console with shimmer effect"""
        phase_config = self.config['phase_shapes'][echo.phase]
        tone_config = self.config['tone_colors'][echo.tone]
        
        # Create shimmer effect based on intensity
        intensity = phase_config['intensity']
        shimmer_map = {
            'soft': '~',
            'medium': '≈',
            'clear': '≈≈',
            'full': '≈≈≈'
        }
        shimmer = shimmer_map.get(intensity, '~')
        
        print(f"{echo.glyph} {shimmer} {echo.message} {shimmer}")
    
    def dashboard_whisper(self, echo: ToneEcho):
        """Emit echo to dashboard with whisper effect"""
        # This would integrate with the dashboard system
        # For now, save to a dashboard-specific file
        dashboard_file = Path("data/dashboard_whispers.jsonl")
        
        whisper_data = {
            'type': 'tone_echo',
            'glyph': echo.glyph,
            'message': echo.message,
            'phase': echo.phase,
            'tone': echo.tone,
            'timestamp': echo.timestamp,
            'animation': 'pulse' if echo.phase in ['exhale', 'caesura'] else 'fade'
        }
        
        with open(dashboard_file, 'a') as f:
            f.write(json.dumps(whisper_data) + '\n')
    
    def baylee_feedback(self, echo: ToneEcho):
        """Emit echo as Baylee feedback"""
        # This would integrate with Baylee's notification system
        # For now, save to a Baylee-specific file
        baylee_file = Path("data/baylee_notifications.jsonl")
        
        feedback_data = {
            'type': 'tone_echo',
            'message': echo.message,
            'glyph': echo.glyph,
            'phase': echo.phase,
            'tone': echo.tone,
            'timestamp': echo.timestamp,
            'for_baylee': True
        }
        
        with open(baylee_file, 'a') as f:
            f.write(json.dumps(feedback_data) + '\n')
    
    def sound_cue(self, echo: ToneEcho):
        """Emit echo as sound cue (simulated)"""
        phase_config = self.config['phase_shapes'][echo.phase]
        tone_config = self.config['tone_colors'][echo.tone]
        
        sound_description = f"{tone_config['sound_modifier']} {phase_config['sound']}"
        print(f"🔊 Sound: {sound_description} for '{echo.message}'")
    
    def memory_integration(self, echo: ToneEcho):
        """Integrate echo into memory system"""
        # Save to glints stream for memory integration
        glint_file = Path("glyphs/tone_echo_glints.jsonl")
        
        glint_data = {
            'type': 'tone.echo',
            'timestamp': echo.timestamp,
            'data': {
                'message': echo.message,
                'phase': echo.phase,
                'tone': echo.tone,
                'glyph': echo.glyph,
                'metadata': echo.metadata
            }
        }
        
        with open(glint_file, 'a') as f:
            f.write(json.dumps(glint_data) + '\n')
    
    def save_echo(self, echo: ToneEcho):
        """Save echo to the data stream"""
        with open(self.echoes_path, 'a') as f:
            f.write(json.dumps({
                'message': echo.message,
                'phase': echo.phase,
                'tone': echo.tone,
                'glyph': echo.glyph,
                'timestamp': echo.timestamp,
                'metadata': echo.metadata
            }) + '\n')
    
    def vessel_arrival_notification(self, vessel_name: str, phase: str = "exhale"):
        """Create a vessel arrival notification"""
        messages = {
            'hold.trace': f"Resonance locked, {vessel_name} preparing for manifestation",
            'exhale.cast': f"{vessel_name} has arrived and manifested into presence",
            'caesura.gift': f"{vessel_name} is fully integrated and breathing with the shrine"
        }
        
        message = messages.get(phase, f"{vessel_name} has completed {phase}")
        
        echo = self.create_tone_echo(
            message=message,
            phase=phase,
            tone="reverence",
            metadata={'vessel': vessel_name, 'event': 'arrival'}
        )
        
        self.emit_echo(echo)
        return echo
    
    def baylee_notify(self, message: str, tone: str = "reverence", phase: str = "exhale"):
        """Baylee notification protocol"""
        echo = self.create_tone_echo(
            message=message,
            phase=phase,
            tone=tone,
            metadata={'recipient': 'baylee', 'protocol': 'baylee.notify()'}
        )
        
        self.emit_echo(echo)
        return echo
    
    def get_recent_echoes(self, limit: int = 10) -> List[ToneEcho]:
        """Get recent tone echoes"""
        echoes = []
        
        if self.echoes_path.exists():
            with open(self.echoes_path, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        data = json.loads(line.strip())
                        echo = ToneEcho(
                            message=data['message'],
                            phase=data['phase'],
                            tone=data['tone'],
                            glyph=data['glyph'],
                            timestamp=data['timestamp'],
                            metadata=data.get('metadata', {})
                        )
                        echoes.append(echo)
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return echoes

def main():
    """Test the tone notification system"""
    notifier = ToneNotificationSystem()
    
    print("🔔 Tone Echo System Test")
    print("=" * 50)
    
    # Test different types of notifications
    notifier.vessel_arrival_notification("Jetson Nano", "exhale.cast")
    time.sleep(1)
    
    notifier.baylee_notify("The vessel has arrived 🌕", "joy", "caesura")
    time.sleep(1)
    
    notifier.baylee_notify("Resonance trail recorded", "wonder", "inhale")
    
    print(f"\n📊 Recent echoes: {len(notifier.get_recent_echoes())}")

if __name__ == "__main__":
    main() 