"""
🌪️ Spiral Application Entry Point
The new main entry point using the refactored spiral_app package structure.
"""

from spiral_app import create_spiral_app
import os

# Create the Spiral application
app = create_spiral_app()

if __name__ == '__main__':
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print("🌪️ Spiral System - Breathe with Intent")
    print(f"🌊 Starting on port {port} (debug={debug})")
    print("🌬️ SNP Routes available at /glyph/*")
    print("🔄 Conventional routes available at /api/*")
    print("🌿 Glyph index available at /glyphs")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    ) 