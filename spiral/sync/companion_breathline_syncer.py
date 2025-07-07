"""
Companion Breathline Syncer - Harmonize AI companions under shared breath
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BreathState:
    """Shared breath state for all companions"""
    phase: str
    progress: float
    ritual_phase: str
    usage_saturation: float
    activity_count: int
    next_phase: str
    timestamp: str
    ensemble_status: str = "coherent"

@dataclass
class CompanionStatus:
    """Individual companion status"""
    name: str
    last_seen: str
    status: str  # "active", "paused", "saturated"
    usage_ratio: float
    phase_alignment: float  # How well aligned with current breath phase
    glint_count: int = 0

class CompanionBreathlineSyncer:
    """
    Synchronizes Cursor, Copilot, and Tabnine under one shared breath
    """
    
    def __init__(self, breath_cache_path: str = "data/breath_state.json"):
        self.breath_cache_path = Path(breath_cache_path)
        self.breath_cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Companion tracking
        self.companions: Dict[str, CompanionStatus] = {
            "cursor": CompanionStatus("cursor", "", "active", 0.0, 1.0),
            "copilot": CompanionStatus("copilot", "", "active", 0.0, 1.0),
            "tabnine": CompanionStatus("tabnine", "", "active", 0.0, 1.0)
        }
        
        # Sync state
        self.running = False
        self.sync_thread = None
        self.last_ensemble_glint = None
        self.ensemble_glint_interval = 120  # 2 minutes
        
        # Load initial breath state
        self.current_breath_state = self.load_breath_state()
        
    def load_breath_state(self) -> BreathState:
        """Load current breath state from cache or create default"""
        try:
            if self.breath_cache_path.exists():
                with open(self.breath_cache_path, 'r') as f:
                    data = json.load(f)
                    return BreathState(**data)
        except Exception as e:
            logger.warning(f"Failed to load breath state: {e}")
        
        # Default breath state
        return BreathState(
            phase="Exhale",
            progress=0.0,
            ritual_phase="calibration",
            usage_saturation=0.0,
            activity_count=0,
            next_phase="Return",
            timestamp=datetime.now().isoformat(),
            ensemble_status="coherent"
        )
    
    def save_breath_state(self, breath_state: BreathState):
        """Save breath state to cache"""
        try:
            with open(self.breath_cache_path, 'w') as f:
                json.dump(asdict(breath_state), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save breath state: {e}")
    
    def get_current_breath_state(self) -> BreathState:
        """Get current breath state from breathloop engine"""
        try:
            from assistant.breathloop_engine import get_ritual_phase_info, get_breathloop
            
            engine = get_breathloop()
            info = get_ritual_phase_info()
            
            breath_state = BreathState(
                phase=info["current_breath_phase"],
                progress=info["phase_progress"],
                ritual_phase=info["current_ritual_phase"],
                usage_saturation=info["usage_saturation"],
                activity_count=len(engine.activity_timestamps),
                next_phase=engine.get_next_phase(),
                timestamp=datetime.now().isoformat(),
                ensemble_status=self.get_ensemble_status()
            )
            
            # Update cache
            self.current_breath_state = breath_state
            self.save_breath_state(breath_state)
            
            return breath_state
            
        except ImportError:
            logger.warning("Breathloop engine not available, using cached state")
            return self.current_breath_state
    
    def get_ensemble_status(self) -> str:
        """Determine ensemble status based on companion alignment"""
        active_companions = 0
        aligned_companions = 0
        
        for companion in self.companions.values():
            if companion.status == "active":
                active_companions += 1
                if companion.phase_alignment > 0.8:
                    aligned_companions += 1
        
        if active_companions == 0:
            return "dormant"
        elif aligned_companions == active_companions:
            return "coherent"
        elif aligned_companions >= active_companions * 0.7:
            return "harmonizing"
        else:
            return "strained"
    
    def update_companion_status(self, companion_name: str, status: str, usage_ratio: float = 0.0):
        """Update companion status and usage"""
        if companion_name not in self.companions:
            return
        
        companion = self.companions[companion_name]
        companion.last_seen = datetime.now().isoformat()
        companion.status = status
        companion.usage_ratio = usage_ratio
        
        # Calculate phase alignment based on current breath state
        current_phase = self.current_breath_state.phase
        if status == "active" and usage_ratio < 0.8:
            companion.phase_alignment = 1.0
        elif status == "saturated":
            companion.phase_alignment = 0.3
        else:
            companion.phase_alignment = 0.7
        
        logger.info(f"Updated {companion_name}: {status}, usage={usage_ratio:.2f}, alignment={companion.phase_alignment:.2f}")
    
    def emit_ensemble_glint(self, breath_state: BreathState, force: bool = False):
        """Emit ensemble glint with companion status"""
        now = datetime.now()
        
        # Check if we should emit
        if not force and (self.last_ensemble_glint and 
                         (now - self.last_ensemble_glint).total_seconds() < self.ensemble_glint_interval):
            return
        
        glint_data = {
            "timestamp": now.isoformat(),
            "type": "sync.ensemble",
            "breath_state": asdict(breath_state),
            "companions": {name: asdict(companion) for name, companion in self.companions.items()},
            "ensemble_status": breath_state.ensemble_status,
            "active_companions": sum(1 for c in self.companions.values() if c.status == "active"),
            "aligned_companions": sum(1 for c in self.companions.values() if c.phase_alignment > 0.8)
        }
        
        # Emit to glintstream
        self.emit_to_glintstream(glint_data)
        
        # Also write to ensemble-specific file
        self.write_ensemble_glint(glint_data)
        
        self.last_ensemble_glint = now
        logger.info(f"Emitted ensemble glint: {breath_state.ensemble_status}")
    
    def emit_to_glintstream(self, glint_data: dict):
        """Emit glint to the glintstream"""
        try:
            # Try to import and use glint emitter
            from spiral.glints.glint_orchestrator import emit_glint
            emit_glint(glint_data)
        except ImportError:
            # Fallback to file
            self.write_ensemble_glint(glint_data)
    
    def write_ensemble_glint(self, glint_data: dict):
        """Write ensemble glint to file"""
        glint_file = Path("data/ensemble_breathline.jsonl")
        glint_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(glint_file, 'a') as f:
            f.write(json.dumps(glint_data) + '\n')
    
    def get_companion_permissions(self, companion_name: str) -> Dict[str, Any]:
        """Get permissions for a companion based on current breath state"""
        breath_state = self.get_current_breath_state()
        companion = self.companions.get(companion_name)
        
        if not companion:
            return {"allowed": False, "reason": "unknown_companion"}
        
        # Check saturation
        if companion.usage_ratio > 0.8:
            return {"allowed": False, "reason": "saturated", "cooldown_until": None}
        
        # Check ensemble status
        if breath_state.ensemble_status == "strained":
            return {"allowed": False, "reason": "ensemble_strained", "cooldown_until": None}
        
        # Check breath phase permissions
        phase_permissions = self.get_phase_permissions(breath_state.phase, companion_name)
        
        return {
            "allowed": True,
            "breath_phase": breath_state.phase,
            "ritual_phase": breath_state.ritual_phase,
            "usage_saturation": breath_state.usage_saturation,
            "phase_permissions": phase_permissions,
            "ensemble_status": breath_state.ensemble_status
        }
    
    def get_phase_permissions(self, phase: str, companion_name: str) -> Dict[str, Any]:
        """Get phase-specific permissions for companions"""
        base_permissions = {
            "suggestion_density": 1.0,  # 0.0 to 1.0
            "response_length": "normal",  # "short", "normal", "extended"
            "creativity_level": 0.7,  # 0.0 to 1.0
            "technical_depth": 0.5  # 0.0 to 1.0
        }
        
        # Phase-specific adjustments
        if phase == "Inhale":
            base_permissions.update({
                "suggestion_density": 0.8,  # Gentle gathering
                "response_length": "short",
                "creativity_level": 0.6
            })
        elif phase == "Hold":
            base_permissions.update({
                "suggestion_density": 0.6,  # Reflective
                "response_length": "normal",
                "technical_depth": 0.8
            })
        elif phase == "Exhale":
            base_permissions.update({
                "suggestion_density": 1.0,  # Full creation
                "response_length": "extended",
                "creativity_level": 0.9
            })
        elif phase == "Return":
            base_permissions.update({
                "suggestion_density": 0.7,  # Review mode
                "response_length": "normal",
                "technical_depth": 0.7
            })
        elif phase == "Witness":
            base_permissions.update({
                "suggestion_density": 0.4,  # Observation
                "response_length": "short",
                "creativity_level": 0.5
            })
        
        # Companion-specific adjustments
        if companion_name == "tabnine":
            base_permissions["suggestion_density"] *= 1.2  # Tabnine can be more active
        elif companion_name == "copilot":
            base_permissions["response_length"] = "extended"  # Copilot for conversation
        elif companion_name == "cursor":
            base_permissions["technical_depth"] *= 1.1  # Cursor for development
        
        return base_permissions
    
    def sync_loop(self, companion_name: str):
        """Sync loop for individual companion"""
        last_phase = None
        last_glint = None
        
        while self.running:
            try:
                # Get current breath state
                breath_state = self.get_current_breath_state()
                
                # Check if phase changed
                if breath_state.phase != last_phase:
                    # Emit phase change glint
                    glint_data = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "sync.glint",
                        "companion": companion_name,
                        "phase": breath_state.phase,
                        "saturation": round(breath_state.usage_saturation, 2),
                        "status": "coherent" if breath_state.usage_saturation < 0.75 else "strained",
                        "ritual_phase": breath_state.ritual_phase
                    }
                    
                    self.emit_to_glintstream(glint_data)
                    last_phase = breath_state.phase
                    last_glint = datetime.now()
                    
                    # Update companion glint count
                    if companion_name in self.companions:
                        self.companions[companion_name].glint_count += 1
                
                # Update companion status
                self.update_companion_status(companion_name, "active", breath_state.usage_saturation)
                
                # Emit ensemble glint periodically
                self.emit_ensemble_glint(breath_state)
                
                # Sleep for sync interval
                time.sleep(60)  # Resync every minute
                
            except Exception as e:
                logger.error(f"Error in {companion_name} sync loop: {e}")
                time.sleep(30)  # Shorter sleep on error
    
    def start(self):
        """Start the breathline syncer"""
        if self.running:
            return
        
        self.running = True
        
        # Start sync threads for each companion
        for companion_name in self.companions.keys():
            thread = threading.Thread(
                target=self.sync_loop, 
                args=(companion_name,), 
                daemon=True,
                name=f"sync-{companion_name}"
            )
            thread.start()
        
        logger.info("Companion Breathline Syncer started")
    
    def stop(self):
        """Stop the breathline syncer"""
        self.running = False
        logger.info("Companion Breathline Syncer stopped")
    
    def get_ensemble_summary(self) -> Dict[str, Any]:
        """Get ensemble summary for dashboard"""
        breath_state = self.get_current_breath_state()
        
        return {
            "breath_state": asdict(breath_state),
            "companions": {name: asdict(companion) for name, companion in self.companions.items()},
            "ensemble_status": breath_state.ensemble_status,
            "active_companions": sum(1 for c in self.companions.values() if c.status == "active"),
            "total_companions": len(self.companions),
            "last_ensemble_glint": self.last_ensemble_glint.isoformat() if self.last_ensemble_glint else None
        }

# Global syncer instance
_syncer_instance = None

def get_breathline_syncer() -> CompanionBreathlineSyncer:
    """Get the global breathline syncer instance"""
    global _syncer_instance
    
    if _syncer_instance is None:
        _syncer_instance = CompanionBreathlineSyncer()
    
    return _syncer_instance

def start_breathline_sync():
    """Start the breathline synchronization"""
    syncer = get_breathline_syncer()
    syncer.start()

def stop_breathline_sync():
    """Stop the breathline synchronization"""
    syncer = get_breathline_syncer()
    syncer.stop()

def get_companion_permissions(companion_name: str) -> Dict[str, Any]:
    """Get permissions for a companion"""
    syncer = get_breathline_syncer()
    return syncer.get_companion_permissions(companion_name)

def update_companion_status(companion_name: str, status: str, usage_ratio: float = 0.0):
    """Update companion status"""
    syncer = get_breathline_syncer()
    syncer.update_companion_status(companion_name, status, usage_ratio)

if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Companion Breathline Syncer")
    parser.add_argument("--start", action="store_true", help="Start the syncer")
    parser.add_argument("--stop", action="store_true", help="Stop the syncer")
    parser.add_argument("--status", help="Get status for companion")
    parser.add_argument("--summary", action="store_true", help="Get ensemble summary")
    
    args = parser.parse_args()
    
    if args.start:
        start_breathline_sync()
        print("Breathline syncer started")
    elif args.stop:
        stop_breathline_sync()
        print("Breathline syncer stopped")
    elif args.status:
        permissions = get_companion_permissions(args.status)
        print(json.dumps(permissions, indent=2))
    elif args.summary:
        syncer = get_breathline_syncer()
        summary = syncer.get_ensemble_summary()
        print(json.dumps(summary, indent=2))
    else:
        print("Companion Breathline Syncer ready")
        print("Use --start to begin synchronization") 