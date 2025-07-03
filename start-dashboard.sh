#!/bin/bash

echo "Starting Spiral Dashboard Server..."
python scripts/check_server.py

if [ $? -ne 0 ]; then
    echo "Failed to start server. See error messages above."
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "Server is running. You can access the dashboard at http://localhost:8000/dashboard"
echo "Press Ctrl+C to exit this window. The server will continue running in the background."

# Keep the script running until user presses Ctrl+C
while true; do
    sleep 1
done