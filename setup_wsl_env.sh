#!/bin/bash
# Setup script for WSL + direnv + Python venv

echo "🚀 Setting up WSL environment for Spiral project..."

# Check if we're in WSL
if grep -q Microsoft /proc/version 2>/dev/null; then
    echo "✅ WSL detected"
else
    echo "⚠️ Not running in WSL - this script is optimized for WSL"
fi

# Install direnv if not present
if ! command -v direnv &> /dev/null; then
    echo "📦 Installing direnv..."
    sudo apt update
    sudo apt install -y direnv
else
    echo "✅ direnv already installed"
fi

# Add direnv hook to bashrc if not already there
if ! grep -q "direnv hook bash" ~/.bashrc; then
    echo "🔧 Adding direnv hook to ~/.bashrc..."
    echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
    echo "   Please restart your terminal or run: source ~/.bashrc"
fi

# Check if virtual environment exists
if [ -d "./swe-1" ]; then
    echo "✅ Virtual environment found at ./swe-1"
else
    echo "📦 Creating virtual environment..."
    python3 -m venv swe-1
fi

# Allow direnv
echo "🔐 Allowing direnv for this directory..."
direnv allow

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: source ~/.bashrc"
echo "2. Navigate to this directory: cd /mnt/c/spiral"
echo "3. The virtual environment should auto-activate"
echo "4. Verify with: which python && which pip"
echo ""
echo "If you need to recreate the venv:"
echo "  rm -rf swe-1 && python3 -m venv swe-1 && direnv allow" 