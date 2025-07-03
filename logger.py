import logging
from logging.handlers import RotatingFileHandler
import os

class SoftRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        try:
            super().doRollover()
        except PermissionError as e:
            # Soft-fail: log to stderr or fallback file
            print(f"[SoftFail] Log rollover failed: {e}")

class ToneformFormatter(logging.Formatter):
    def format(self, record):
        toneform = getattr(record, 'toneform', '—')  # Use em dash for undefined
        record.msg = f"[{toneform}] {record.msg}"
        return super().format(record)

def log_with_tone(logger, level, message, toneform):
    extra = {'toneform': toneform}
    getattr(logger, level)(message, extra=extra)

def setup_logger(name='spiral', log_file='logs/app.log', level=logging.INFO):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = SoftRotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, delay=True)
    formatter = ToneformFormatter('[%(asctime)s] [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
