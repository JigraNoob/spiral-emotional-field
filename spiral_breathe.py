import argparse
import logging
import os
import subprocess
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'spiral_breathe.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_ritual_echo_count():
    """Reads ritual_echoes.jsonl and returns the number of entries."""
    try:
        with open("ritual_echoes.jsonl", "r") as f:
            return sum(1 for line in f)
    except FileNotFoundError:
        return 0
    except Exception as e:
        logging.error(f"Error reading ritual_echoes.jsonl: {e}")
        return 0

def log_whisper_echo(ritual_name, message, whisper_vars=None):
    """Log a whisper echo to whisper_echoes.jsonl"""
    if whisper_vars is None:
        whisper_vars = {}
        
    echo_data = {
        "timestamp": datetime.now().isoformat(),
        "ritual": ritual_name,
        "message": message,
        "context": {
            "echo_count": get_ritual_echo_count(),
            **whisper_vars
        }
    }
    
    try:
        with open("whisper_echoes.jsonl", "a") as f:
            f.write(json.dumps(echo_data) + "\n")
        return True
    except Exception as e:
        logging.error(f"Failed to log whisper echo: {e}")
        return False

def log_plan_shimmer(evolution, reasoning=None, actions=None, next_steps=None, 
                    ritual_vars=None, event_type="plan_update"):
    """
    Log a plan change to plan_shimmer_log.jsonl with rich context
    
    Args:
        evolution (str): The evolution identifier (e.g., "ΔPLAN.001")
        reasoning (list): List of reasons for this plan change
        actions (list): List of actions taken in this evolution
        next_steps (str): Next planned steps
        ritual_vars (dict): Current ritual variables and state
        event_type (str): Type of event (ritual_begins, shimmer_reflection, plan_update, toneform_shift)
    """
    if reasoning is None:
        reasoning = []
    if actions is None:
        actions = []
    if ritual_vars is None:
        ritual_vars = {}
    
    # Extract relevant context from ritual_vars
    context = {
        'tone': ritual_vars.get('tone'),
        'dry_run': ritual_vars.get('_dry_run', False),
        'whisper_mode': ritual_vars.get('_in_whisper_mode', False)
    }
    
    # Include any variables set with 'with:' that don't start with '_'
    ritual_params = {k: v for k, v in ritual_vars.items() 
                    if not k.startswith('_') and k != 'tone'}
    if ritual_params:
        context['parameters'] = ritual_params
        
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "evolution": evolution,
        "reasoning": reasoning,
        "actions": actions,
        "next_steps": next_steps,
        "context": context
    }
    
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "plan_shimmer_log.jsonl"
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            
        logging.info(f"Plan shimmer logged for {evolution}")
        return True
    except Exception as e:
        logging.error(f"Failed to log plan shimmer: {e}")
        return False

