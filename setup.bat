@echo off
echo Checking for Python installation...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3 from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python is found. Running installation script...
python install.py
pause
