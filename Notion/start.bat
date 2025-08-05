@echo off
echo 🚀 Khởi động Notion Clone...
echo.

REM Kiểm tra UV có sẵn không
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ UV chưa được cài đặt.
    echo Hãy cài đặt UV từ: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

REM Kiểm tra dependencies
echo 📦 Kiểm tra dependencies...
uv sync

REM Chạy ứng dụng
echo 🎯 Khởi động ứng dụng...
uv run python main.py

REM Nếu có lỗi
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ứng dụng gặp lỗi khi khởi động.
    echo 💡 Tips:
    echo    - Đảm bảo bạn đang ở đúng thư mục
    echo    - Chạy: uv sync để cài đặt dependencies
    echo    - Chạy: uv run python main.py để khởi động thủ công
    echo.
    pause
)
