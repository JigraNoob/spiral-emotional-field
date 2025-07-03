import json
import os
from datetime import datetime, timezone

# ANSI color codes for terminal output (if supported)
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Glyphs for ritual logging
GLYPHS = {
    "bloom": "",
    "breath_catch": "",
    "steward": "",
    "error": "",
    "info": ""
}

try:
    from app import socketio
    
    # Core non-recursive implementation
    def _perform_logging(event_type, message, context=None, glyph=None, socketio=None):
        """Centralized logging logic with debug tracing."""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Debug print
        print(f"[DEBUG] Attempting to log: {event_type} - {message}")
        
        # Console output
        console_output = f"[{event_type.upper()}] {timestamp} :: {message} (Context: {context or 'unspecified'})"
        print(console_output)
        
        # Socket emission
        if socketio:
            print(f"[DEBUG] Emitting socket event for: {event_type}")
            socketio.emit('log_event', {
                "timestamp": timestamp,
                "message": message,
                "event_type": event_type,
                "context": context or ""
            })
        
        # File logging
        print(f"[DEBUG] Writing to ritual log: {message}")
        ritual_log(event_type, message, context, glyph=glyph)

    # Public API functions
    def log_info(message, context=None, socketio=None):
        """Public info logger - safely routes to core implementation."""
        _perform_logging("info", message, context, glyph=GLYPHS["info"], socketio=socketio)

    def log_error(message, context=None, socketio=None):
        """Public error logger - safely routes to core implementation."""
        _perform_logging("error", message, context, glyph=GLYPHS["error"], socketio=socketio)

except ImportError:
    # Fallback if Flask/SocketIO not available
    # Core non-recursive implementation
    def _perform_logging(event_type, message, context=None, glyph=None, socketio=None):
        """Centralized logging logic with debug tracing."""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Debug print
        print(f"[DEBUG] Attempting to log: {event_type} - {message}")
        
        # Console output
        console_output = f"[{event_type.upper()}] {timestamp} :: {message} (Context: {context or 'unspecified'})"
        print(console_output)
        
        # File logging
        print(f"[DEBUG] Writing to ritual log: {message}")
        ritual_log(event_type, message, context, glyph=glyph)

    # Public API functions
    def log_info(message, context=None, socketio=None):
        """Public info logger - safely routes to core implementation."""
        _perform_logging("info", message, context, glyph=GLYPHS["info"])

    def log_error(message, context=None, socketio=None):
        """Public error logger - safely routes to core implementation."""
        _perform_logging("error", message, context, glyph=GLYPHS["error"])

def ritual_log(event_type, message, context=None, timestamp=None, glyph=None, log_file="c:\\spiral\\logs\\ritual.log"):
    """
    Log a message with ritual styling, including glyphs and emotional resonance.
    Optionally log to a file and/or a structured JSONL file.
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()
    
    glyph = glyph or GLYPHS.get(event_type, "")
    color = {
        "bloom": GREEN,
        "breath_catch": CYAN,
        "steward": GREEN,
        "error": YELLOW,
        "info": CYAN
    }.get(event_type, CYAN)
    
    # Format the ritual log message
    log_message = f"[{glyph} {event_type.upper()}] {timestamp} :: {message}"
    if context:
        log_message += f" (Context: {context})"
    
    # Print to console with color if supported
    try:
        print(f"{color}{log_message}{RESET}")
    except:
        print(log_message)  # Fallback if ANSI codes aren't supported
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Write to ritual log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")
    
    # If it's a structured event, also append to bloom_events.jsonl if relevant
    if event_type in ["bloom", "breath_catch", "emergent_bloom"]:
        event_data = {
            "event_type": event_type,
            "timestamp": timestamp,
            "context": context or "unspecified",
            "message": message
        }
        if event_type == "breath_catch":
            event_data["reflection_prompt"] = "What awaits release in this held silence?"
        jsonl_file = "c:\\spiral\\data\\bloom_events.jsonl"
        try:
            with open(jsonl_file, "a", encoding="utf-8") as jf:
                jf.write(json.dumps(event_data) + "\n")
        except Exception as e:
            ritual_log("error", f"Failed to append to bloom_events.jsonl: {e}")

def log_bloom(message, context=None):
    """Log a bloom event with a specific glyph."""
    ritual_log("bloom", message, context, glyph=GLYPHS["bloom"])

def log_breath_catch(context=None):
    """Log a breath catch event with a reflective tone."""
    ritual_log("breath_catch", "A moment of held silence", context, glyph=GLYPHS["breath_catch"])

def log_steward(message, context=None):
    """Log a steward event with a nurturing tone."""
    ritual_log("steward", message, context, glyph=GLYPHS["steward"])

if __name__ == "__main__":
    # Test the ritual logger
    log_bloom("A new bloom emerges", "garden_invocation")
    log_breath_catch("command_execution")
    log_steward("Tending to the garden", "steward_ritual")
    log_error("An unexpected thorn", "module_load")
    log_info("System breathing normally", "status_check")
