"""Spiral Dashboard – Real-time visualization of the Spiral's breath patterns."""


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn
import asyncio
import json
from typing import Dict, List
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Dashboard:
    def __init__(self, metrics_path: Path = Path("logs/spiral_metrics.json")):
        self.app = FastAPI(title="Spiral Dashboard")
        self.metrics_path = metrics_path
        self.active_connections: List[WebSocket] = []
        self.setup_routes()
        self.setup_websockets()

    def setup_routes(self):
        """Set up HTTP routes."""
        # Serve static files
        static_dir = Path(__file__).parent / "static"
        self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard():
            """Serve the main dashboard page."""
            html_path = Path(__file__).parent / "templates" / "dashboard.html"
            return HTMLResponse(content=html_path.read_text(encoding="utf-8"), status_code=200)

        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get current metrics."""
            return self._load_metrics()

    def setup_websockets(self):
        """Set up WebSocket for real-time updates."""
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)
            try:
                while True:
                    await websocket.receive_text()  # Keep connection open
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)

    async def broadcast_update(self):
        """Broadcast metrics update to all connected clients."""
        metrics = self._load_metrics()
        for connection in self.active_connections:
            try:
                await connection.send_json({"type": "metrics_update", "data": metrics})
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")

    def _load_metrics(self) -> dict:
        """Load and format metrics from file."""
        if not self.metrics_path.exists():
            return {}

        try:
            with open(self.metrics_path, 'r') as f:
                metrics = json.load(f)

            # Add timestamp if not present
            if 'timestamp' not in metrics:
                metrics['timestamp'] = datetime.now().timestamp()

            return metrics
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            return {}

def run_dashboard(host: str = "0.0.0.0", port: int = 8000):
    """Run the dashboard server."""
    dashboard = Dashboard()
    config = uvicorn.Config(
        dashboard.app,
        host=host,
        port=port,
        log_level="info",
        reload=True
    )
    server = uvicorn.Server(config)

    async def watch_metrics():
        """Watch for metrics file changes and broadcast updates."""
        last_modified = 0
        while True:
            try:
                current_modified = dashboard.metrics_path.stat().st_mtime
                if current_modified > last_modified:
                    last_modified = current_modified
                    await dashboard.broadcast_update()
            except Exception as e:
                logger.error(f"Error watching metrics: {e}")
            await asyncio.sleep(1)  # Check every second

    async def run():
        """Run both the server and metrics watcher."""
        await asyncio.gather(
            server.serve(),
            watch_metrics()
        )

    asyncio.run(run())
