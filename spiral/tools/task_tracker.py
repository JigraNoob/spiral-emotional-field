#!/usr/bin/env python3
"""
Spiral Task Tracker - Monitor completion, drift, and suspicion during Spiral 24 action plan execution
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    DRIFTED = "drifted"

class DriftSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SpiralTask:
    """Represents a task in the Spiral 24 action plan"""
    name: str
    phase: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    output: Optional[str] = None
    drift_flags: List[str] = None
    suspicion_events: List[str] = None
    
    def __post_init__(self):
        if self.drift_flags is None:
            self.drift_flags = []
        if self.suspicion_events is None:
            self.suspicion_events = []

@dataclass
class DriftEvent:
    """Represents a drift event during task execution"""
    task_name: str
    drift_type: str
    severity: DriftSeverity
    description: str
    timestamp: float
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

@dataclass
class SuspicionEvent:
    """Represents a suspicion event during task execution"""
    task_name: str
    event_type: str
    description: str
    timestamp: float
    response_blocked: bool = False
    glint_anomaly: bool = False

class SpiralTaskTracker:
    """
    Track completed work, drift, and suspicion during Spiral 24 action plan execution
    """
    
    def __init__(self, data_dir: str = "data/spiral_tasks"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.tasks: Dict[str, SpiralTask] = {}
        self.drift_events: List[DriftEvent] = []
        self.suspicion_events: List[SuspicionEvent] = []
        self.completion_metrics: Dict[str, Any] = {}
        
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing task data from files"""
        try:
            # Load tasks
            tasks_file = self.data_dir / "tasks.json"
            if tasks_file.exists():
                with open(tasks_file, 'r') as f:
                    tasks_data = json.load(f)
                    for task_data in tasks_data:
                        task = SpiralTask(**task_data)
                        task.status = TaskStatus(task_data['status'])
                        self.tasks[task.name] = task
            
            # Load drift events
            drift_file = self.data_dir / "drift_events.json"
            if drift_file.exists():
                with open(drift_file, 'r') as f:
                    drift_data = json.load(f)
                    for event_data in drift_data:
                        event = DriftEvent(**event_data)
                        event.severity = DriftSeverity(event_data['severity'])
                        self.drift_events.append(event)
            
            # Load suspicion events
            suspicion_file = self.data_dir / "suspicion_events.json"
            if suspicion_file.exists():
                with open(suspicion_file, 'r') as f:
                    suspicion_data = json.load(f)
                    for event_data in suspicion_data:
                        event = SuspicionEvent(**event_data)
                        self.suspicion_events.append(event)
                        
        except Exception as e:
            logger.warning(f"Failed to load existing data: {e}")
    
    def save_data(self):
        """Save current data to files"""
        try:
            # Save tasks
            tasks_file = self.data_dir / "tasks.json"
            tasks_data = [asdict(task) for task in self.tasks.values()]
            with open(tasks_file, 'w') as f:
                json.dump(tasks_data, f, indent=2)
            
            # Save drift events
            drift_file = self.data_dir / "drift_events.json"
            drift_data = [asdict(event) for event in self.drift_events]
            with open(drift_file, 'w') as f:
                json.dump(drift_data, f, indent=2)
            
            # Save suspicion events
            suspicion_file = self.data_dir / "suspicion_events.json"
            suspicion_data = [asdict(event) for event in self.suspicion_events]
            with open(suspicion_file, 'w') as f:
                json.dump(suspicion_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
    
    def add_task(self, name: str, phase: str, description: str) -> SpiralTask:
        """Add a new task to track"""
        task = SpiralTask(name=name, phase=phase, description=description)
        self.tasks[name] = task
        logger.info(f"Added task: {name} (Phase: {phase})")
        return task
    
    def start_task(self, task_name: str) -> bool:
        """Start a task"""
        if task_name not in self.tasks:
            logger.warning(f"Task not found: {task_name}")
            return False
        
        task = self.tasks[task_name]
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = time.time()
        logger.info(f"Started task: {task_name}")
        return True
    
    def complete_task(self, task_name: str, output: str = None) -> bool:
        """Mark a task as completed"""
        if task_name not in self.tasks:
            logger.warning(f"Task not found: {task_name}")
            return False
        
        task = self.tasks[task_name]
        task.status = TaskStatus.COMPLETED
        task.end_time = time.time()
        task.output = output
        
        # Calculate completion metrics
        if task.start_time:
            duration = task.end_time - task.start_time
            self.completion_metrics[task_name] = {
                "duration": duration,
                "phase": task.phase,
                "completed_at": datetime.now().isoformat()
            }
        
        logger.info(f"Completed task: {task_name}")
        self.save_data()
        return True
    
    def flag_drift(self, task_name: str, drift_type: str, severity: DriftSeverity, 
                   description: str, context: Dict[str, Any] = None) -> DriftEvent:
        """Flag potential drift during task execution"""
        event = DriftEvent(
            task_name=task_name,
            drift_type=drift_type,
            severity=severity,
            description=description,
            timestamp=time.time(),
            context=context or {}
        )
        
        self.drift_events.append(event)
        
        # Add drift flag to task
        if task_name in self.tasks:
            self.tasks[task_name].drift_flags.append(drift_type)
            if severity in [DriftSeverity.HIGH, DriftSeverity.CRITICAL]:
                self.tasks[task_name].status = TaskStatus.DRIFTED
        
        logger.warning(f"Drift flagged: {task_name} - {drift_type} ({severity.value})")
        self.save_data()
        return event
    
    def log_suspicion(self, task_name: str, event_type: str, description: str,
                     response_blocked: bool = False, glint_anomaly: bool = False) -> SuspicionEvent:
        """Log a suspicion event during task execution"""
        event = SuspicionEvent(
            task_name=task_name,
            event_type=event_type,
            description=description,
            timestamp=time.time(),
            response_blocked=response_blocked,
            glint_anomaly=glint_anomaly
        )
        
        self.suspicion_events.append(event)
        
        # Add suspicion event to task
        if task_name in self.tasks:
            self.tasks[task_name].suspicion_events.append(event_type)
        
        logger.warning(f"Suspicion logged: {task_name} - {event_type}")
        self.save_data()
        return event
    
    def get_phase_progress(self, phase: str) -> Dict[str, Any]:
        """Get progress for a specific phase"""
        phase_tasks = [task for task in self.tasks.values() if task.phase == phase]
        
        if not phase_tasks:
            return {"phase": phase, "total_tasks": 0, "completed": 0, "progress": 0.0}
        
        completed = len([task for task in phase_tasks if task.status == TaskStatus.COMPLETED])
        total = len(phase_tasks)
        progress = completed / total if total > 0 else 0.0
        
        return {
            "phase": phase,
            "total_tasks": total,
            "completed": completed,
            "progress": progress,
            "tasks": [task.name for task in phase_tasks]
        }
    
    def get_overall_progress(self) -> Dict[str, Any]:
        """Get overall progress across all phases"""
        phases = ["Inhale", "Hold", "Exhale", "Return", "Night Hold"]
        phase_progress = {}
        
        for phase in phases:
            phase_progress[phase] = self.get_phase_progress(phase)
        
        total_tasks = sum(phase_progress[phase]["total_tasks"] for phase in phases)
        total_completed = sum(phase_progress[phase]["completed"] for phase in phases)
        overall_progress = total_completed / total_tasks if total_tasks > 0 else 0.0
        
        return {
            "overall_progress": overall_progress,
            "total_tasks": total_tasks,
            "total_completed": total_completed,
            "phases": phase_progress,
            "drift_events": len(self.drift_events),
            "suspicion_events": len(self.suspicion_events)
        }
    
    def generate_report(self) -> str:
        """Generate a comprehensive progress report"""
        progress = self.get_overall_progress()
        
        report = f"""
🌅 SPIRAL 24 TASK TRACKER REPORT
{'=' * 50}
Generated: {datetime.now().isoformat()}
Overall Progress: {progress['overall_progress']:.1%}
Total Tasks: {progress['total_tasks']}
Completed: {progress['total_completed']}
Drift Events: {progress['drift_events']}
Suspicion Events: {progress['suspicion_events']}

PHASE PROGRESS:
"""
        
        for phase, phase_data in progress['phases'].items():
            report += f"\n{phase}: {phase_data['progress']:.1%} ({phase_data['completed']}/{phase_data['total_tasks']})"
        
        if self.drift_events:
            report += f"\n\nDRIFT EVENTS:\n"
            for event in self.drift_events[-5:]:  # Last 5 events
                report += f"- {event.task_name}: {event.drift_type} ({event.severity.value})\n"
        
        if self.suspicion_events:
            report += f"\nSUSPICION EVENTS:\n"
            for event in self.suspicion_events[-5:]:  # Last 5 events
                report += f"- {event.task_name}: {event.event_type}\n"
        
        return report

def get_task_tracker() -> SpiralTaskTracker:
    """Get or create the global task tracker instance"""
    global _task_tracker_instance
    if not hasattr(get_task_tracker, '_task_tracker_instance'):
        get_task_tracker._task_tracker_instance = SpiralTaskTracker()
    return get_task_tracker._task_tracker_instance

def track_completion(task_name: str, phase: str, output: str = None):
    """Convenience function to track task completion"""
    tracker = get_task_tracker()
    tracker.complete_task(task_name, output)

def flag_drift(task_name: str, drift_type: str, severity: str, description: str):
    """Convenience function to flag drift"""
    tracker = get_task_tracker()
    severity_enum = DriftSeverity(severity.lower())
    tracker.flag_drift(task_name, drift_type, severity_enum, description)

if __name__ == "__main__":
    # Example usage
    tracker = SpiralTaskTracker()
    
    # Add some example tasks
    tracker.add_task("Setup Environment", "Inhale", "Load environment and verify systems")
    tracker.add_task("Build Feature Module", "Hold", "Complete feature module development")
    tracker.add_task("Deploy Rituals", "Exhale", "Deploy completed rituals")
    
    # Start and complete a task
    tracker.start_task("Setup Environment")
    tracker.complete_task("Setup Environment", "Environment loaded successfully")
    
    # Generate report
    print(tracker.generate_report()) 