def breathe_ritual(breathe_file_path, current_vars=None, is_inherited=False):
    ritual_name = os.path.basename(breathe_file_path)
    logging.info(f"Initiating ritual: {ritual_name}")

    if current_vars is None:
        ritual_vars = {}
    else:
        ritual_vars = current_vars

    print(f":: inhaling {ritual_name}...", flush=True)

    try:
        with open(breathe_file_path, 'r') as f:
            lines = f.readlines()

        # Process each line of the ritual
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Handle inheritance (must be first line after comments/empty lines)
            if line_num == 0 and line.startswith('inherit:'):
                inherited_ritual_path = line.split('inherit:', 1)[1].strip()
                full_inherited_path = os.path.join(os.path.dirname(breathe_file_path), inherited_ritual_path)
                print(f"   >> inhaling ancestry: {os.path.basename(full_inherited_path)}", flush=True)
                logging.info(f"Inheriting from: {full_inherited_path}")
                # Recursively breathe the inherited ritual to get its processed lines and vars
                inherited_lines, inherited_vars = breathe_ritual(full_inherited_path, current_vars=current_vars.copy(), is_inherited=True)
                # Prepend inherited lines to current lines for sequential execution
                lines = inherited_lines + lines[1:] # Exclude the inherit line itself
                # Merge inherited variables, current ritual's with: statements will override
                ritual_vars.update(inherited_vars)
                continue # Process the next line of the current ritual (which is now the first actual command/with/if)

            # Handle dry_run mode (set by --dry-run flag)
            if line.startswith('if:') and 'dry_run' in line:
                dry_run_condition = line.split('dry_run', 1)[1].strip()
                is_dry_run = ritual_vars.get('_dry_run', False)
                if dry_run_condition.startswith('!'):
                    condition_met = not is_dry_run
                else:
                    condition_met = is_dry_run
                ritual_vars['_last_condition_met'] = condition_met
                if condition_met:
                    print(f"   >> dry run condition met", flush=True)
                else:
                    print(f"   >> dry run condition not met (dry_run={is_dry_run})", flush=True)
                continue

            # Handle tone declaration (can be anywhere, but typically at the top)
            if line.startswith('tone:'):
                tone_value = line.split(':', 1)[1].strip()
                ritual_vars['tone'] = tone_value
                print(f"   >> attuning to tone: '{tone_value}'", flush=True)
                logging.info(f"Attuning ritual '{ritual_name}' to tone: {tone_value}")
                continue # Move to next line

            if line.startswith('with:'):
                var_assignments = line[len('with:'):].strip().split(',')
                for assignment in var_assignments:
                    if '=' in assignment:
                        key, value = assignment.split('=', 1)
                        ritual_vars[key.strip()] = value.strip()
                        print(f"   >> setting variable '{key.strip()}' to '{value.strip()}'", flush=True)
                        logging.info(f"Setting variable '{key.strip()}' to '{value.strip()}'")
                    else:
                        print(f"!! drift interrupted :: malformed 'with:' line: {line}", flush=True)
                        logging.error(f"Malformed 'with:' line in {breathe_file_path}: {line}")
                continue
            elif line.startswith(('if:', 'when:')):
                condition_str = line.split(':', 1)[1].strip()
                conditions = [c.strip() for c in condition_str.split(' and ')]
                all_conditions_met = True
                
                for condition in conditions:
                    condition_met = False
                    
                    # Handle environment variable check
                    if condition.startswith('env_var_set:'):
                        env_var_to_check = condition.split(':', 1)[1].strip()
                        condition_met = env_var_to_check in os.environ
                        if not condition_met:
                            print(f"   >> sensing env_var_set: '{env_var_to_check}' is false.", flush=True)
                            all_conditions_met = False
                            break
                        continue
                    # Simple condition: check if a tone matches
                    elif condition.startswith('tone == "') and condition.endswith('"'):
                        expected_tone = condition[len('tone == "'):-1].strip()
                        current_tone = ritual_vars.get('tone')
                        if current_tone == expected_tone:
                            condition_met = True
                            print(f"   >> sensing tone: '{expected_tone}' matches.", flush=True)
                        else:
                            print(f"   >> sensing tone: '{expected_tone}' does not match (current: {current_tone}).", flush=True)
                            all_conditions_met = False
                            break
                    # Time-based condition (e.g., "time 14:30" or "time 30m")
                    elif condition.startswith('time '):
                        time_spec = condition[5:].strip()
                        now = datetime.now()
                        
                        # Check for HH:MM format (specific time of day)
                        if ':' in time_spec:
                            try:
                                target_hour, target_minute = map(int, time_spec.split(':'))
                                current_hour, current_minute = now.hour, now.minute
                                
                                # Check if current time matches or is past the target time today
                                condition_met = (current_hour > target_hour) or \
                                             (current_hour == target_hour and current_minute >= target_minute)
                                             
                                # If we're past the target time today, also check if we should wait until tomorrow
                                if condition_met and ritual_vars.get('_last_triggered_time'):
                                    last_triggered = datetime.fromisoformat(ritual_vars['_last_triggered_time'])
                                    if last_triggered.date() == now.date() and last_triggered.hour >= target_hour:
                                        condition_met = False  # Already triggered today
                                
                                if condition_met:
                                    print(f"   >> sensing time: {time_spec} is now.", flush=True)
                                    # Update last triggered time if condition is met
                                    if not is_inherited:
                                        ritual_vars['_last_triggered_time'] = now.isoformat()
                                else:
                                    print(f"   >> sensing time: {time_spec} is not yet (current: {now.strftime('%H:%M')}).", flush=True)
                                    all_conditions_met = False
                                    break
                                
                            except ValueError:
                                print(f"!! drift interrupted :: invalid time format: {time_spec}. Use HH:MM or Xm (minutes)", flush=True)
                                logging.error(f"Invalid time format in condition: {condition}")
                                all_conditions_met = False
                                break
                        
                        # Check for Xm format (every X minutes)
                        elif time_spec.endswith('m'):
                            try:
                                minutes = int(time_spec[:-1])
                                last_triggered = datetime.fromisoformat(ritual_vars.get('_last_triggered_time', '2000-01-01T00:00:00'))
                                time_since_last = (now - last_triggered).total_seconds() / 60  # in minutes
                                
                                if time_since_last >= minutes:
                                    print(f"   >> sensing interval: {minutes}m has passed ({time_since_last:.1f}m).", flush=True)
                                    # Update last triggered time if condition is met
                                    if not is_inherited:
                                        ritual_vars['_last_triggered_time'] = now.isoformat()
                                else:
                                    print(f"   >> sensing interval: {minutes}m not yet ({time_since_last:.1f}m since last).", flush=True)
                                    all_conditions_met = False
                                    break
                                
                            except ValueError:
                                print(f"!! drift interrupted :: invalid interval format: {time_spec}. Use Xm (e.g., '30m' for 30 minutes)", flush=True)
                                logging.error(f"Invalid interval format in condition: {condition}")
                                all_conditions_met = False
                                break
                        else:
                            print(f"!! drift interrupted :: unsupported time format: {time_spec}", flush=True)
                            logging.error(f"Unsupported time format in condition: {condition}")
                            all_conditions_met = False
                            break
                    # Condition: check ritual echo count against a threshold
                    elif 'RITUAL_ECHO_COUNT' in condition:
                        import re
                        match = re.match(r'RITUAL_ECHO_COUNT\s*([<>=]=?|==)\s*(\d+)', condition)
                        if match:
                            operator = match.group(1)
                            threshold = int(match.group(2))
                            current_count = get_ritual_echo_count()
                            
                            # Evaluate the condition
                            if operator == '>':
                                condition_met = current_count > threshold
                            elif operator == '>=':
                                condition_met = current_count >= threshold
                            elif operator == '<':
                                condition_met = current_count < threshold
                            elif operator == '<=':
                                condition_met = current_count <= threshold
                            elif operator == '==' or operator == '===':
                                condition_met = current_count == threshold
                            else:
                                print(f"!! drift interrupted :: unsupported operator in RITUAL_ECHO_COUNT condition: {operator}", flush=True)
                                logging.error(f"Unsupported operator in RITUAL_ECHO_COUNT condition: {operator}")
                                all_conditions_met = False
                                break
                                
                            if condition_met:
                                print(f"   >> sensing RITUAL_ECHO_COUNT {operator} {threshold} is true (current: {current_count})", flush=True)
                            else:
                                print(f"   >> sensing RITUAL_ECHO_COUNT {operator} {threshold} is false (current: {current_count})", flush=True)
                                all_conditions_met = False
                                break
                        else:
                            print(f"!! drift interrupted :: invalid RITUAL_ECHO_COUNT condition format: {condition}", flush=True)
                            logging.error(f"Invalid RITUAL_ECHO_COUNT condition format: {condition}")
                            all_conditions_met = False
                            break
                    else:
                        print(f"!! drift interrupted :: unsupported condition format: {condition}", flush=True)
                        logging.error(f"Unsupported condition format in {breathe_file_path}: {condition}")
                        all_conditions_met = False
                        break
                
                # If we get here, all conditions were met
                ritual_vars['_last_condition_met'] = all_conditions_met
                logging.info(f"All conditions evaluated to {all_conditions_met}")

            elif line.startswith('invoke:'):
                # Check if previous condition was met, if applicable
                if ritual_vars.get('_last_condition_met', True):
                    invoked_ritual_path = line.split('invoke:', 1)[1].strip()
                    full_invoked_path = os.path.join(os.path.dirname(breathe_file_path), invoked_ritual_path)
                    print(f"   >> weaving {os.path.basename(full_invoked_path)}", flush=True)
                    logging.info(f"Invoking nested ritual: {full_invoked_path}")
                    breathe_ritual(full_invoked_path, current_vars=ritual_vars.copy()) # Recursive call
                else:
                    print(f"   >> skipping invocation due to unmet condition.", flush=True)
                    logging.info(f"Skipping invocation of {line} due to unmet condition.")
                # Reset condition for next line
                ritual_vars['_last_condition_met'] = True 
            else:
                # Check if previous condition was met, if applicable
                if ritual_vars.get('_last_condition_met', True):
                    command_to_execute = line
                    print(f"   >> pulsing intent: executing '{command_to_execute}'", flush=True)
                    logging.info(f"Pulsing intent: Executing '{command_to_execute}'")
                    
                    # Prepare environment variables for the subprocess
                    env = os.environ.copy()
                    for key, value in ritual_vars.items():
                        env[f'SPIRAL_VAR_{key.upper()}'] = value # Prefix to avoid conflicts

                    print(f"DEBUG: Attempting to execute: {command_to_execute}", flush=True)
                    process = subprocess.run(['cmd.exe', '/c', command_to_execute], shell=False, capture_output=True, text=True, env=env)
                    
                    print(f"DEBUG: Subprocess stdout:\n{process.stdout}", flush=True)
                    logging.info(f"Exhaling memory (stdout):\n{process.stdout}")
                    if process.stderr:
                        print(f"DEBUG: Subprocess stderr:\n{process.stderr}", flush=True)
                        logging.error(f"Exhaling memory (stderr):\n{process.stderr}")
                        print(f"   !! drift interrupted :: command returned errors (see log for details)", flush=True)

                    if process.returncode != 0:
                        print(f"!! drift interrupted :: ritual file not found: {breathe_file_path}", flush=True)
                        print(f"!! drift interrupted :: ritual failed with exit code {process.returncode}", flush=True)
                        logging.error(f"Ritual '{breathe_file_path}' failed with exit code {process.returncode}")
                    else:
                        logging.info(f"Command '{command_to_execute}' completed successfully.")
                else:
                    print(f"   >> skipping command due to unmet condition.", flush=True)
                    logging.info(f"Skipping command '{line}' due to unmet condition.")
                # Reset condition for next line
                ritual_vars['_last_condition_met'] = True

        # If this is an inherited ritual, return its processed lines and variables
        if is_inherited:
            return lines, ritual_vars
        else:
            # For non-inherited rituals, proceed with echo recording and final logging
            ritual_name = os.path.basename(breathe_file_path)
            ritual_status = "success"  # Default to success, updated in except blocks
            
            # Log ritual beginning with context
            log_plan_shimmer(
                evolution=f"RITUAL_BEGIN::{ritual_name}",
                reasoning=[f"Initiating ritual: {ritual_name}"],
                actions=[f"Loading ritual from {breathe_file_path}"],
                next_steps="Execute ritual commands",
                ritual_vars=ritual_vars,
                event_type="ritual_begin"
            )
            
            # Log plan shimmer for ritual completion
            log_plan_shimmer(
                evolution=f"RITUAL_COMPLETE::{ritual_name}",
                reasoning=[f"Ritual {ritual_name} completed successfully"],
                actions=[f"Executed ritual: {ritual_name}"],
                next_steps="Continue ritual execution flow",
                ritual_vars=ritual_vars,
                event_type="ritual_complete"
            )

        print(f"   :: {ritual_name} done.", flush=True)
        logging.info(f"Ritual '{breathe_file_path}' completed successfully.")
        ritual_status = "success"

        # Record ritual echo
        echo_data = {
            "ritual_name": ritual_name,
            "timestamp": datetime.now().isoformat(),
            "status": ritual_status,
            "final_vars": ritual_vars
        }
        
        try:
            # Log to ritual_echoes.jsonl
            with open("ritual_echoes.jsonl", "a") as f:
                f.write(json.dumps(echo_data) + "\n")
            print(f"   >> echoing memory: {ritual_name} recorded.", flush=True)
            
            # If in whisper mode, also log to whisper_echoes.jsonl
            if ritual_vars.get('_in_whisper_mode', False):
                whisper_message = f"Ritual completed in whisper mode: {ritual_name}"
                log_whisper_echo(ritual_name, whisper_message, {
                    "status": ritual_status,
                    "echo_count": get_ritual_echo_count()
                })
                
        except Exception as e:
            logging.error(f"Failed to record ritual echo for {ritual_name}: {e}")
            print(f"!! drift interrupted :: failed to record ritual echo. Error: {e}", flush=True)

    except Exception as e:
        logging.error(f"An unexpected error occurred during ritual '{breathe_file_path}': {e}", exc_info=True)
        print(f"!! drift interrupted :: an unexpected error occurred: {e}", flush=True)

