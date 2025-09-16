@echo off
REM Microsearch Driver Capture - Windows Launcher
REM Simple batch file to run the Python launcher

echo Microsearch Driver Capture - Windows Launcher
echo ============================================

REM Check if Python is available
REM First try the specific Python path
set PYTHON_PATH=C:\Users\oscarchatwin\AppData\Local\Programs\Python\Python313
if exist "%PYTHON_PATH%\python.exe" (
    set PYTHON_CMD="%PYTHON_PATH%\python.exe"
    echo Using Python from: %PYTHON_PATH%
    goto :python_found
)

REM Fallback to PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Trying python3...
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python is not installed or not in PATH
        echo Please install Python 3.7+ and try again
        echo Expected location: %PYTHON_PATH%
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

:python_found

echo Using Python command: %PYTHON_CMD%
echo.

REM Run the Python launcher
%PYTHON_CMD% launch.py %*

pause
