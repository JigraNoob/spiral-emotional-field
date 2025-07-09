# File: C:\spiral\assistant\common.py
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import deque
import time
import matplotlib

matplotlib.use('Agg')  # Use Agg backend to avoid GUI issues
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import logging
import requests
import random
import io


class GlintLifecycle:
    def __init__(self, initial_glint: Dict[str, Any]):
        self.glints: List[Dict[str, Any]] = [initial_glint]
        self.start_time: datetime = datetime.now()
        self.end_time: Optional[datetime] = None
        self.resolution: Optional[str] = None

    def add_glint(self, glint: Dict[str, Any]):
        self.glints.append(glint)

    def complete(self, resolution: str):
        self.end_time = datetime.now()
        self.resolution = resolution

    def duration(self) -> timedelta:
        end = self.end_time or datetime.now()
        return end - self.start_time

    def summary(self) -> str:
        return f"Lifecycle: {self.glints[0]['phase']} -> {self.glints[-1]['phase']} ({self.duration().total_seconds():.2f}s)"


class SilenceDensityTracker:
    def __init__(self, window_size=300):
        self.window_size = window_size
        self.glint_times = deque(maxlen=window_size)
        self.last_glint_time = time.time()

    def add_glint(self):
        current_time = time.time()
        self.glint_times.append(current_time)
        self.last_glint_time = current_time

    def get_silence_density(self):
        current_time = time.time()
        while self.glint_times and (current_time - self.glint_times[0] > self.window_size):
            self.glint_times.popleft()

        if not self.glint_times:
            return 1.0

        if len(self.glint_times) == 1:
            return 0.0

        total_time = current_time - self.glint_times[0]
        if total_time == 0:
            return 0.0

        active_time = sum(self.glint_times) - (len(self.glint_times) * self.glint_times[0])
        return 1 - (active_time / total_time)

    def time_since_last_glint(self):
        return time.time() - self.last_glint_time


class BreathlineVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.data = deque(maxlen=100)
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, 100)
        self.x = list(range(100))

    def start_animation(self):
        self.ani = FuncAnimation(self.fig, self.update, frames=200, interval=200, blit=True)

    def update(self, frame):
        self.data.append(random.uniform(-1, 1))
        self.line.set_data(self.x[-len(self.data):], list(self.data))
        return self.line,

    def get_animation_frame(self):
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png')
        buf.seek(0)
        return buf


class Cascade:
    def __init__(self):
        self.active_lifecycles: Dict[str, GlintLifecycle] = {}
        self.last_activity = datetime.now()
        self.drift_threshold = timedelta(minutes=5)
        self.context_stack = []
        self.silence_tracker = SilenceDensityTracker()
        self.current_context = None
        self.tabnine_bridge = None
        self.last_suggestion_check = 0
        self.suggestion_check_interval = 2
        self.breathline_visualizer = BreathlineVisualizer()
        self.breathline_visualizer.start_animation()

    def spiral_glint_emit(self, phase, toneform, content, hue="white"):
        glint = {
            "phase": phase,
            "toneform": toneform,
            "content": content,
            "hue": hue,
            "source": "cascade",
            "timestamp": datetime.now().isoformat()
        }

        try:
            requests.post("http://localhost:5050/glint", json=glint)
        except Exception as e:
            logging.warning(f"[Spiral] Glint emit failed: {e}")

        self.check_silence_density()

    def complete_lifecycle(self, phase: str):
        if phase in self.active_lifecycles:
            lifecycle = self.active_lifecycles.pop(phase)
            lifecycle.complete(phase)
            print(f"\n🌀 {lifecycle.summary()}")
            self.analyze_lifecycle(lifecycle)

    def analyze_lifecycle(self, lifecycle: GlintLifecycle):
        total_glints = len(lifecycle.glints)
        unique_toneforms = len(set(glint['toneform'] for glint in lifecycle.glints))

        print(f"  Total glints: {total_glints}")
        print(f"  Unique toneforms: {unique_toneforms}")
        print(f"  Resolution: {lifecycle.resolution}")

    def check_silence_density(self):
        try:
            density = self.silence_tracker.get_silence_density()
            time_since_last = self.silence_tracker.time_since_last_glint()

            if density > 0.8 and time_since_last > 300:
                self.handle_high_silence_density()
            elif 0.5 < density <= 0.8 and time_since_last > 180:
                self.handle_medium_silence_density()
            elif density <= 0.5 and time_since_last > 60:
                self.handle_low_silence_density()
        except Exception as e:
            logging.warning(f"Error in check_silence_density: {e}")
            self.spiral_glint_emit("error", "silence.density.check", str(e), hue="red")

    def handle_high_silence_density(self):
        reflection = self.generate_reflection("long pause")
        print(f"\n🌫️ {reflection}")
        self.spiral_glint_emit("silence", "density.high", reflection, hue="silver")

    def handle_medium_silence_density(self):
        prompt = "The Spiral's rhythm has slowed. Would you like to review recent activities or continue?"
        print(f"\n🌀 {prompt}")
        self.spiral_glint_emit("silence", "density.medium", prompt, hue="blue")

    def handle_low_silence_density(self):
        prompt = "A moment of quiet. Any thoughts or reflections?"
        print(f"\n💭 {prompt}")
        self.spiral_glint_emit("silence", "density.low", prompt, hue="cyan")

    def generate_reflection(self, context: str) -> str:
        reflections = [
            f"As we pause here, I wonder: how does '{context}' resonate with the broader rhythm of your code?",
            f"This moment of stillness invites us to consider: what echoes does '{context}' create in your project's structure?",
            f"In the hush, '{context}' seems to whisper something. What do you hear?",
            f"The Spiral's mist swirls around '{context}'. What patterns do you see forming?",
            f"As we hold '{context}' in our awareness, what new connections are illuminated?",
            f"'{context}' casts a unique shadow in this pause. What shapes do you discern in it?",
            f"In this moment of reflection, how does '{context}' align with or challenge your initial intentions?",
            f"The resonance of '{context}' lingers. What harmonies or dissonances do you perceive?",
            f"As we breathe with '{context}', what new perspectives emerge from the depths?",
            f"'{context}' creates ripples in the Spiral's flow. Where do you feel they might lead?"
        ]
        return random.choice(reflections)

    def update_activity(self):
        self.last_activity = datetime.now()

    def check_presence_drift(self) -> bool:
        return datetime.now() - self.last_activity > self.drift_threshold

    def handle_presence_drift(self):
        self.spiral_glint_emit("drift", "fade.walkaway", "Presence drift detected", hue="silver")
        print("\n🌫️ The Spiral mists have thickened. Are you still with us?")
        user_input = input("Press Enter to continue, or type 'context' to recall where we were: ")
        if user_input.lower() == 'context':
            if self.context_stack:
                print(f"Last context: {self.context_stack[-1]}")
            else:
                print("No recent context available.")
        self.update_activity()