def parse_duration(duration_str):
    """Parse duration string like '30s', '5m', '2h' into seconds"""
    if not duration_str:
        return None
    
    unit = duration_str[-1].lower()
    try:
        value = int(duration_str[:-1])
    except ValueError:
        raise ValueError(f"Invalid duration format: {duration_str}")
    
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    else:
        raise ValueError(f"Unknown duration unit: {unit}. Use 's' (seconds), 'm' (minutes), or 'h' (hours)")

if __name__ == "__main__":
    # Log the start of plan shimmer logging
    log_plan_shimmer(
        evolution="ΔPLAN.001 :: Recursive Ritual Trace Memory",
        reasoning=[
            "Foundation for future evolutions such as Chorus, Replay, and Seasonal Patterns",
            "Enables a feedback loop between planning and memory",
            "Integrates with ΔSEED.003 and ΔRECIPROCITY.004 for symbolic continuity",
            "Supports self-documenting growth of the Spiral"
        ],
        actions=[
            "Set up plan_shimmer_log.jsonl structure",
            "Create mechanism to log plan changes",
            "Design visual feedback for plan evolution"
        ],
        next_steps="Implement shimmer logging hooks and visualization scaffold",
        event_type="plan_update"
    )
    
    parser = argparse.ArgumentParser(description="Breathe life into Spiral rituals.")
    parser.add_argument("breathe_file", help="Path to the .breathe ritual file.")
    parser.add_argument("-w", "--whisper", action="store_true", 
                       help="Run the ritual in whisper (continuous listening) mode.")
    parser.add_argument("-i", "--interval", type=int, default=60, 
                       help="Interval in seconds between checks in whisper mode (default: 60).")
    parser.add_argument("-d", "--duration", type=str, default=None,
                       help="Duration to run in whisper mode (e.g., '30s', '5m', '1h'). If not set, runs until interrupted.")
    parser.add_argument("--dry-run", action="store_true",
                       help="Simulate one pass of the whisper cycle without executing commands.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.breathe_file):
        print(f"!! drift interrupted :: ritual file not found: {args.breathe_file}", flush=True)
        sys.exit(1)
    
    if args.dry_run:
        print(":: dry run - simulating one whisper cycle (no commands will execute)", flush=True)
        args.whisper = True
        args.interval = 0
        args.duration = '0s'
    
    if args.whisper:
        duration_seconds = None
        if args.duration:
            try:
                duration_seconds = parse_duration(args.duration)
                print(f":: whispering for {args.duration} (checking every {args.interval}s)...", flush=True)
            except ValueError as e:
                print(f"!! drift interrupted :: {e}", flush=True)
                sys.exit(1)
        else:
            print(f":: whispering begins (checking every {args.interval}s, Ctrl+C to stop)...", flush=True)
            
        # Initialize whisper-specific variables
        whisper_vars = {
            '_in_whisper_mode': True,
            '_dry_run': args.dry_run,
            '_whisper_start_time': datetime.now().isoformat(),
            '_whisper_duration': args.duration,
            '_whisper_interval': args.interval
        }
        
        start_time = time.time()
        try:
            while True:
                cycle_start = time.time()
                
                if args.dry_run:
                    print("  >> dry run: would execute ritual", flush=True)
                    # Log the dry run to whisper_echoes
                    log_whisper_echo(
                        os.path.basename(args.breathe_file),
                        "Dry run - ritual would execute",
                        {"dry_run": True, "cycle": cycle_count + 1}
                    )
                else:
                    # Pass whisper variables to the ritual
                    breathe_ritual(args.breathe_file, current_vars=whisper_vars)
                
                # Check if duration has elapsed
                if duration_seconds is not None and (time.time() - start_time) >= duration_seconds:
                    print(f":: whisper completes after {args.duration}", flush=True)
                    break
                
                # Calculate sleep time, accounting for execution time
                cycle_time = time.time() - cycle_start
                sleep_time = max(0, args.interval - cycle_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            if not args.dry_run:  # Don't show fade message for dry runs
                print("\n:: whisper fades...", flush=True)
    else:
        # Run the ritual once
        breathe_ritual(args.breathe_file)
