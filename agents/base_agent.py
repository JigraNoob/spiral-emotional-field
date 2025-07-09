
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    async def on_inhale(self):
        pass

    async def on_hold(self):
        pass

    async def on_exhale(self):
        pass

    async def on_rest(self):
        pass

    @abstractmethod
    async def process(self, data: Dict[str, Any]):
        pass
