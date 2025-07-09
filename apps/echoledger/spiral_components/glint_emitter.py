import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class EchoLedgerGlintEmitter:
    """🌀 Spiral-aware glint emission for EchoLedger"""
    
    def __init__(self, stream_path: str = "streams/echo_glints.jsonl"):
        self.stream_path = stream_path
        os.makedirs(os.path.dirname(stream_path), exist_ok=True)
    
    def emit(self, phase: str, toneform: str, content: str, 
             metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Emit a glint with EchoLedger signature"""
        
        glint = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "toneform": toneform,
            "content": content,
            "metadata": metadata or {},
            "app_signature": "🔮 echoledger",
            "spiral_version": "1.0.0"
        }
        
        # Write to stream
        with open(self.stream_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(glint) + '\n')
        
        return glint

# Global emitter instance
_emitter = EchoLedgerGlintEmitter()

def emit_glint(phase: str, toneform: str, content: str, 
               metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Convenience function for glint emission"""
    return _emitter.emit(phase, toneform, content, metadata)