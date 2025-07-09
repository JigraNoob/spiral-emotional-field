#!/usr/bin/env python3
"""
Ritual Logger - Document daily Spiral reflections and completion metrics
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

class RitualPhase(Enum):
    INHALE = "inhale"
    HOLD = "hold"
    EXHALE = "exhale"
    RETURN = "return"
    NIGHT_HOLD = "night_hold"

class CompletionStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"

@dataclass
class DailyReflection:
    """Represents a daily Spiral reflection"""
    date: str
    phase: RitualPhase
    outputs: List[str]
    insights: List[str]
    challenges: List[str]
    completions: Dict[str, CompletionStatus]
    glints_emitted: int
    suspicion_events: int
    drift_events: int
    breath_quality: str  # "excellent", "good", "fair", "poor"
    ritual_notes: str
    timestamp: float

@dataclass
class CompletionMetric:
    """Represents completion metrics for a specific task or phase"""
    task_name: str
    phase: RitualPhase
    status: CompletionStatus
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    duration: Optional[float] = None
    output: Optional[str] = None
    notes: Optional[str] = None

class RitualLogger:
    """
    Log daily Spiral reflections and completion metrics
    """
    
    def __init__(self, data_dir: str = "data/ritual_logs"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.daily_reflections: List[DailyReflection] = []
        self.completion_metrics: List[CompletionMetric] = []
        self.current_phase: Optional[RitualPhase] = None
        self.current_date: str = datetime.now().strftime("%Y-%m-%d")
        
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing ritual data from files"""
        try:
            # Load daily reflections
            reflections_file = self.data_dir / "daily_reflections.json"
            if reflections_file.exists():
                with open(reflections_file, 'r') as f:
                    reflections_data = json.load(f)
                    for reflection_data in reflections_data:
                        reflection = DailyReflection(**reflection_data)
                        reflection.phase = RitualPhase(reflection_data['phase'])
                        self.daily_reflections.append(reflection)
            
            # Load completion metrics
            metrics_file = self.data_dir / "completion_metrics.json"
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    metrics_data = json.load(f)
                    for metric_data in metrics_data:
                        metric = CompletionMetric(**metric_data)
                        metric.phase = RitualPhase(metric_data['phase'])
                        metric.status = CompletionStatus(metric_data['status'])
                        self.completion_metrics.append(metric)
                        
        except Exception as e:
            logger.warning(f"Failed to load existing ritual data: {e}")
    
    def save_data(self):
        """Save current ritual data to files"""
        try:
            # Save daily reflections
            reflections_file = self.data_dir / "daily_reflections.json"
            reflections_data = [asdict(reflection) for reflection in self.daily_reflections]
            with open(reflections_file, 'w') as f:
                json.dump(reflections_data, f, indent=2)
            
            # Save completion metrics
            metrics_file = self.data_dir / "completion_metrics.json"
            metrics_data = [asdict(metric) for metric in self.completion_metrics]
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save ritual data: {e}")
    
    def set_current_phase(self, phase: RitualPhase):
        """Set the current ritual phase"""
        self.current_phase = phase
        logger.info(f"Current phase set to: {phase.value}")
    
    def log_daily_reflection(self, phase: RitualPhase, outputs: List[str], insights: List[str],
                           challenges: List[str], completions: Dict[str, CompletionStatus],
                           glints_emitted: int = 0, suspicion_events: int = 0, drift_events: int = 0,
                           breath_quality: str = "good", ritual_notes: str = "") -> DailyReflection:
        """Log a daily Spiral reflection"""
        
        reflection = DailyReflection(
            date=self.current_date,
            phase=phase,
            outputs=outputs,
            insights=insights,
            challenges=challenges,
            completions=completions,
            glints_emitted=glints_emitted,
            suspicion_events=suspicion_events,
            drift_events=drift_events,
            breath_quality=breath_quality,
            ritual_notes=ritual_notes,
            timestamp=time.time()
        )
        
        self.daily_reflections.append(reflection)
        logger.info(f"Logged daily reflection for phase: {phase.value}")
        self.save_data()
        return reflection
    
    def log_completion_metric(self, task_name: str, phase: RitualPhase, status: CompletionStatus,
                            start_time: Optional[float] = None, end_time: Optional[float] = None,
                            output: Optional[str] = None, notes: Optional[str] = None) -> CompletionMetric:
        """Log completion metrics for a specific task"""
        
        duration = None
        if start_time and end_time:
            duration = end_time - start_time
        
        metric = CompletionMetric(
            task_name=task_name,
            phase=phase,
            status=status,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            output=output,
            notes=notes
        )
        
        self.completion_metrics.append(metric)
        logger.info(f"Logged completion metric: {task_name} - {status.value}")
        self.save_data()
        return metric
    
    def get_phase_completion_summary(self, phase: RitualPhase) -> Dict[str, Any]:
        """Get completion summary for a specific phase"""
        phase_metrics = [metric for metric in self.completion_metrics if metric.phase == phase]
        
        if not phase_metrics:
            return {
                "phase": phase.value,
                "total_tasks": 0,
                "completed": 0,
                "in_progress": 0,
                "failed": 0,
                "completion_rate": 0.0
            }
        
        total_tasks = len(phase_metrics)
        completed = len([m for m in phase_metrics if m.status == CompletionStatus.COMPLETED])
        in_progress = len([m for m in phase_metrics if m.status == CompletionStatus.IN_PROGRESS])
        failed = len([m for m in phase_metrics if m.status == CompletionStatus.FAILED])
        completion_rate = completed / total_tasks if total_tasks > 0 else 0.0
        
        return {
            "phase": phase.value,
            "total_tasks": total_tasks,
            "completed": completed,
            "in_progress": in_progress,
            "failed": failed,
            "completion_rate": completion_rate,
            "tasks": [m.task_name for m in phase_metrics]
        }
    
    def get_daily_summary(self, date: str = None) -> Dict[str, Any]:
        """Get daily summary for a specific date"""
        if date is None:
            date = self.current_date
        
        daily_reflections = [r for r in self.daily_reflections if r.date == date]
        daily_metrics = [m for m in self.completion_metrics if m.start_time and 
                        datetime.fromtimestamp(m.start_time).strftime("%Y-%m-%d") == date]
        
        if not daily_reflections:
            return {
                "date": date,
                "reflections": 0,
                "total_tasks": 0,
                "completed_tasks": 0,
                "glints_emitted": 0,
                "suspicion_events": 0,
                "drift_events": 0,
                "breath_quality": "unknown"
            }
        
        # Use the most recent reflection for the day
        latest_reflection = max(daily_reflections, key=lambda r: r.timestamp)
        
        completed_tasks = len([m for m in daily_metrics if m.status == CompletionStatus.COMPLETED])
        total_tasks = len(daily_metrics)
        
        return {
            "date": date,
            "reflections": len(daily_reflections),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0.0,
            "glints_emitted": latest_reflection.glints_emitted,
            "suspicion_events": latest_reflection.suspicion_events,
            "drift_events": latest_reflection.drift_events,
            "breath_quality": latest_reflection.breath_quality,
            "phases": [r.phase.value for r in daily_reflections]
        }
    
    def get_weekly_summary(self, end_date: str = None) -> Dict[str, Any]:
        """Get weekly summary ending on the specified date"""
        if end_date is None:
            end_date = self.current_date
        
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        start_dt = end_dt - timedelta(days=7)
        
        weekly_reflections = [
            r for r in self.daily_reflections
            if start_dt <= datetime.strptime(r.date, "%Y-%m-%d") <= end_dt
        ]
        
        weekly_metrics = [
            m for m in self.completion_metrics
            if m.start_time and start_dt <= datetime.fromtimestamp(m.start_time) <= end_dt
        ]
        
        total_tasks = len(weekly_metrics)
        completed_tasks = len([m for m in weekly_metrics if m.status == CompletionStatus.COMPLETED])
        
        total_glints = sum(r.glints_emitted for r in weekly_reflections)
        total_suspicion = sum(r.suspicion_events for r in weekly_reflections)
        total_drift = sum(r.drift_events for r in weekly_reflections)
        
        # Calculate average breath quality
        breath_qualities = [r.breath_quality for r in weekly_reflections if r.breath_quality != "unknown"]
        avg_breath_quality = "unknown"
        if breath_qualities:
            quality_scores = {"excellent": 4, "good": 3, "fair": 2, "poor": 1}
            avg_score = sum(quality_scores.get(q, 0) for q in breath_qualities) / len(breath_qualities)
            if avg_score >= 3.5:
                avg_breath_quality = "excellent"
            elif avg_score >= 2.5:
                avg_breath_quality = "good"
            elif avg_score >= 1.5:
                avg_breath_quality = "fair"
            else:
                avg_breath_quality = "poor"
        
        return {
            "period": f"{start_dt.strftime('%Y-%m-%d')} to {end_date}",
            "total_reflections": len(weekly_reflections),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0.0,
            "total_glints": total_glints,
            "total_suspicion": total_suspicion,
            "total_drift": total_drift,
            "avg_breath_quality": avg_breath_quality,
            "days_with_reflections": len(set(r.date for r in weekly_reflections))
        }
    
    def generate_daily_report(self, date: str = None) -> str:
        """Generate a daily ritual report"""
        if date is None:
            date = self.current_date
        
        summary = self.get_daily_summary(date)
        phase_summaries = {}
        
        for phase in RitualPhase:
            phase_summaries[phase.value] = self.get_phase_completion_summary(phase)
        
        report = f"""
🕯️ SPIRAL RITUAL DAILY REPORT
{'=' * 50}
Date: {date}
Generated: {datetime.now().isoformat()}

DAILY SUMMARY:
- Total Tasks: {summary['total_tasks']}
- Completed Tasks: {summary['completed_tasks']}
- Completion Rate: {summary['completion_rate']:.1%}
- Glints Emitted: {summary['glints_emitted']}
- Suspicion Events: {summary['suspicion_events']}
- Drift Events: {summary['drift_events']}
- Breath Quality: {summary['breath_quality']}

PHASE COMPLETION:
"""
        
        for phase_name, phase_summary in phase_summaries.items():
            if phase_summary['total_tasks'] > 0:
                report += f"\n{phase_name.upper()}:"
                report += f"\n  - Completion Rate: {phase_summary['completion_rate']:.1%}"
                report += f"\n  - Tasks: {phase_summary['completed']}/{phase_summary['total_tasks']}"
                if phase_summary['tasks']:
                    report += f"\n  - Completed: {', '.join(phase_summary['tasks'][:3])}"
                    if len(phase_summary['tasks']) > 3:
                        report += f" (+{len(phase_summary['tasks']) - 3} more)"
        
        # Add recent reflections
        daily_reflections = [r for r in self.daily_reflections if r.date == date]
        if daily_reflections:
            latest = max(daily_reflections, key=lambda r: r.timestamp)
            report += f"\n\nLATEST REFLECTION ({latest.phase.value}):"
            if latest.outputs:
                report += f"\n- Outputs: {', '.join(latest.outputs[:3])}"
            if latest.insights:
                report += f"\n- Insights: {', '.join(latest.insights[:2])}"
            if latest.ritual_notes:
                report += f"\n- Notes: {latest.ritual_notes[:100]}..."
        
        return report
    
    def generate_weekly_report(self, end_date: str = None) -> str:
        """Generate a weekly ritual report"""
        if end_date is None:
            end_date = self.current_date
        
        summary = self.get_weekly_summary(end_date)
        
        report = f"""
🕯️ SPIRAL RITUAL WEEKLY REPORT
{'=' * 50}
Period: {summary['period']}
Generated: {datetime.now().isoformat()}

WEEKLY SUMMARY:
- Total Reflections: {summary['total_reflections']}
- Days with Reflections: {summary['days_with_reflections']}/7
- Total Tasks: {summary['total_tasks']}
- Completed Tasks: {summary['completed_tasks']}
- Completion Rate: {summary['completion_rate']:.1%}
- Total Glints: {summary['total_glints']}
- Total Suspicion Events: {summary['total_suspicion']}
- Total Drift Events: {summary['total_drift']}
- Average Breath Quality: {summary['avg_breath_quality']}

WEEKLY TRENDS:
"""
        
        # Calculate daily trends
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        for i in range(7):
            day_date = (end_dt - timedelta(days=i)).strftime("%Y-%m-%d")
            day_summary = self.get_daily_summary(day_date)
            report += f"\n{day_date}: {day_summary['completed_tasks']}/{day_summary['total_tasks']} tasks"
            if day_summary['breath_quality'] != "unknown":
                report += f" ({day_summary['breath_quality']} breath)"
        
        return report

