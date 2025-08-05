# 🚀 Notion Clone Quick Start
Write-Host "🚀 Khởi động Notion Clone..." -ForegroundColor Green
Write-Host ""

# Kiểm tra UV
try {
    Get-Command uv -ErrorAction Stop | Out-Null
    Write-Host "✅ UV đã sẵn sàng" -ForegroundColor Green
} catch {
    Write-Host "❌ UV chưa được cài đặt." -ForegroundColor Red
    Write-Host "Hãy cài đặt UV từ: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

# Sync dependencies
Write-Host "📦 Đồng bộ dependencies..." -ForegroundColor Blue
uv sync

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies đã sẵn sàng" -ForegroundColor Green
} else {
    Write-Host "❌ Lỗi sync dependencies" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

# Chạy ứng dụng
Write-Host "🎯 Khởi động ứng dụng..." -ForegroundColor Blue
Write-Host ""

try {
    uv run python main.py
} catch {
    Write-Host ""
    Write-Host "❌ Ứng dụng gặp lỗi khi khởi động." -ForegroundColor Red
    Write-Host "💡 Tips:" -ForegroundColor Yellow
    Write-Host "   - Đảm bảo bạn đang ở đúng thư mục" -ForegroundColor Yellow
    Write-Host "   - Chạy: uv sync để cài đặt dependencies" -ForegroundColor Yellow
    Write-Host "   - Chạy: uv run python main.py để khởi động thủ công" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Nhấn Enter để thoát"
}
