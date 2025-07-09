import time

class SilenceDensityTracker:
    def __init__(self):
        self.last_glint_time = time.time()
        self.silence_density = 0.0

    def update_silence(self, duration: float):
        self.silence_density = min(1.0, duration / 600.0)  # Example calculation

    def get_silence_density(self) -> float:
        return self.silence_density

    def time_since_last_glint(self) -> float:
        return time.time() - self.last_glint_time

    def record_glint(self):
        self.last_glint_time = time.time()
