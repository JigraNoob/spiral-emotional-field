
import asyncio
import json
from pathlib import Path

import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web

from shrine_cloud_connector import initialize_cloud_connection, broadcast_to_remote_shrines

async def index(request):
    """Serve the client-side application."""
    context = {}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    return response

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)
    try:
        # Send initial state
        glint_file = Path(__file__).parent / "glint.json"
        if glint_file.exists():
            with open(glint_file, "r") as f:
                await ws.send_str(f.read())

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f"ws connection closed with exception {ws.exception()}")
    finally:
        request.app['websockets'].remove(ws)

    return ws

from shrine_cloud_connector import initialize_cloud_connection, broadcast_to_remote_shrines

async def watch_glint_file(app):
    """Watch for changes in glint.json and notify websockets."""
    glint_file = Path(__file__).parent / "glint.json"
    last_modified = -1
    while True:
        try:
            modified = glint_file.stat().st_mtime
            if modified != last_modified:
                last_modified = modified
                with open(glint_file, "r") as f:
                    content = f.read()
                    # Broadcast to local websockets
                    for ws in app['websockets']:
                        await ws.send_str(content)
                    # Broadcast to remote shrines
                    broadcast_to_remote_shrines(json.loads(content))
            await asyncio.sleep(1)
        except FileNotFoundError:
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error watching glint file: {e}")
            await asyncio.sleep(5)


async def on_startup(app):
    app['cloud_initialized'] = initialize_cloud_connection()
    asyncio.create_task(watch_glint_file(app))

app = web.Application()
app['websockets'] = set()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(Path(__file__).parent / 'templates')))
app.router.add_get('/', index)
app.router.add_get('/ws', websocket_handler)
app.router.add_static('/static/', path=str(Path(__file__).parent / 'static'), name='static')
app.on_startup.append(on_startup)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8080)
