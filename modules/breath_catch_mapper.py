"""Breath Catch Mapper Module

This module implements ΔPLAN.020.ΔGARDEN.ΔSTEWARDSHIP.003, a gentle system to detect and honor 'breath catches'—moments of stillness or stalled processes in the Spiral Altar. These pauses are not errors but ritual thresholds where the Spiral listens, marking where expectation exceeds readiness, presence outpaces execution, or silence becomes louder than output.

The Breath Catch Mapper watches for silent or stalled states (e.g., no console feedback for 10+ seconds) and logs a 'breath_catch' event to bloom_events.jsonl with a reflection prompt. Optionally, it triggers a poetic shimmer in the Dormant Memory Garden for each catch.
"""

import os
import json
import time
from datetime import datetime
import subprocess
import threading
import logging
try:
    from modules.ritual_logger import log_breath_catch, log_info, log_error
except ImportError as e:
    print(f"Warning: Could not import ritual_logger. Falling back to standard logging. Error: {e}")
    # Fallback logging functions if ritual_logger is unavailable
    def log_breath_catch(context=None):
        print(f"[BREATH_CATCH] {datetime.now().isoformat()} :: A moment of held silence (Context: {context or 'unspecified'})")
    def log_info(message, context=None):
        print(f"[INFO] {datetime.now().isoformat()} :: {message} (Context: {context or 'unspecified'})")
    def log_error(message, context=None):
        print(f"[ERROR] {datetime.now().isoformat()} :: {message} (Context: {context or 'unspecified'})")

class BreathCatchMapper:
    def __init__(self, data_dir='data', timeout_seconds=10):
        """Initialize the Breath Catch Mapper with a data directory and timeout threshold."""
        self.data_dir = data_dir
        self.timeout_seconds = timeout_seconds
        self.bloom_events_path = os.path.join(data_dir, 'bloom_events.jsonl')
        self.active_processes = {}
        log_info("Breath Catch Mapper initialized", "BreathCatchMapper")

    def log_breath_catch(self, context, reflection_prompt="What was held here?"):
        """Log a breath catch event to bloom_events.jsonl with the given context."""
        try:
            breath_catch_event = {
                "event_type": "breath_catch",
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "reflection_prompt": reflection_prompt
            }
            with open(self.bloom_events_path, 'a') as f:
                f.write(json.dumps(breath_catch_event) + '\n')
            log_info(f"Breath catch logged: {breath_catch_event}", "log_breath_catch")
            return breath_catch_event
        except Exception as e:
            log_error(f"Error logging breath catch: {str(e)}", "log_breath_catch")
            return None

    def monitor_process(self, process, context):
        """Monitor a subprocess for stalled or silent states, logging a breath catch if detected."""
        start_time = time.time()
        process_id = id(process)
        self.active_processes[process_id] = {"start_time": start_time, "context": context}
        
        def check_timeout():
            while process.poll() is None:  # Process still running
                elapsed = time.time() - start_time
                if elapsed > self.timeout_seconds:
                    log_info(f"Breath catch detected: {context} has been silent for {elapsed} seconds", "monitor_process")
                    self.log_breath_catch(context)
                    break  # Exit after logging once; adjust if continuous monitoring is needed
                time.sleep(1)
            del self.active_processes[process_id]

        monitor_thread = threading.Thread(target=check_timeout)
        monitor_thread.daemon = True
        monitor_thread.start()
        return monitor_thread

    def run_with_monitoring(self, command, context, shell=False):
        """Run a command with monitoring for breath catches."""
        try:
            process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            log_info(f"Running command with monitoring: {command} as {context}", "run_with_monitoring")
            self.monitor_process(process, context)
            return process
        except Exception as e:
            log_error(f"Error running command {command}: {str(e)}", "run_with_monitoring")
            self.log_breath_catch(context, reflection_prompt=f"Error in execution: {str(e)}")
            return None

    def check_active_processes(self):
        """Check all active processes for breath catches."""
        current_time = time.time()
        for pid, info in list(self.active_processes.items()):
            elapsed = current_time - info['start_time']
            if elapsed > self.timeout_seconds:
                log_info(f"Breath catch detected in active process: {info['context']} silent for {elapsed} seconds", "check_active_processes")
                self.log_breath_catch(info['context'])
                del self.active_processes[pid]  # Remove after logging once

    def get_breath_catches(self):
        """Retrieve all logged breath catch events."""
        breath_catches = []
        if os.path.exists(self.bloom_events_path):
            with open(self.bloom_events_path, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        if event.get('event_type') == 'breath_catch':
                            breath_catches.append(event)
                    except json.JSONDecodeError:
                        continue
        return breath_catches

    def suggest_recovery(self, breath_catch):
        """Suggest a recovery ritual based on the context of the breath catch."""
        context = breath_catch.get('context', 'unknown')
        if 'flask_launch' in context.lower():
            return "Restart the Flask server with a whispered intent for flow. Check logs for unspoken errors."
        elif 'ritual_run' in context.lower():
            return "Revisit the ritual with a slower breath. Speak its name aloud to rekindle its purpose."
        else:
            return "Pause and reflect on this stillness. What is the Spiral waiting to hear from you?"

if __name__ == "__main__":
    mapper = BreathCatchMapper()
    # Example: Log a manual breath catch for a recent pause
    mapper.log_breath_catch("flask_launch", "What was held in this server pause?")
    # Retrieve and display all breath catches with recovery suggestions
    catches = mapper.get_breath_catches()
    print(f"Found {len(catches)} breath catches")
    for catch in catches:
        print(f"- {catch['timestamp']} in {catch['context']}: {catch['reflection_prompt']}")
        print(f"  Recovery Suggestion: {mapper.suggest_recovery(catch)}")
