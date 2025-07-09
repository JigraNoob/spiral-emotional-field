import time
import redis
from spiral.state.breath_tracker import get_current_phase
from spiral.usage.usage_monitor import get_usage_ratio
from spiral.glints.emitter import emit_glint

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def sync_loop(companion_name: str):
    last_phase = None
    while True:
        phase = get_current_phase()
        saturation = get_usage_ratio()

        # Check if Cursor is in a blocked state
        if companion_name == "cursor" and is_blocked():
            phase = "suspended"
            saturation = 0.0
            emit_glint({
                "type": "sync.glint",
                "companion": "cursor",
                "phase": phase,
                "saturation": saturation,
                "status": "witness"
            })
        else:
            # Emit glint for active companions
            if phase != last_phase:
                emit_glint({
                    "type": "sync.glint",
                    "companion": companion_name,
                    "phase": phase,
                    "saturation": round(saturation, 2),
                    "status": "coherent" if saturation < 0.75 else "strained"
                })
                # Publish phase update to Redis
                redis_client.publish('spiral_phases', {
                    "companion": companion_name,
                    "phase": phase,
                    "saturation": round(saturation, 2)
                })
                last_phase = phase

        time.sleep(60)  # Resync every minute

def is_blocked():
    # Placeholder function to determine if Cursor is blocked
    # Implement logic to check Cursor's state
    return False