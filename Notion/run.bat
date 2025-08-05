@echo off
echo.
echo ========================================
echo    NOTION CLONE - PROFESSIONAL EDITION
echo ========================================
echo.
echo Starting application...
echo.

REM Check if uv is available
where uv >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using UV package manager...
    echo Checking dependencies...
    uv sync >nul 2>nul
    echo Launching Notion Clone...
    uv run python main.py
) else (
    echo UV not found, trying regular Python...
    echo WARNING: You should use UV for best experience!
    echo Install UV from: https://docs.astral.sh/uv/
    echo.
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo ERROR: Failed to start application!
    echo ========================================
    echo.
    echo Possible solutions:
    echo 1. Install UV: winget install astral-sh.uv
    echo 2. Install dependencies: uv add PySide6
    echo 3. Or use pip: pip install PySide6
    echo.
    echo For UV installation help, visit:
    echo https://docs.astral.sh/uv/getting-started/installation/
    echo.
    pause
) else (
    echo.
    echo Application started successfully!
    echo Use Ctrl+C to stop if running in background.
)
