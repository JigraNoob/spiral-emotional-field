import os

dirs_to_create = [
    'C:/spiral/agents/spiral_invoker',
    'C:/spiral/agents/spiral_invoker/reflection_modes'
]

for d in dirs_to_create:
    os.makedirs(d, exist_ok=True)