def get_ritual_logger() -> RitualLogger:
    """Get or create the global ritual logger instance"""
    global _ritual_logger_instance
    if not hasattr(get_ritual_logger, '_ritual_logger_instance'):
        get_ritual_logger._ritual_logger_instance = RitualLogger()
    return get_ritual_logger._ritual_logger_instance

def log_daily_reflection(phase: str, outputs: List[str], insights: List[str], 
                        challenges: List[str], completions: Dict[str, str],
                        **kwargs):
    """Convenience function to log daily reflection"""
    logger = get_ritual_logger()
    phase_enum = RitualPhase(phase.lower())
    completion_enums = {k: CompletionStatus(v.lower()) for k, v in completions.items()}
    return logger.log_daily_reflection(phase_enum, outputs, insights, challenges, completion_enums, **kwargs)

if __name__ == "__main__":
    # Example usage
    logger = RitualLogger()
    
    # Log a daily reflection
    reflection = logger.log_daily_reflection(
        phase=RitualPhase.HOLD,
        outputs=["Feature module completed", "Shrine system updated"],
        insights=["Breath awareness improves focus", "Ritual structure provides clarity"],
        challenges=["Time management", "System integration"],
        completions={"Setup Environment": "completed", "Build Feature": "completed"},
        glints_emitted=15,
        suspicion_events=2,
        drift_events=1,
        breath_quality="good",
        ritual_notes="Strong focus during build phase"
    )
    
    # Generate report
    print(logger.generate_daily_report()) 