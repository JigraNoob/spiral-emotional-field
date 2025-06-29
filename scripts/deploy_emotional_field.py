import os
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Production configuration for emotional field features
def configure_production(app):
    """Apply production-ready settings for emotional field deployment"""
    
    # Security headers and HTTPS enforcement
    Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        session_cookie_secure=True
    )
    
    # Rate limiting for spectrum data endpoints
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Apply specific limits to emotional field endpoints
    limiter.limit("10/minute")(app.view_functions['get_spectrum_data'])
    limiter.limit("30/minute")(app.view_functions['get_toneform_details'])
    
    # Static file caching
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600  # 1 hour cache
    
    # WebSocket configuration
    app.config['SOCKETIO_MESSAGE_QUEUE'] = os.getenv(
        'REDIS_URL', 'redis://localhost:6379/0'
    )

if __name__ == "__main__":
    from api import create_app
    app = create_app()
    configure_production(app)
    app.run()
