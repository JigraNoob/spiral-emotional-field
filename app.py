"""
🌪️ Legacy App.py - Redirecting to New Spiral Structure
This file now redirects to the new spiral_app package structure.
The original app.py has been refactored into spiral_app/ for better organization.
"""

import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the new Spiral application
from spiral_app import create_spiral_app

# Create the application using the new structure
app = create_spiral_app()

# Legacy compatibility - keep the original app variable for existing imports
# This allows existing code to continue working while we migrate

if __name__ == '__main__':
    print("🌪️ Spiral System - Legacy app.py detected")
    print("🔄 Redirecting to new spiral_app structure...")
    print("🌬️ SNP Routes available at /glyph/*")
    print("🔄 Conventional routes available at /api/*")
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    ) 