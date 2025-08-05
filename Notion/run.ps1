#!/usr/bin/env pwsh

# Notion Clone Launcher Script
# PowerShell version for better Windows integration

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   NOTION CLONE - PROFESSIONAL EDITION" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Check if UV is available
if (Test-Command "uv") {
    Write-Host "✓ UV package manager detected" -ForegroundColor Green
    Write-Host "Checking project dependencies..." -ForegroundColor Yellow
    
    # Sync dependencies silently
    $syncResult = uv sync 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies up to date" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 Launching Notion Clone..." -ForegroundColor Magenta
        Write-Host ""
        
        # Run the application
        uv run python main.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Application started successfully!" -ForegroundColor Green
        }
        else {
            Write-Host ""
            Write-Host "❌ Application failed to start" -ForegroundColor Red
            Write-Host "Exit code: $LASTEXITCODE" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "⚠ Dependency sync failed, trying anyway..." -ForegroundColor Yellow
        uv run python main.py
    }
}
elseif (Test-Command "python") {
    Write-Host "⚠ UV not found, falling back to system Python" -ForegroundColor Yellow
    Write-Host "Recommendation: Install UV for better dependency management" -ForegroundColor Yellow
    Write-Host "Install command: winget install astral-sh.uv" -ForegroundColor Cyan
    Write-Host ""
    
    # Check if PySide6 is available
    $checkPySide = python -c "import PySide6; print('PySide6 OK')" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PySide6 detected" -ForegroundColor Green
        Write-Host "🚀 Launching Notion Clone..." -ForegroundColor Magenta
        python main.py
    }
    else {
        Write-Host "❌ PySide6 not found" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install PySide6:" -ForegroundColor Yellow
        Write-Host "  pip install PySide6" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}
else {
    Write-Host "❌ No Python interpreter found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://python.org" -ForegroundColor Cyan
    Write-Host "  2. Or install via winget: winget install Python.Python.3.12" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Error handling
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "   ERROR: Application failed to start" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Install UV: winget install astral-sh.uv" -ForegroundColor Cyan
    Write-Host "2. Install dependencies: uv add PySide6" -ForegroundColor Cyan
    Write-Host "3. Alternative: pip install PySide6" -ForegroundColor Cyan
    Write-Host "4. Check Python version: python --version" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "For help, visit: https://github.com/your-repo/notion-clone" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
}
else {
    Write-Host ""
    Write-Host "Thank you for using Notion Clone!" -ForegroundColor Green
    Write-Host "Application closed normally." -ForegroundColor Gray
}
