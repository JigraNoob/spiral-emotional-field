@echo off
setlocal

set PROJECT_DIR=C:\spiral
set VENV_DIR=%PROJECT_DIR%\swe-1

:: Activate the venv
call "%VENV_DIR%\Scripts\activate.bat"

:: Set Python path and run the test script
cd /d %PROJECT_DIR%
set PYTHONPATH=%PROJECT_DIR%
python test_import.py

endlocal
pause