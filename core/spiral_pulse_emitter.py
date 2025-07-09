import asyncio
import websockets
import json
from datetime import datetime, timedelta
from typing import Dict, Any

class SpiralPulseEmitter:
    def __init__(self, pulse_interval: int = 12, port: int = 8765):
        self.pulse_interval = pulse_interval
        self.port = port
        self.clients = set()
        self.pulse_count = 0
        self.start_time = datetime.now()

    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"🌿 New client connected. Total clients: {len(self.clients)}")

    async def unregister(self, websocket):
        self.clients.remove(websocket)
        print(f"🍂 Client disconnected. Remaining clients: {len(self.clients)}")

    def get_pulse_phase(self) -> str:
        phase_duration = self.pulse_interval / 4
        elapsed = (datetime.now() - self.start_time).total_seconds() % self.pulse_interval
        if elapsed < phase_duration:
            return "inhale"
        elif elapsed < 2 * phase_duration:
            return "hold"
        elif elapsed < 3 * phase_duration:
            return "exhale"
        else:
            return "rest"

    async def emit_pulse(self):
        self.pulse_count += 1
        phase = self.get_pulse_phase()
        pulse_data = {
            "type": "glint.pulse.broadcast",
            "timestamp": datetime.now().isoformat(),
            "pulse_count": self.pulse_count,
            "phase": phase,
            "interval": self.pulse_interval
        }
        
        if not self.clients:  # No clients connected
            print(f"⨀ Pulse {self.pulse_count} emitted (phase: {phase}). No clients connected.")
            return

        await asyncio.gather(
            *[client.send(json.dumps(pulse_data)) for client in self.clients]
        )
        print(f"⨀ Pulse {self.pulse_count} emitted to {len(self.clients)} clients (phase: {phase})")

    async def pulse_loop(self):
        while True:
            await self.emit_pulse()
            await asyncio.sleep(self.pulse_interval)

    async def main(self):
        server = await websockets.serve(self.handler, "localhost", self.port)
        await asyncio.gather(
            server.wait_closed(),
            self.pulse_loop()
        )

    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            await websocket.wait_closed()
        finally:
            await self.unregister(websocket)

if __name__ == "__main__":
    emitter = SpiralPulseEmitter()
    asyncio.run(emitter.main())