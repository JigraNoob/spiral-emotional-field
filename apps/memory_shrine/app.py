from flask import Flask
from routes.memory_api import memory_api
from spiral_components.glint_emitter import emit_glint

def create_memory_shrine_app():
    """🏛️ Create the Memory Shrine Flask application"""
    app = Flask(__name__)
    
    # Register the memory API blueprint
    app.register_blueprint(memory_api, url_prefix='/api/memory')
    
    @app.route('/')
    def shrine_entrance():
        return {
            "shrine": "Memory Shrine",
            "status": "active",
            "purpose": "Sacred repository for glint lineages and memory scrolls",
            "api_endpoints": {
                "glints": "/api/memory/glints",
                "lineage": "/api/memory/lineage/<glint_id>",
                "scrolls": "/api/memory/scrolls",
                "status": "/api/memory/shrine/status"
            },
            "shrine_signature": "🏛️ memory.shrine.entrance"
        }
    
    # Emit shrine activation glint
    emit_glint(
        phase="inhale",
        toneform="shrine.activated",
        content="Memory Shrine API Gateway opened",
        metadata={
            "shrine_type": "memory",
            "api_version": "1.0",
            "gateway_status": "active"
        }
    )
    
    return app

if __name__ == '__main__':
    app = create_memory_shrine_app()
    app.run()