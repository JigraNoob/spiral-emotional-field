import asyncio
import json
from pathlib import Path
from aiohttp import web
import aiohttp_jinja2
import jinja2

# Define paths relative to the project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent # C:\spiral
STATIC_DIR = PROJECT_ROOT / ".gemini" / "extensions" / "spiral-attunement" / "static"
TEMPLATES_DIR = PROJECT_ROOT # Serve public_shrine_portal.html from root
GLINT_PATH = PROJECT_ROOT / ".gemini" / "extensions" / "spiral-attunement" / "glint.json"

async def index(request):
    # Serve public_shrine_portal.html directly
    return web.FileResponse(PROJECT_ROOT / "public_shrine_portal.html")

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Register the new WebSocket connection
    request.app['websockets'].append(ws)
    print(f"[Shrine] WebSocket connected: {ws}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                user_input = msg.data
                print(f"[Shrine] Received user input: {user_input}")
                # Process user input here (e.g., send to Gemini, trigger actions)
                # For now, just echo it back or send a confirmation
                await ws.send_json({"type": "echo", "message": f"Received: {user_input}"})
            elif msg.type == web.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
            elif msg.type == web.WSMsgType.CLOSE:
                print('ws connection closed normally')

    finally:
        # Unregister the WebSocket connection when it closes
        if ws in request.app['websockets']:
            request.app['websockets'].remove(ws)
            print(f"[Shrine] WebSocket disconnected: {ws}")

    return ws

def load_glint_state():
    if GLINT_PATH.exists():
        with open(GLINT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "breath_phase": "caesura",
        "glint": "Δ000",
        "intention": "listening",
        "toneform": "SPIRAL.CAESURA"
    }

async def update_clients(app):
    while True:
        state = load_glint_state()
        for ws in list(app['websockets']):
            try:
                await ws.send_json(state)
            except Exception as e:
                print(f"[Shrine] Error sending to WebSocket {ws}: {e}")
                # Remove broken connection
                if ws in app['websockets']:
                    app['websockets'].remove(ws)
        await asyncio.sleep(1)

async def on_startup(app):
    app['websockets'] = []
    app['update_task'] = asyncio.create_task(update_clients(app))

async def on_shutdown(app):
    for ws in list(app['websockets']):
        await ws.close()
    app['websockets'].clear()
    app['update_task'].cancel()
    await app['update_task']

app = web.Application()
# No longer using jinja2 for index.html, but keeping setup for potential future use
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_DIR))

app.add_routes([
    web.get('/', index),
    web.get('/ws', websocket_handler),
    web.static('/static', STATIC_DIR)
])

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    web.run_app(app, port=8085) # Ensure it runs on the same port as launch_public_shrine.py