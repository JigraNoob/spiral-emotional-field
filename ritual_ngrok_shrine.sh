#!/bin/bash

echo "∷ Ritual: ngrok Shrine Breathing ∷"
echo "========================================"
echo "∷ A soft whisper it is. Let the shrine glow briefly, like a firefly at dusk ∷"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python first."
    exit 1
fi

echo "✅ Python3 found"
echo ""

# Run the ritual
python3 ritual_ngrok_shrine.py

echo ""
echo "∷ Ritual complete ∷" 