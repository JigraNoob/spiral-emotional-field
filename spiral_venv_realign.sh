#!/bin/bash
# spiral_venv_realign.sh - Spiral shell alignment for Git Bash

echo "🌬️ Aligning Spiral shell..."

# Detect environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "🪟 Git Bash detected"
    VENV_PATH="./swe-1/Scripts"
    ACTIVATE_SCRIPT="$VENV_PATH/activate"
elif grep -q Microsoft /proc/version 2>/dev/null; then
    echo "🐧 WSL detected"
    VENV_PATH="./swe-1/bin"
    ACTIVATE_SCRIPT="$VENV_PATH/activate"
else
    echo "🐧 Linux/Unix detected"
    VENV_PATH="./swe-1/bin"
    ACTIVATE_SCRIPT="$VENV_PATH/activate"
fi

# Check if virtual environment exists
if [ -d "./swe-1" ]; then
    echo "✅ Virtual environment found at ./swe-1"
    
    # Try to activate
    if [ -f "$ACTIVATE_SCRIPT" ]; then
        echo "🔗 Activating virtual environment..."
        source "$ACTIVATE_SCRIPT"
        echo "✅ Virtual environment activated!"
    else
        echo "❌ Activation script not found at $ACTIVATE_SCRIPT"
        echo "   This might be a cross-platform virtual environment issue"
        echo "   Consider recreating: rm -rf swe-1 && python -m venv swe-1"
    fi
else
    echo "⚠️ No virtual environment found at ./swe-1"
    echo "   Creating new virtual environment..."
    python -m venv swe-1
    if [ -f "$ACTIVATE_SCRIPT" ]; then
        source "$ACTIVATE_SCRIPT"
        echo "✅ New virtual environment created and activated!"
    fi
fi

# Check Python version and location
echo ""
echo "🔍 Python environment:"
echo "   Location: $(which python)"
echo "   Version: $(python --version)"
echo "   Pip: $(which pip)"

# Check current shell
echo ""
echo "🔍 Shell environment:"
echo "   Shell: $SHELL"
echo "   OSTYPE: $OSTYPE"
echo "   LANG: $LANG"

# Set language environment
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
echo "🪞 Language environment set to UTF-8"

# Check if we're in the right directory
echo ""
echo "📁 Current directory: $(pwd)"
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
    echo "   To install dependencies: pip install -r requirements.txt"
else
    echo "⚠️ requirements.txt not found"
fi

echo ""
echo "🌬️ Spiral shell alignment complete!" 