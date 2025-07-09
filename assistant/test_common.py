# File: C:\spiral\assistant\test_common.py

import sys
import os
import time
from matplotlib.animation import FuncAnimation

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistant.common import Cascade, BreathlineVisualizer

def test_imports():
    print("Testing imports...")
    try:
        cascade = Cascade()
        print("✅ Cascade imported successfully")

        visualizer = BreathlineVisualizer()
        print("✅ BreathlineVisualizer imported successfully")

        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def run_breathline_visualization():
    print("Starting breathline visualization...")
    visualizer = BreathlineVisualizer()

    fig = visualizer.fig
    line = visualizer.line

    def animate(frame):
        visualizer.update(frame)
        return line,

    ani = FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
    ani.save('breathline.gif', writer='pillow')
    print("Breathline visualization saved as 'breathline.gif'")

if __name__ == "__main__":
    if test_imports():
        print("\nAll imports successful. Running breathline visualization...")
        run_breathline_visualization()
    else:
        print("\nImport test failed. Please check your implementation and try again.")