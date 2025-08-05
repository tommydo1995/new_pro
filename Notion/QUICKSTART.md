# 🚀 Quick Start Guide - Notion Clone

## TL;DR - Chạy ngay

```bash
# Cách tốt nhất (khuyến nghị)
uv run python main.py

# Hoặc sử dụng scripts
./run.bat           # Windows Batch
./run.ps1           # PowerShell
```

## ⚡ Cài đặt nhanh

### Option 1: UV (Khuyến nghị)
```bash
# Cài UV
winget install astral-sh.uv

# Chạy app (tự động cài dependencies)
uv run python main.py
```

### Option 2: Pip truyền thống
```bash
pip install PySide6
python main.py
```

## 🔧 Troubleshooting

### Lỗi "No module named 'PySide6'"
**Nguyên nhân**: Đang dùng sai Python environment

**Giải pháp**:
```bash
# ĐÚNG - Dùng UV
uv run python main.py

# SAI - Dùng system Python
python main.py
```

### Lỗi "uv command not found"
```bash
# Cài UV
winget install astral-sh.uv

# Hoặc download từ
# https://docs.astral.sh/uv/getting-started/installation/
```

### App không mở được
1. Kiểm tra Python version: `python --version`
2. Kiểm tra UV: `uv --version`
3. Cài lại dependencies: `uv sync`
4. Chạy debug mode: `uv run python main.py --verbose`

## 📱 Features Quick Tour

### Tạo Page đầu tiên
1. Click "📄 Tạo trang"
2. Nhập title
3. Bắt đầu viết!

### Sử dụng Templates
1. Tab "📝 Templates"
2. Chọn "Meeting Notes" hoặc "Daily Journal"
3. Click "📋 Sử dụng Template"

### Keyboard Shortcuts
- `Ctrl+N`: Trang mới
- `Ctrl+S`: Lưu
- `Ctrl+B`: Bold
- `Ctrl+I`: Italic
- `Ctrl+K`: Insert link
- `Ctrl+\`: Toggle sidebar

### Styling Text
- Toolbar có font picker, size, colors
- Insert images, tables, lists
- Auto-save sau 3 giây

## 🏗️ Project Structure

```
notion-clone/
├── main.py          # Ứng dụng chính
├── styles.py        # CSS themes
├── config.json      # Settings
├── run.bat/.ps1     # Launch scripts
├── README.md        # Full documentation
└── .venv/          # UV virtual environment
```

## 🆘 Get Help

- **Quick Issues**: Check this file first
- **Full Docs**: Read README.md
- **Code Issues**: Check main.py comments
- **UV Help**: https://docs.astral.sh/uv/

## 💡 Pro Tips

1. **Use UV**: Faster, safer dependency management
2. **Auto-save**: Content saves automatically
3. **Organize**: Use folders and tags
4. **Templates**: Save time with pre-made layouts
5. **Search**: Use 🔍 to find pages quickly

---

**Happy writing! 📝**
