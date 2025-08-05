#!/usr/bin/env python3
"""
Smart Launcher for Notion Clone
Automatically detects and uses the correct Python environment
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, "", str(e)

def check_command_exists(cmd):
    """Check if a command exists in PATH."""
    success, _, _ = run_command(f"{'where' if platform.system() == 'Windows' else 'which'} {cmd}", check=False)
    return success

def print_status(message, status="info"):
    """Print colored status messages."""
    colors = {
        "info": "\033[94m",      # Blue
        "success": "\033[92m",   # Green
        "warning": "\033[93m",   # Yellow
        "error": "\033[91m",     # Red
        "reset": "\033[0m"       # Reset
    }
    
    symbols = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    color = colors.get(status, colors["info"])
    symbol = symbols.get(status, "")
    reset = colors["reset"]
    
    print(f"{color}{symbol} {message}{reset}")

def main():
    print("=" * 50)
    print("🚀 NOTION CLONE - SMART LAUNCHER")
    print("=" * 50)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print_status("main.py not found! Please run from the project directory.", "error")
        return 1
    
    # Method 1: Try UV (recommended)
    if check_command_exists("uv"):
        print_status("UV detected - using UV environment", "success")
        
        # Check if pyproject.toml exists
        if os.path.exists("pyproject.toml"):
            print_status("Syncing dependencies...", "info")
            success, _, error = run_command("uv sync", check=False)
            if not success:
                print_status(f"UV sync failed: {error}", "warning")
        
        # Try to run with UV
        print_status("Launching with UV...", "info")
        success, output, error = run_command("uv run python main.py", check=False)
        
        if success:
            print_status("Application started successfully!", "success")
            return 0
        else:
            print_status(f"UV run failed: {error}", "error")
            print_status("Falling back to system Python...", "warning")
    
    # Method 2: Try system Python with virtual environment
    if os.path.exists(".venv"):
        print_status("Virtual environment detected", "info")
        
        if platform.system() == "Windows":
            activate_script = ".venv\\Scripts\\activate.bat"
            python_exe = ".venv\\Scripts\\python.exe"
        else:
            activate_script = ".venv/bin/activate"
            python_exe = ".venv/bin/python"
        
        if os.path.exists(python_exe):
            print_status("Using virtual environment Python", "success")
            success, output, error = run_command(f"{python_exe} main.py", check=False)
            
            if success:
                print_status("Application started successfully!", "success")
                return 0
            else:
                print_status(f"Virtual env failed: {error}", "error")
    
    # Method 3: Try system Python
    if check_command_exists("python"):
        print_status("Trying system Python...", "warning")
        
        # Check if PySide6 is available
        success, _, _ = run_command('python -c "import PySide6"', check=False)
        
        if success:
            print_status("PySide6 found in system Python", "success")
            success, output, error = run_command("python main.py", check=False)
            
            if success:
                print_status("Application started successfully!", "success")
                return 0
            else:
                print_status(f"System Python failed: {error}", "error")
        else:
            print_status("PySide6 not found in system Python", "error")
    
    # Method 4: Try python3
    if check_command_exists("python3"):
        print_status("Trying python3...", "warning")
        
        # Check if PySide6 is available
        success, _, _ = run_command('python3 -c "import PySide6"', check=False)
        
        if success:
            print_status("PySide6 found in python3", "success")
            success, output, error = run_command("python3 main.py", check=False)
            
            if success:
                print_status("Application started successfully!", "success")
                return 0
            else:
                print_status(f"Python3 failed: {error}", "error")
        else:
            print_status("PySide6 not found in python3", "error")
    
    # If we get here, nothing worked
    print()
    print_status("❌ FAILED TO START APPLICATION", "error")
    print()
    print("📋 Troubleshooting steps:")
    print("1. Install UV (recommended):")
    print("   winget install astral-sh.uv")
    print()
    print("2. Install PySide6:")
    print("   uv add PySide6")
    print("   OR")
    print("   pip install PySide6")
    print()
    print("3. Check Python installation:")
    print("   python --version")
    print()
    print("4. Run manually:")
    print("   uv run python main.py")
    print()
    
    return 1

if __name__ == "__main__":
    exit_code = main()
    
    if exit_code != 0:
        input("\nPress Enter to exit...")
    
    sys.exit(exit_code)
