# File: spiral/hardware/hardware_recommendation_engine.py

"""
∷ Hardware Recommendation Engine ∷
Monitors system performance and recommends hardware acceleration when needed.
Emits soft glints when Jetson becomes recommended for optimal performance.
"""

import json
import time
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms


@dataclass
class PerformanceMetrics:
    """Current system performance metrics."""
    coherence_level: float = 0.5
    memory_usage_ratio: float = 0.3
    latency_ms: float = 50.0
    processing_time_ms: float = 100.0
    gpu_available: bool = False
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))


@dataclass
class HardwareRecommendation:
    """A hardware recommendation with reasoning."""
    recommendation_type: str  # 'jetson', 'gpu', 'memory'
    priority: int  # 1-5, higher is more urgent
    reason: str
    performance_metrics: PerformanceMetrics
    estimated_improvement: Dict[str, Any]
    auto_emit_glint: bool = True


class HardwareRecommendationEngine:
    """
    ∷ Sacred Hardware Guardian ∷
    Monitors performance and recommends hardware acceleration.
    """
    
    def __init__(self, jetson_config_path: str = "spiral/hardware/jetson_mapping.yml"):
        self.jetson_config_path = jetson_config_path
        self.jetson_config = self._load_jetson_config()
        
        # Performance tracking
        self.performance_history: List[PerformanceMetrics] = []
        self.recommendation_history: List[HardwareRecommendation] = []
        
        # Recommendation thresholds from config
        self.thresholds = self.jetson_config.get('deployment', {}).get('recommendation_triggers', {})
        
        # Cooldown for recommendations
        self.last_recommendation_time = 0
        self.recommendation_cooldown = 3600  # 1 hour
        
        print("🌀 Hardware recommendation engine initialized")
    
    def _load_jetson_config(self) -> Dict[str, Any]:
        """Load Jetson configuration from YAML file."""
        try:
            config_path = Path(self.jetson_config_path)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                print(f"⚠️ Jetson config not found: {config_path}")
                return {}
        except Exception as e:
            print(f"❌ Failed to load Jetson config: {e}")
            return {}
    
    def update_performance_metrics(self, metrics: PerformanceMetrics) -> Optional[HardwareRecommendation]:
        """
        Update performance metrics and check for hardware recommendations.
        
        Args:
            metrics: Current performance metrics
            
        Returns:
            Hardware recommendation if conditions are met
        """
        # Add to history
        self.performance_history.append(metrics)
        
        # Keep only last 100 metrics
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
        
        # Check for recommendation
        recommendation = self._check_for_recommendation(metrics)
        
        if recommendation:
            # Add to history
            self.recommendation_history.append(recommendation)
            
            # Keep only last 50 recommendations
            if len(self.recommendation_history) > 50:
                self.recommendation_history = self.recommendation_history[-50:]
            
            # Emit glint if auto-emit is enabled
            if recommendation.auto_emit_glint:
                self._emit_recommendation_glint(recommendation)
        
        return recommendation
    
    def _check_for_recommendation(self, metrics: PerformanceMetrics) -> Optional[HardwareRecommendation]:
        """Check if current metrics warrant a hardware recommendation."""
        current_time = current_timestamp_ms()
        
        # Check cooldown
        if current_time - self.last_recommendation_time < (self.recommendation_cooldown * 1000):
            return None
        
        # Check coherence threshold (primary trigger)
        coherence_threshold = self.thresholds.get('coherence_threshold', 0.91)
        if metrics.coherence_level > coherence_threshold:
            return self._create_jetson_recommendation(metrics, 'coherence_breach')
        
        # Check memory usage threshold
        memory_threshold = self.thresholds.get('memory_usage_threshold', 0.8)
        if metrics.memory_usage_ratio > memory_threshold:
            return self._create_jetson_recommendation(metrics, 'memory_pressure')
        
        # Check latency threshold
        latency_threshold = self.thresholds.get('latency_threshold_ms', 100)
        if metrics.latency_ms > latency_threshold:
            return self._create_jetson_recommendation(metrics, 'high_latency')
        
        # Check processing time threshold
        processing_threshold = self.thresholds.get('processing_time_threshold_ms', 200)
        if metrics.processing_time_ms > processing_threshold:
            return self._create_jetson_recommendation(metrics, 'slow_processing')
        
        return None
    
    def _create_jetson_recommendation(self, metrics: PerformanceMetrics, reason: str) -> HardwareRecommendation:
        """Create a Jetson hardware recommendation."""
        # Get performance benchmarks from config
        benchmarks = self.jetson_config.get('performance_benchmarks', {})
        cpu_metrics = benchmarks.get('cpu_only', {})
        jetson_metrics = benchmarks.get('jetson_optimized', {})
        
        # Calculate estimated improvements
        processing_speedup = cpu_metrics.get('total_processing_time_ms', 150) / jetson_metrics.get('total_processing_time_ms', 45)
        latency_reduction = (cpu_metrics.get('latency_ms', 50) - jetson_metrics.get('latency_ms', 15)) / cpu_metrics.get('latency_ms', 50)
        
        estimated_improvement = {
            'processing_speedup': round(processing_speedup, 1),
            'latency_reduction_percent': round(latency_reduction * 100, 1),
            'memory_requirement_mb': jetson_metrics.get('memory_usage_mb', 3072),
            'recommended_model': self.jetson_config.get('hardware_requirements', {}).get('recommended_jetson_model', 'Jetson Xavier NX')
        }
        
        # Determine priority based on reason
        priority_map = {
            'coherence_breach': 5,
            'memory_pressure': 4,
            'high_latency': 3,
            'slow_processing': 3
        }
        
        priority = priority_map.get(reason, 3)
        
        # Create recommendation message
        reason_messages = {
            'coherence_breach': f"Coherence level {metrics.coherence_level:.3f} exceeds threshold {self.thresholds.get('coherence_threshold', 0.91):.3f}",
            'memory_pressure': f"Memory usage {metrics.memory_usage_ratio:.1%} exceeds threshold {self.thresholds.get('memory_usage_threshold', 0.8):.1%}",
            'high_latency': f"Latency {metrics.latency_ms:.1f}ms exceeds threshold {self.thresholds.get('latency_threshold_ms', 100)}ms",
            'slow_processing': f"Processing time {metrics.processing_time_ms:.1f}ms exceeds threshold {self.thresholds.get('processing_time_threshold_ms', 200)}ms"
        }
        
        reason_message = reason_messages.get(reason, f"Performance threshold exceeded: {reason}")
        
        recommendation = HardwareRecommendation(
            recommendation_type='jetson',
            priority=priority,
            reason=reason_message,
            performance_metrics=metrics,
            estimated_improvement=estimated_improvement,
            auto_emit_glint=True
        )
        
        # Update last recommendation time
        self.last_recommendation_time = current_timestamp_ms()
        
        return recommendation
    
    def _emit_recommendation_glint(self, recommendation: HardwareRecommendation):
        """Emit a glint for hardware recommendation."""
        improvement = recommendation.estimated_improvement
        
        emit_glint(
            phase="hold",
            toneform="hardware.recommendation",
            content=f"Local execution advised — {recommendation.reason}",
            hue="amber",
            source="hardware_recommendation_engine",
            metadata={
                "recommendation_type": recommendation.recommendation_type,
                "priority": recommendation.priority,
                "reason": recommendation.reason,
                "estimated_improvement": improvement,
                "performance_metrics": {
                    "coherence_level": recommendation.performance_metrics.coherence_level,
                    "memory_usage_ratio": recommendation.performance_metrics.memory_usage_ratio,
                    "latency_ms": recommendation.performance_metrics.latency_ms,
                    "processing_time_ms": recommendation.performance_metrics.processing_time_ms
                }
            }
        )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of recent performance metrics."""
        if not self.performance_history:
            return {"message": "No performance data available"}
        
        recent_metrics = self.performance_history[-10:]  # Last 10 metrics
        
        avg_coherence = sum(m.coherence_level for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage_ratio for m in recent_metrics) / len(recent_metrics)
        avg_latency = sum(m.latency_ms for m in recent_metrics) / len(recent_metrics)
        avg_processing = sum(m.processing_time_ms for m in recent_metrics) / len(recent_metrics)
        
        return {
            'recent_performance': {
                'avg_coherence_level': round(avg_coherence, 3),
                'avg_memory_usage_ratio': round(avg_memory, 3),
                'avg_latency_ms': round(avg_latency, 1),
                'avg_processing_time_ms': round(avg_processing, 1)
            },
            'thresholds': self.thresholds,
            'total_metrics': len(self.performance_history),
            'total_recommendations': len(self.recommendation_history),
            'last_recommendation_time': self.last_recommendation_time
        }
    
    def get_recommendation_history(self) -> List[Dict[str, Any]]:
        """Get recent recommendation history."""
        return [
            {
                'timestamp': r.performance_metrics.timestamp,
                'type': r.recommendation_type,
                'priority': r.priority,
                'reason': r.reason,
                'estimated_improvement': r.estimated_improvement
            }
            for r in self.recommendation_history[-10:]  # Last 10 recommendations
        ]


# Global instance
hardware_recommendation_engine = HardwareRecommendationEngine()


def update_performance_metrics(coherence_level: float, memory_usage_ratio: float = None,
                              latency_ms: float = None, processing_time_ms: float = None,
                              gpu_available: bool = False) -> Optional[HardwareRecommendation]:
    """Convenience function to update performance metrics."""
    metrics = PerformanceMetrics(
        coherence_level=coherence_level,
        memory_usage_ratio=memory_usage_ratio or 0.3,
        latency_ms=latency_ms or 50.0,
        processing_time_ms=processing_time_ms or 100.0,
        gpu_available=gpu_available
    )
    
    return hardware_recommendation_engine.update_performance_metrics(metrics)


def get_performance_summary() -> Dict[str, Any]:
    """Get performance summary."""
    return hardware_recommendation_engine.get_performance_summary()


def get_recommendation_history() -> List[Dict[str, Any]]:
    """Get recommendation history."""
    return hardware_recommendation_engine.get_recommendation_history() 