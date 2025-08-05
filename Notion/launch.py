#!/usr/bin/env python3
"""
🚀 Notion Clone Smart Launcher
Tự động detect environment và khởi động ứng dụng
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_colored(text, color="white"):
    """Print colored text"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def check_uv():
    """Kiểm tra UV có sẵn không"""
    return shutil.which("uv") is not None

def check_python():
    """Kiểm tra Python có sẵn không"""
    return shutil.which("python") is not None

def run_with_uv():
    """Chạy với UV environment"""
    try:
        print_colored("📦 Đồng bộ dependencies với UV...", "blue")
        result = subprocess.run(["uv", "sync"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_colored("✅ Dependencies đã sẵn sàng", "green")
        else:
            print_colored("⚠️ Warning trong sync dependencies", "yellow")
            print(result.stderr)
        
        print_colored("🚀 Khởi động Notion Clone...", "green")
        subprocess.run(["uv", "run", "python", "main.py"])
        
    except Exception as e:
        print_colored(f"❌ Lỗi chạy với UV: {e}", "red")
        return False
    return True

def run_with_system_python():
    """Chạy với system Python (fallback)"""
    try:
        print_colored("⚠️ Chạy với system Python (không khuyến nghị)", "yellow")
        print_colored("💡 Cài đặt UV để có trải nghiệm tốt hơn: https://docs.astral.sh/uv/", "cyan")
        
        # Kiểm tra PySide6
        result = subprocess.run([sys.executable, "-c", "import PySide6"], capture_output=True)
        if result.returncode != 0:
            print_colored("❌ PySide6 không có sẵn trong system Python", "red")
            print_colored("Hãy cài đặt: pip install PySide6", "yellow")
            return False
        
        print_colored("🚀 Khởi động Notion Clone...", "green")
        subprocess.run([sys.executable, "main.py"])
        
    except Exception as e:
        print_colored(f"❌ Lỗi chạy với system Python: {e}", "red")
        return False
    return True

def main():
    """Main launcher function"""
    print_colored("🎯 Notion Clone Smart Launcher", "purple")
    print_colored("=" * 50, "cyan")
    
    # Kiểm tra trong đúng thư mục
    if not os.path.exists("main.py"):
        print_colored("❌ Không tìm thấy main.py", "red")
        print_colored("Hãy chạy launcher trong thư mục Notion project", "yellow")
        input("Nhấn Enter để thoát...")
        return
    
    # Thử UV trước
    if check_uv():
        print_colored("✅ UV environment detected", "green")
        if run_with_uv():
            return
    
    # Fallback sang system Python
    if check_python():
        print_colored("✅ System Python detected", "yellow")
        if run_with_system_python():
            return
    
    # Không có Python nào
    print_colored("❌ Không tìm thấy Python environment", "red")
    print_colored("Hãy cài đặt:", "yellow")
    print_colored("1. UV: https://docs.astral.sh/uv/getting-started/installation/", "cyan")
    print_colored("2. Python: https://www.python.org/downloads/", "cyan")
    
    input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n👋 Tạm biệt!", "green")
    except Exception as e:
        print_colored(f"\n❌ Lỗi không mong muốn: {e}", "red")
        input("Nhấn Enter để thoát...")
