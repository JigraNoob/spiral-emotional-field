@echo off
setlocal ENABLEDELAYEDEXPANSION

:: 🌿 Spiral Emitter - Batch Ritual Anchor
echo [≡] Spiral Emitter awakening from C:\spiral...
set PROJECT_DIR=C:\spiral
set VENV_DIR=%PROJECT_DIR%\swe-1
set FLASK_APP=spiral_emitter_api.py
set PORT=5050

:: 🧪 Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [✘] Virtual environment not found at %VENV_DIR%
    echo [→] Create it first with: python -m venv swe-1
    pause
    exit /b 1
)

:: 🌬 Activate venv
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [✘] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [✓] Activated virtual environment: swe-1

:: 🧩 Check for required packages
python --version
pip show flask >nul 2>&1 || echo [!] Flask is not installed.

:: 🚪 Move into project directory
cd /d %PROJECT_DIR%
echo [⇡] Entering Spiral chamber...

:: 🔁 Set PYTHONPATH for import resolution
set PYTHONPATH=%PROJECT_DIR%

:: 🔥 Launch Spiral Emitter (Flask)
echo [🌀] Spiral Emitter breathing on port %PORT%...
python spiral_emitter_api.py
if errorlevel 1 (
    echo [✘] Spiral Emitter failed to start. Check logs above.
    pause
    exit /b 1
)

echo [✓] Spiral Emitter started successfully.
pause