# 🚀 Python Notion Clone

Ứng dụng clone Notion được xây dựng bằng Python và PySide6, cung cấp đầy đủ tính năng quản lý ghi chú, templates, và tổ chức nội dung chuyên nghiệp.

## ✨ Tính năng chính

### 📝 Rich Text Editor
- Định dạng văn bản đầy đủ (Bold, Italic, Underline)
- Font family & size controls
- Text & background colors
- Bullet lists & numbered lists
- Insert tables, images, links

### 📋 Page Management
- Tạo và quản lý pages/folders
- Hierarchical organization (parent-child structure)
- Context menu với rename, delete, duplicate
- Drag & drop để sắp xếp
- Favorite pages system
- Tags cho cross-reference

### 🔍 Search & Navigation
- Advanced search trong title và content
- Keyboard shortcuts đầy đủ
- Recent pages với quick access
- Real-time filtering

### � Template System
- **Meeting Notes**: Template cho ghi chú họp
- **Daily Journal**: Template nhật ký cá nhân  
- **Project Plan**: Template kế hoạch dự án
- Auto-replace placeholders: `{date}`, `{time}`, `{datetime}`
- Tạo page mới trực tiếp từ template

### � Auto-Save & Data Management
- Auto-save thông minh sau 2 giây
- SQLite database với migration tự động
- Export pages ra HTML/PDF/TXT
- Backup & restore capabilities

### 🎨 Giao diện người dùng
- Modern UI với Material Design
- Dark mode support
- Responsive design
- Customizable layout

### ⌨️ Keyboard Shortcuts
- `Ctrl+N`: Tạo page mới
- `Ctrl+S`: Lưu page
- `Ctrl+O`: Mở file
- `Ctrl+K`: Chèn link
- `Ctrl+\\`: Toggle sidebar
- `Ctrl+Z/Y`: Undo/Redo

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- PySide6
- SQLite3 (built-in)

### Cài đặt dependencies
```bash
# Sử dụng uv (khuyến nghị)
uv add PySide6

# Hoặc sử dụng pip
pip install PySide6
```

### Chạy ứng dụng
```bash
# Với uv
uv run python main.py

# Với python thông thường
python main.py
```

## Cấu trúc dự án

```
notion-clone/
├── main.py              # File chính của ứng dụng
├── styles.py            # CSS styles và themes
├── notion_clone.db      # SQLite database (tự động tạo)
├── pyproject.toml       # UV project configuration
├── README.md            # Tài liệu này
└── assets/              # Icons và resources (optional)
```

## Cấu trúc Database

### Bảng `pages`
- `id`: Primary key
- `title`: Tiêu đề page
- `content`: Nội dung HTML
- `created_at`: Ngày tạo
- `updated_at`: Ngày cập nhật
- `parent_id`: ID của parent page/folder
- `icon`: Emoji icon
- `cover_image`: Đường dẫn ảnh cover
- `is_favorite`: Đánh dấu yêu thích
- `is_template`: Đánh dấu template
- `tags`: Tags (phân cách bằng dấu phẩy)

### Bảng `blocks` (cho tương lai)
- Hỗ trợ block-based content như Notion thật

### Bảng `templates`
- Lưu trữ các templates có sẵn

## Sử dụng

### Tạo Page mới
1. Click nút "📄 Tạo trang" hoặc Ctrl+N
2. Nhập tiêu đề
3. Page sẽ được tạo và tự động mở

### Tạo Folder
1. Click nút "📁 Tạo folder"
2. Nhập tên folder
3. Có thể kéo thả pages vào folder

### Sử dụng Templates
1. Chuyển sang tab "📝 Templates"
2. Chọn template
3. Click "📋 Sử dụng Template"

### Định dạng văn bản
- Sử dụng toolbar để định dạng
- Chọn font, size, color
- Thêm lists, tables, images

### Export/Import
- File → Export để xuất page
- File → Open để import file
- Hỗ trợ HTML, TXT formats

## Tính năng nâng cao

### Auto-save
- Tự động lưu sau 3 giây không activity
- Hiển thị trạng thái lưu ở status bar

### Search & Filter
- Tìm kiếm realtime trong danh sách pages
- Filter theo tags, favorites

### Recent Pages
- Tab "🕒 Recent" hiển thị pages gần đây
- Nhanh chóng truy cập pages đã làm việc

## Customization

### Themes
Chỉnh sửa file `styles.py` để tùy chỉnh:
- Colors
- Fonts  
- Layout
- Dark/Light mode

### Database
Có thể mở rộng database schema để thêm:
- Sharing & Collaboration
- Comments
- Version history
- File attachments

## Troubleshooting

### ❌ Lỗi "ModuleNotFoundError: No module named 'PySide6'"

**Nguyên nhân phổ biến**: Đang sử dụng sai Python environment

**Giải pháp**:
```bash
# ✅ ĐÚNG - Sử dụng UV environment
uv run python main.py

# ❌ SAI - Sử dụng system Python  
python main.py
```

**Kiểm tra environment**:
```bash
# Kiểm tra UV Python version
uv run python --version

# Kiểm tra PySide6 trong UV
uv run python -c "import PySide6; print('OK')"

# Sync dependencies nếu cần
uv sync
```

### 🔧 Cài đặt lại từ đầu
```bash
# Xóa environment cũ
rm -rf .venv

# Cài đặt lại
uv add PySide6

# Chạy app
uv run python main.py
```

### Lỗi Import PySide6
```bash
# Cài đặt lại PySide6
uv add PySide6
# hoặc
pip install --upgrade PySide6
```

### Database locked
- Đóng tất cả instances của app
- Restart app

### Performance issues
- Limit content size trong pages
- Sử dụng pagination cho large datasets

## Roadmap

### Version 2.1
- [ ] Block-based editor
- [ ] Real-time collaboration
- [ ] Plugin system
- [ ] Web interface

### Version 2.2
- [ ] Mobile app
- [ ] Cloud sync
- [ ] Advanced search
- [ ] AI integration

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

Nếu gặp vấn đề hoặc có đề xuất:
1. Tạo issue trên GitHub
2. Email: support@notionclone.com
3. Documentation: wiki.notionclone.com

---

**Tác giả**: Notion Clone Team  
**Version**: 2.0  
**Ngày cập nhật**: 2025-01-08
