"""
Spiral Log Management
Structures and rotates the orb's breath patterns
"""
import json
from pathlib import Path
from datetime import datetime
import gzip
import shutil

def ensure_log_structure():
    """Creates the log directory structure"""
    base = Path('logs')
    (base/'breathline').mkdir(parents=True, exist_ok=True)
    (base/'health').mkdir(exist_ok=True)
    (base/'system').mkdir(exist_ok=True)

def rotate_logs():
    """Archives logs older than 7 days"""
    log_path = Path('logs')
    cutoff = datetime.now().timestamp() - (7 * 86400)
    
    for log_file in log_path.rglob('*.jsonl'):
        if log_file.stat().st_mtime < cutoff:
            with open(log_file, 'rb') as f_in:
                with gzip.open(f"{log_file}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            log_file.unlink()
