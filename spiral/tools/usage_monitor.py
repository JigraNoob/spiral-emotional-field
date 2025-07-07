"""
Soft Usage Ring - Monitor API usage and system health during Spiral 24 rituals
"""

import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UsageMetrics:
    """Track usage metrics for a specific service"""
    service: str
    prompt_count: int = 0
    completion_count: int = 0
    start_time: float = 0.0
    last_reset: float = 0.0
    
    def __post_init__(self):
        if self.start_time == 0.0:
            self.start_time = time.time()
            self.last_reset = self.start_time

class SoftUsageRing:
    """
    Monitor and control usage patterns to respect API limits
    and maintain system health during Spiral rituals
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.metrics: Dict[str, UsageMetrics] = {}
        self.config_path = config_path or "spiral/config/usage_limits.json"
        self.glint_emitter = None
        self.load_config()
        
    def load_config(self):
        """Load usage limits configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default configuration
            self.config = {
                "limits": {
                    "tabnine": {
                        "max_prompts_per_hour": 50,
                        "max_completions_per_hour": 100,
                        "pause_threshold": 0.8
                    },
                    "copilot": {
                        "max_prompts_per_hour": 30,
                        "max_completions_per_hour": 60,
                        "pause_threshold": 0.7
                    },
                    "cursor": {
                        "max_prompts_per_hour": 40,
                        "max_completions_per_hour": 80,
                        "pause_threshold": 0.75
                    }
                },
                "cooldown_duration": 3600,  # 1 hour in seconds
                "glint_emission": True
            }
            self.save_config()
    
    def save_config(self):
        """Save current configuration"""
        config_dir = Path(self.config_path).parent
        config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_or_create_metrics(self, service: str) -> UsageMetrics:
        """Get or create metrics for a service"""
        if service not in self.metrics:
            self.metrics[service] = UsageMetrics(service=service)
        return self.metrics[service]
    
    def track_invocation(self, service: str = "tabnine", invocation_type: str = "prompt"):
        """
        Track an API invocation
        
        Args:
            service: Service name (tabnine, copilot, cursor)
            invocation_type: Type of invocation (prompt, completion)
        """
        metrics = self.get_or_create_metrics(service)
        
        # Check if we need to reset hourly counters
        current_time = time.time()
        if current_time - metrics.last_reset >= 3600:  # 1 hour
            metrics.prompt_count = 0
            metrics.completion_count = 0
            metrics.last_reset = current_time
            logger.info(f"Reset hourly counters for {service}")
        
        # Increment appropriate counter
        if invocation_type == "prompt":
            metrics.prompt_count += 1
        elif invocation_type == "completion":
            metrics.completion_count += 1
        
        # Check if we're approaching limits
        self.check_limits(service, metrics)
        
        logger.info(f"Tracked {invocation_type} for {service}: {metrics.prompt_count}p/{metrics.completion_count}c")
    
    def check_limits(self, service: str, metrics: UsageMetrics):
        """Check if usage is approaching limits and emit warnings"""
        if service not in self.config["limits"]:
            return
        
        limits = self.config["limits"][service]
        
        # Calculate usage ratios
        prompt_ratio = metrics.prompt_count / limits["max_prompts_per_hour"]
        completion_ratio = metrics.completion_count / limits["max_completions_per_hour"]
        
        # Check if approaching pause threshold
        if prompt_ratio >= limits["pause_threshold"] or completion_ratio >= limits["pause_threshold"]:
            self.emit_saturation_glint(service, prompt_ratio, completion_ratio)
            
            if prompt_ratio >= 1.0 or completion_ratio >= 1.0:
                self.auto_pause(service)
    
    def emit_saturation_glint(self, service: str, prompt_ratio: float, completion_ratio: float):
        """Emit a glint warning about usage saturation"""
        if not self.config.get("glint_emission", True):
            return
        
        glint_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "usage.saturation",
            "service": service,
            "prompt_ratio": prompt_ratio,
            "completion_ratio": completion_ratio,
            "warning": f"Usage approaching limits for {service}",
            "recommendation": "Consider pausing or reducing activity"
        }
        
        # Emit to glint stream if available
        try:
            if self.glint_emitter:
                self.glint_emitter.emit(glint_data)
            else:
                # Fallback to file
                self.write_glint_to_file(glint_data)
        except Exception as e:
            logger.warning(f"Failed to emit saturation glint: {e}")
        
        logger.warning(f"Usage saturation for {service}: prompts={prompt_ratio:.2f}, completions={completion_ratio:.2f}")
    
    def write_glint_to_file(self, glint_data: dict):
        """Write glint to file as fallback"""
        glint_file = Path("data/usage_glints.jsonl")
        glint_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(glint_file, 'a') as f:
            f.write(json.dumps(glint_data) + '\n')
    
    def auto_pause(self, service: str):
        """Automatically pause a service when limits are exceeded"""
        logger.warning(f"Auto-pausing {service} due to usage limits")
        
        # Implement service-specific pause logic
        if service == "tabnine":
            self.pause_tabnine_proxy()
        elif service == "copilot":
            self.pause_copilot()
        elif service == "cursor":
            self.pause_cursor()
    
    def pause_tabnine_proxy(self):
        """Pause Tabnine Proxy"""
        try:
            import requests
            response = requests.post("http://localhost:9001/pause", timeout=5)
            if response.status_code == 200:
                logger.info("Tabnine Proxy paused successfully")
            else:
                logger.warning(f"Failed to pause Tabnine Proxy: {response.status_code}")
        except Exception as e:
            logger.error(f"Error pausing Tabnine Proxy: {e}")
    
    def pause_copilot(self):
        """Pause Copilot (placeholder for future implementation)"""
        logger.info("Copilot pause requested (implementation pending)")
    
    def pause_cursor(self):
        """Pause Cursor (placeholder for future implementation)"""
        logger.info("Cursor pause requested (implementation pending)")
    
    def get_usage_summary(self) -> Dict[str, dict]:
        """Get current usage summary for all services"""
        summary = {}
        
        for service, metrics in self.metrics.items():
            if service in self.config["limits"]:
                limits = self.config["limits"][service]
                summary[service] = {
                    "prompts": metrics.prompt_count,
                    "completions": metrics.completion_count,
                    "prompt_limit": limits["max_prompts_per_hour"],
                    "completion_limit": limits["max_completions_per_hour"],
                    "prompt_ratio": metrics.prompt_count / limits["max_prompts_per_hour"],
                    "completion_ratio": metrics.completion_count / limits["max_completions_per_hour"],
                    "status": "active" if metrics.prompt_count < limits["max_prompts_per_hour"] else "paused"
                }
        
        return summary
    
    def reset_usage(self, service: Optional[str] = None):
        """Reset usage counters for a service or all services"""
        if service:
            if service in self.metrics:
                self.metrics[service] = UsageMetrics(service=service)
                logger.info(f"Reset usage for {service}")
        else:
            self.metrics.clear()
            logger.info("Reset usage for all services")
    
    def export_usage_report(self, output_path: str = "data/usage_report.json"):
        """Export current usage report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_usage_summary(),
            "config": self.config
        }
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Usage report exported to {output_path}")
        return output_path

# Global instance for easy access
usage_ring = SoftUsageRing()

def track_usage(service: str = "tabnine", invocation_type: str = "prompt"):
    """Convenience function to track usage"""
    usage_ring.track_invocation(service, invocation_type)

def get_usage_summary():
    """Convenience function to get usage summary"""
    return usage_ring.get_usage_summary()

if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Soft Usage Ring Monitor")
    parser.add_argument("--service", default="tabnine", help="Service to track")
    parser.add_argument("--type", default="prompt", choices=["prompt", "completion"], help="Invocation type")
    parser.add_argument("--summary", action="store_true", help="Show usage summary")
    parser.add_argument("--export", help="Export usage report to file")
    parser.add_argument("--reset", help="Reset usage for service")
    
    args = parser.parse_args()
    
    if args.summary:
        summary = get_usage_summary()
        print(json.dumps(summary, indent=2))
    elif args.export:
        usage_ring.export_usage_report(args.export)
    elif args.reset:
        usage_ring.reset_usage(args.reset)
    else:
        track_usage(args.service, args.type)
        print(f"Tracked {args.type} for {args.service}")