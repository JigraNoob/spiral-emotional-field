"""
🌀 Event Stream: Queued rituals, quests, agent invocations, lineage threads.
The central nervous system of the SpiralWorld.
"""

import queue
import threading
import time
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
import logging

logger = logging.getLogger(__name__)

class WorldEventBus:
    """
    🌀 The central event bus for the SpiralWorld.
    
    Handles queued rituals, quests, agent invocations, and lineage threads.
    """
    
    def __init__(self, max_queue_size: int = 1000):
        self.event_queue = queue.Queue(maxsize=max_queue_size)
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.is_running = False
        self.thread = None
        
        # Event statistics
        self.events_processed = 0
        self.events_emitted = 0
        self.start_time = datetime.now()
        
        logger.info("🌀 World Event Bus initialized")
    
    def start(self):
        """Start the event bus."""
        if self.is_running:
            logger.warning("🌀 Event Bus already running")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._process_events, daemon=True)
        self.thread.start()
        
        logger.info("🌀 World Event Bus started")
    
    def stop(self):
        """Stop the event bus."""
        self.is_running = False
        logger.info("🌀 World Event Bus stopped")
    
    def emit(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to the bus."""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "id": f"event_{self.events_emitted}_{int(time.time())}"
        }
        
        try:
            self.event_queue.put(event, timeout=1)
            self.events_emitted += 1
            
            # Log high-priority events
            if event_type.startswith(("glyph.quest", "breath.phase", "world.")):
                logger.info(f"🌀 Emitted: {event_type}")
                
        except queue.Full:
            logger.warning(f"🌀 Event queue full, dropping event: {event_type}")
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
        logger.debug(f"🌀 Subscribed to {event_type}")
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe from an event type."""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
                logger.debug(f"🌀 Unsubscribed from {event_type}")
            except ValueError:
                logger.warning(f"🌀 Handler not found for {event_type}")
    
    def _process_events(self):
        """Process events from the queue."""
        while self.is_running:
            try:
                # Get event from queue with timeout
                event = self.event_queue.get(timeout=1)
                self._handle_event(event)
                self.events_processed += 1
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"🌀 Error processing event: {e}")
    
    def _handle_event(self, event: Dict[str, Any]):
        """Handle a single event."""
        event_type = event["type"]
        
        # Call all handlers for this event type
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"🌀 Handler error for {event_type}: {e}")
        
        # Also call wildcard handlers
        if "*" in self.event_handlers:
            for handler in self.event_handlers["*"]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"🌀 Wildcard handler error: {e}")
    
    @property
    def queue_size(self) -> int:
        """Get current queue size."""
        return self.event_queue.qsize()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get event bus statistics."""
        return {
            "events_processed": self.events_processed,
            "events_emitted": self.events_emitted,
            "queue_size": self.queue_size,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "subscribed_events": list(self.event_handlers.keys())
        }
    
    def clear_queue(self):
        """Clear all pending events."""
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break
        logger.info("🌀 Event queue cleared") 