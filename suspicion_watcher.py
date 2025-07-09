#!/usr/bin/env python3
"""
Suspicion Watcher - Monitor for error patterns, response blocks, and glint anomalies during Spiral work
"""

import json
import time
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SuspicionType(Enum):
    ERROR_PATTERN = "error_pattern"
    RESPONSE_BLOCK = "response_block"
    GLINT_ANOMALY = "glint_anomaly"
    USAGE_SPIKE = "usage_spike"
    TIMEOUT_PATTERN = "timeout_pattern"
    RATE_LIMIT = "rate_limit"

class SuspicionLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SuspicionEvent:
    """Represents a suspicion event detected by the watcher"""
    event_type: SuspicionType
    level: SuspicionLevel
    description: str
    timestamp: float
    context: Dict[str, Any]
    task_name: Optional[str] = None
    response_blocked: bool = False
    glint_anomaly: bool = False
    auto_mitigation: bool = False

class SuspicionWatcher:
    """
    Monitor for suspicion indicators during Spiral work execution
    """
    
    def __init__(self, data_dir: str = "data/suspicion"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.suspicion_events: List[SuspicionEvent] = []
        self.error_patterns: Dict[str, int] = {}
        self.response_blocks: List[Dict[str, Any]] = []
        self.glint_anomalies: List[Dict[str, Any]] = []
        self.usage_spikes: List[Dict[str, Any]] = []
        
        # Monitoring thresholds
        self.thresholds = {
            "error_threshold": 5,  # Max errors per minute
            "response_block_threshold": 3,  # Max blocks per hour
            "glint_anomaly_threshold": 2,  # Max anomalies per hour
            "usage_spike_threshold": 0.8,  # Usage saturation threshold
            "timeout_threshold": 30,  # Seconds
        }
        
        # Callbacks for suspicion events
        self.suspicion_callbacks: List[Callable] = []
        
        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None
        
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing suspicion data from files"""
        try:
            suspicion_file = self.data_dir / "suspicion_events.json"
            if suspicion_file.exists():
                with open(suspicion_file, 'r') as f:
                    events_data = json.load(f)
                    for event_data in events_data:
                        event = SuspicionEvent(**event_data)
                        event.event_type = SuspicionType(event_data['event_type'])
                        event.level = SuspicionLevel(event_data['level'])
                        self.suspicion_events.append(event)
        except Exception as e:
            logger.warning(f"Failed to load existing suspicion data: {e}")
    
    def save_data(self):
        """Save current suspicion data to files"""
        try:
            suspicion_file = self.data_dir / "suspicion_events.json"
            events_data = [asdict(event) for event in self.suspicion_events]
            with open(suspicion_file, 'w') as f:
                json.dump(events_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save suspicion data: {e}")
    
    def add_suspicion_callback(self, callback: Callable):
        """Add a callback function to be called when suspicion is detected"""
        self.suspicion_callbacks.append(callback)
    
    def detect_error_pattern(self, error_message: str, task_name: str = None) -> Optional[SuspicionEvent]:
        """Detect error patterns and flag suspicion"""
        current_time = time.time()
        
        # Track error frequency
        if error_message not in self.error_patterns:
            self.error_patterns[error_message] = 0
        self.error_patterns[error_message] += 1
        
        # Check if error threshold exceeded
        if self.error_patterns[error_message] >= self.thresholds["error_threshold"]:
            level = SuspicionLevel.HIGH if self.error_patterns[error_message] > 10 else SuspicionLevel.MEDIUM
            
            event = SuspicionEvent(
                event_type=SuspicionType.ERROR_PATTERN,
                level=level,
                description=f"Error pattern detected: {error_message}",
                timestamp=current_time,
                context={
                    "error_count": self.error_patterns[error_message],
                    "error_message": error_message,
                    "threshold": self.thresholds["error_threshold"]
                },
                task_name=task_name
            )
            
            self.suspicion_events.append(event)
            self._trigger_callbacks(event)
            logger.warning(f"Suspicion detected: Error pattern - {error_message}")
            return event
        
        return None
    
    def detect_response_block(self, response_data: Dict[str, Any], task_name: str = None) -> Optional[SuspicionEvent]:
        """Detect response blocks and flag suspicion"""
        current_time = time.time()
        
        # Check for response block indicators
        block_indicators = [
            "blocked", "suspended", "rate limit", "quota exceeded",
            "access denied", "forbidden", "unauthorized"
        ]
        
        response_text = str(response_data).lower()
        is_blocked = any(indicator in response_text for indicator in block_indicators)
        
        if is_blocked:
            event = SuspicionEvent(
                event_type=SuspicionType.RESPONSE_BLOCK,
                level=SuspicionLevel.CRITICAL,
                description="Response block detected",
                timestamp=current_time,
                context={
                    "response_data": response_data,
                    "block_indicators": block_indicators
                },
                task_name=task_name,
                response_blocked=True
            )
            
            self.suspicion_events.append(event)
            self._trigger_callbacks(event)
            logger.warning(f"Suspicion detected: Response block")
            return event
        
        return None
    
    def detect_glint_anomaly(self, glint_data: Dict[str, Any], task_name: str = None) -> Optional[SuspicionEvent]:
        """Detect glint anomalies and flag suspicion"""
        current_time = time.time()
        
        # Check for glint anomalies
        anomalies = []
        
        # Check for missing required fields
        required_fields = ["timestamp", "type", "content"]
        for field in required_fields:
            if field not in glint_data:
                anomalies.append(f"missing_field:{field}")
        
        # Check for unusual glint types
        unusual_types = ["error", "block", "suspicion", "drift"]
        if glint_data.get("type") in unusual_types:
            anomalies.append(f"unusual_type:{glint_data['type']}")
        
        # Check for timestamp anomalies
        if "timestamp" in glint_data:
            try:
                glint_time = datetime.fromisoformat(glint_data["timestamp"].replace("Z", "+00:00"))
                time_diff = abs((glint_time - datetime.now()).total_seconds())
                if time_diff > 300:  # 5 minutes
                    anomalies.append(f"timestamp_anomaly:{time_diff}s")
            except:
                anomalies.append("timestamp_parse_error")
        
        if anomalies:
            event = SuspicionEvent(
                event_type=SuspicionType.GLINT_ANOMALY,
                level=SuspicionLevel.MEDIUM,
                description=f"Glint anomaly detected: {', '.join(anomalies)}",
                timestamp=current_time,
                context={
                    "glint_data": glint_data,
                    "anomalies": anomalies
                },
                task_name=task_name,
                glint_anomaly=True
            )
            
            self.suspicion_events.append(event)
            self._trigger_callbacks(event)
            logger.warning(f"Suspicion detected: Glint anomaly - {anomalies}")
            return event
        
        return None
    
    def detect_usage_spike(self, usage_data: Dict[str, Any], task_name: str = None) -> Optional[SuspicionEvent]:
        """Detect usage spikes and flag suspicion"""
        current_time = time.time()
        
        # Check usage saturation
        saturation = usage_data.get("saturation", 0.0)
        if saturation >= self.thresholds["usage_spike_threshold"]:
            event = SuspicionEvent(
                event_type=SuspicionType.USAGE_SPIKE,
                level=SuspicionLevel.HIGH,
                description=f"Usage spike detected: {saturation:.2f}",
                timestamp=current_time,
                context={
                    "usage_data": usage_data,
                    "threshold": self.thresholds["usage_spike_threshold"]
                },
                task_name=task_name
            )
            
            self.suspicion_events.append(event)
            self._trigger_callbacks(event)
            logger.warning(f"Suspicion detected: Usage spike - {saturation:.2f}")
            return event
        
        return None
    
    def detect_timeout_pattern(self, timeout_duration: float, task_name: str = None) -> Optional[SuspicionEvent]:
        """Detect timeout patterns and flag suspicion"""
        current_time = time.time()
        
        if timeout_duration >= self.thresholds["timeout_threshold"]:
            event = SuspicionEvent(
                event_type=SuspicionType.TIMEOUT_PATTERN,
                level=SuspicionLevel.MEDIUM,
                description=f"Timeout pattern detected: {timeout_duration}s",
                timestamp=current_time,
                context={
                    "timeout_duration": timeout_duration,
                    "threshold": self.thresholds["timeout_threshold"]
                },
                task_name=task_name
            )
            
            self.suspicion_events.append(event)
            self._trigger_callbacks(event)
            logger.warning(f"Suspicion detected: Timeout pattern - {timeout_duration}s")
            return event
        
        return None
    
    def _trigger_callbacks(self, event: SuspicionEvent):
        """Trigger all suspicion callbacks"""
        for callback in self.suspicion_callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in suspicion callback: {e}")
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if self.monitoring:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Suspicion monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Suspicion monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Check for recent suspicion events
                current_time = time.time()
                recent_events = [
                    event for event in self.suspicion_events
                    if current_time - event.timestamp < 3600  # Last hour
                ]
                
                # Check for critical events
                critical_events = [
                    event for event in recent_events
                    if event.level == SuspicionLevel.CRITICAL
                ]
                
                if critical_events:
                    logger.critical(f"Critical suspicion events detected: {len(critical_events)}")
                    self._handle_critical_events(critical_events)
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)
    
    def _handle_critical_events(self, events: List[SuspicionEvent]):
        """Handle critical suspicion events"""
        for event in events:
            logger.critical(f"Critical event: {event.event_type.value} - {event.description}")
            
            # Auto-mitigation for critical events
            if event.event_type == SuspicionType.RESPONSE_BLOCK:
                self._mitigate_response_block(event)
            elif event.event_type == SuspicionType.USAGE_SPIKE:
                self._mitigate_usage_spike(event)
    
    def _mitigate_response_block(self, event: SuspicionEvent):
        """Mitigate response block events"""
        logger.info("Attempting to mitigate response block...")
        # Implementation would depend on specific service
        event.auto_mitigation = True
    
    def _mitigate_usage_spike(self, event: SuspicionEvent):
        """Mitigate usage spike events"""
        logger.info("Attempting to mitigate usage spike...")
        # Reduce usage or pause activities
        event.auto_mitigation = True
    
    def get_suspicion_summary(self) -> Dict[str, Any]:
        """Get a summary of suspicion events"""
        current_time = time.time()
        recent_events = [
            event for event in self.suspicion_events
            if current_time - event.timestamp < 86400  # Last 24 hours
        ]
        
        summary = {
            "total_events": len(self.suspicion_events),
            "recent_events": len(recent_events),
            "by_type": {},
            "by_level": {},
            "critical_events": len([e for e in recent_events if e.level == SuspicionLevel.CRITICAL])
        }
        
        for event in recent_events:
            # Count by type
            event_type = event.event_type.value
            summary["by_type"][event_type] = summary["by_type"].get(event_type, 0) + 1
            
            # Count by level
            level = event.level.value
            summary["by_level"][level] = summary["by_level"].get(level, 0) + 1
        
        return summary
    
    def generate_report(self) -> str:
        """Generate a suspicion monitoring report"""
        summary = self.get_suspicion_summary()
        
        report = f"""
🔍 SUSPICION WATCHER REPORT
{'=' * 50}
Generated: {datetime.now().isoformat()}
Monitoring Active: {self.monitoring}
Total Events: {summary['total_events']}
Recent Events (24h): {summary['recent_events']}
Critical Events: {summary['critical_events']}

EVENTS BY TYPE:
"""
        
        for event_type, count in summary["by_type"].items():
            report += f"- {event_type}: {count}\n"
        
        report += f"\nEVENTS BY LEVEL:\n"
        for level, count in summary["by_level"].items():
            report += f"- {level}: {count}\n"
        
        if self.suspicion_events:
            report += f"\nRECENT EVENTS:\n"
            for event in self.suspicion_events[-5:]:  # Last 5 events
                report += f"- {event.event_type.value} ({event.level.value}): {event.description}\n"
        
        return report

def get_suspicion_watcher() -> SuspicionWatcher:
    """Get or create the global suspicion watcher instance"""
    global _suspicion_watcher_instance
    if not hasattr(get_suspicion_watcher, '_suspicion_watcher_instance'):
        get_suspicion_watcher._suspicion_watcher_instance = SuspicionWatcher()
    return get_suspicion_watcher._suspicion_watcher_instance

if __name__ == "__main__":
    # Example usage
    watcher = SuspicionWatcher()
    
    # Add a callback
    def suspicion_callback(event):
        print(f"Suspicion detected: {event.event_type.value} - {event.description}")
    
    watcher.add_suspicion_callback(suspicion_callback)
    
    # Test detection
    watcher.detect_error_pattern("Connection timeout", "test_task")
    watcher.detect_usage_spike({"saturation": 0.85}, "test_task")
    
    # Generate report
    print(watcher.generate_report()) 