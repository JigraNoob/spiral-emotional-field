import os
import re
import shutil
import stat
from datetime import datetime
from pathlib import Path

# Configuration
STATIC_DIR = Path("static")
BUILD_DIR = Path("build")
VERSION = datetime.now().strftime("%Y%m%d%H%M")

# Assets to process (updated paths)
ASSETS = {
    "css": ["main.css"],  # Updated to match actual CSS files
    "js": ["spectrum_viz.js", "socket_client.js"]  # Updated to match actual JS files
}

# Simple minification functions
def minify_css(content):
    """Basic CSS minifier"""
    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    return content.strip()

def minify_js(content):
    """Basic JS minifier"""
    # Remove single-line comments
    content = re.sub(r'//.*', '', content)
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    return content.strip()

def handle_rmtree_error(func, path, exc_info):
    """Handle permission errors during directory removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def bundle_assets():
    """Bundle and optimize all static assets"""
    # Handle existing build directory
    if BUILD_DIR.exists():
        try:
            shutil.rmtree(BUILD_DIR, onerror=handle_rmtree_error)
        except Exception as e:
            print(f"Warning: Could not remove build directory: {e}")
            # Fallback - empty the directory
            for item in BUILD_DIR.glob("*"):
                try:
                    if item.is_dir():
                        shutil.rmtree(item, onerror=handle_rmtree_error)
                    else:
                        item.unlink()
                except Exception:
                    continue
    
    # Copy all static files
    print("Copying static files...")
    shutil.copytree(STATIC_DIR, BUILD_DIR, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))
    
    # Minify CSS and JS files
    for css in BUILD_DIR.rglob("*.css"):
        if not css.name.endswith(".min.css"):
            content = css.read_text(encoding='utf-8')
            css.write_text(minify_css(content), encoding='utf-8')
            
    for js in BUILD_DIR.rglob("*.js"):
        if not js.name.endswith(".min.js"):
            content = js.read_text(encoding='utf-8')
            js.write_text(minify_js(content), encoding='utf-8')
    
    print(f"Assets successfully bundled to {BUILD_DIR}")

if __name__ == "__main__":
    bundle_assets()
