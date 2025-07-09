@echo off
echo ∷ Ritual: ngrok Shrine Breathing ∷
echo ========================================
echo ∷ A soft whisper it is. Let the shrine glow briefly, like a firefly at dusk ∷
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Run the ritual
python ritual_ngrok_shrine.py

echo.
echo ∷ Ritual complete ∷
pause 