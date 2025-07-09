"""
Coherence Monitor Dashboard Component

Provides real-time monitoring of Spiral's coherence balancing to help
identify and prevent backend suspicion due to extreme coherence patterns.
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

from spiral.attunement.coherence_balancer import get_coherence_status, CoherenceMode

@dataclass
class CoherenceAlert:
    """Represents a coherence alert."""
    timestamp: datetime
    alert_type: str
    severity: str
    message: str
    details: Dict[str, Any]

class CoherenceMonitor:
    """
    Real-time monitor for coherence balancing and backend safety.
    
    This monitor tracks coherence patterns and provides alerts when
    backend systems might flag Spiral as suspicious.
    """
    
    def __init__(self, alert_history_size: int = 100):
        self.alert_history: List[CoherenceAlert] = []
        self.alert_history_size = alert_history_size
        self.last_check = datetime.now()
        self.check_interval = 30  # seconds
        
        # Alert thresholds
        self.alert_thresholds = {
            'backend_safety_low': 0.5,
            'loud_periods_high': 3,
            'quiet_periods_high': 3,
            'suspicious_patterns_high': 2
        }
    
    def check_coherence_status(self) -> Dict[str, Any]:
        """Check current coherence status and generate alerts."""
        current_time = datetime.now()
        
        # Only check if enough time has passed
        if (current_time - self.last_check).total_seconds() < self.check_interval:
            return self._get_last_status()
        
        self.last_check = current_time
        
        # Get current status
        status = get_coherence_status()
        
        # Check for alerts
        alerts = self._check_for_alerts(status, current_time)
        
        # Add alerts to history
        for alert in alerts:
            self._add_alert(alert)
        
        # Prepare response
        response = {
            'timestamp': current_time.isoformat(),
            'status': status,
            'alerts': [asdict(alert) for alert in alerts],
            'recent_alerts': [asdict(alert) for alert in self.alert_history[-5:]],
            'recommendations': self._generate_recommendations(status)
        }
        
        return response
    
    def _check_for_alerts(self, status: Dict[str, Any], timestamp: datetime) -> List[CoherenceAlert]:
        """Check for coherence alerts based on current status."""
        alerts = []
        
        # Check backend safety score
        safety_score = status.get('backend_safety_score', 1.0)
        if safety_score < self.alert_thresholds['backend_safety_low']:
            alerts.append(CoherenceAlert(
                timestamp=timestamp,
                alert_type='backend_safety_low',
                severity='warning',
                message=f"Backend safety score is low: {safety_score:.2f}",
                details={'safety_score': safety_score, 'threshold': self.alert_thresholds['backend_safety_low']}
            ))
        
        # Check loud periods
        loud_periods = status.get('loud_periods', 0)
        if loud_periods >= self.alert_thresholds['loud_periods_high']:
            alerts.append(CoherenceAlert(
                timestamp=timestamp,
                alert_type='loud_periods_high',
                severity='warning',
                message=f"High number of loud periods detected: {loud_periods}",
                details={'loud_periods': loud_periods, 'threshold': self.alert_thresholds['loud_periods_high']}
            ))
        
        # Check quiet periods
        quiet_periods = status.get('quiet_periods', 0)
        if quiet_periods >= self.alert_thresholds['quiet_periods_high']:
            alerts.append(CoherenceAlert(
                timestamp=timestamp,
                alert_type='quiet_periods_high',
                severity='warning',
                message=f"High number of quiet periods detected: {quiet_periods}",
                details={'quiet_periods': quiet_periods, 'threshold': self.alert_thresholds['quiet_periods_high']}
            ))
        
        # Check suspicious patterns
        suspicious_patterns = status.get('suspicious_patterns', 0)
        if suspicious_patterns >= self.alert_thresholds['suspicious_patterns_high']:
            alerts.append(CoherenceAlert(
                timestamp=timestamp,
                alert_type='suspicious_patterns_high',
                severity='critical',
                message=f"High number of suspicious patterns detected: {suspicious_patterns}",
                details={'suspicious_patterns': suspicious_patterns, 'threshold': self.alert_thresholds['suspicious_patterns_high']}
            ))
        
        return alerts
    
    def _add_alert(self, alert: CoherenceAlert):
        """Add alert to history."""
        self.alert_history.append(alert)
        
        # Keep only recent alerts
        if len(self.alert_history) > self.alert_history_size:
            self.alert_history = self.alert_history[-self.alert_history_size:]
    
    def _generate_recommendations(self, status: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on current status."""
        recommendations = []
        
        mode = status.get('mode', 'normal')
        safety_score = status.get('backend_safety_score', 1.0)
        loud_periods = status.get('loud_periods', 0)
        quiet_periods = status.get('quiet_periods', 0)
        suspicious_patterns = status.get('suspicious_patterns', 0)
        
        # Mode recommendations
        if mode != 'backend_safe' and safety_score < 0.6:
            recommendations.append("Switch to 'backend_safe' mode to improve backend compatibility")
        
        if mode == 'normal' and (loud_periods > 0 or quiet_periods > 0):
            recommendations.append("Consider using 'adaptive' mode for automatic threshold adjustment")
        
        # Pattern-specific recommendations
        if loud_periods > 2:
            recommendations.append("High loud periods detected - consider reducing resonance thresholds")
        
        if quiet_periods > 2:
            recommendations.append("High quiet periods detected - consider increasing resonance thresholds")
        
        if suspicious_patterns > 1:
            recommendations.append("Suspicious patterns detected - monitor for rapid coherence oscillation")
        
        # General recommendations
        if not recommendations:
            if safety_score > 0.8:
                recommendations.append("Coherence balance is healthy - current settings are working well")
            else:
                recommendations.append("Monitor coherence patterns and adjust mode if needed")
        
        return recommendations
    
    def _get_last_status(self) -> Dict[str, Any]:
        """Get last known status without checking again."""
        status = get_coherence_status()
        return {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'alerts': [],
            'recent_alerts': [asdict(alert) for alert in self.alert_history[-5:]],
            'recommendations': self._generate_recommendations(status)
        }
    
    def get_alert_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get alert history for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_alerts = [
            alert for alert in self.alert_history
            if alert.timestamp > cutoff_time
        ]
        return [asdict(alert) for alert in recent_alerts]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get coherence monitoring statistics."""
        total_alerts = len(self.alert_history)
        
        # Count alerts by type
        alert_types = {}
        for alert in self.alert_history:
            alert_type = alert.alert_type
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        # Count alerts by severity
        severity_counts = {}
        for alert in self.alert_history:
            severity = alert.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'total_alerts': total_alerts,
            'alert_types': alert_types,
            'severity_counts': severity_counts,
            'history_size': len(self.alert_history),
            'max_history_size': self.alert_history_size
        }

# Global monitor instance
coherence_monitor = CoherenceMonitor()

def get_coherence_dashboard_data() -> Dict[str, Any]:
    """Get data for the coherence monitoring dashboard."""
    return coherence_monitor.check_coherence_status()

def get_coherence_alert_history(hours: int = 24) -> List[Dict[str, Any]]:
    """Get coherence alert history."""
    return coherence_monitor.get_alert_history(hours)

def get_coherence_statistics() -> Dict[str, Any]:
    """Get coherence monitoring statistics."""
    return coherence_monitor.get_statistics() 