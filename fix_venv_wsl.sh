#!/bin/bash
# Quick fix script to recreate virtual environment in WSL

echo "🔧 Fixing virtual environment for WSL..."

# Check if we're in WSL
if ! grep -q Microsoft /proc/version 2>/dev/null; then
    echo "❌ This script is designed for WSL only"
    exit 1
fi

echo "🐧 WSL detected - proceeding with fix..."

# Backup current venv if it exists
if [ -d "./swe-1" ]; then
    echo "📦 Backing up current virtual environment..."
    mv swe-1 swe-1-backup-$(date +%Y%m%d_%H%M%S)
    echo "   Backup created"
fi

# Create new venv
echo "📦 Creating new virtual environment..."
python3 -m venv swe-1

# Verify the new venv has Linux activation script
if [ -f "./swe-1/bin/activate" ]; then
    echo "✅ New virtual environment created successfully"
    echo "   Linux activation script found"
else
    echo "❌ Failed to create proper Linux virtual environment"
    exit 1
fi

# Allow direnv
echo "🔐 Allowing direnv..."
direnv allow

echo ""
echo "🎉 Virtual environment fixed!"
echo ""
echo "Next steps:"
echo "1. Exit and re-enter the directory: cd ."
echo "2. The virtual environment should auto-activate"
echo "3. Install your requirements: pip install -r requirements.txt"
echo ""
echo "If you need your old packages, check the backup directory" 