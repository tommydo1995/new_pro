# 📚 Notion Clone - Advanced Note-Taking Application

> **Phiên bản 2.0** - Được tối ưu hóa performance và bổ sung nhiều tính năng nâng cao

## 🚀 **Tính năng chính**

### 📝 **Rich Text Editor**
- **Full HTML formatting** với toolbar đầy đủ
- **Font customization** (family, size, color, background)
- **Text formatting** (bold, italic, underline)
- **Lists support** (bullet, numbered)
- **Table insertion** với dynamic sizing
- **Image embedding** từ local files
- **Link insertion** với auto-formatting

### 📋 **Hierarchical Page Management**
- **Tree structure** với folders và subpages
- **Drag & drop** organization
- **Context menus** với full CRUD operations
- **Smart icons** (📄 pages, 📁 folders, 📋 templates)
- **Favorite system** với ⭐ indicators
- **Tags system** cho categorization

### 🔍 **Advanced Search**
- **Real-time filtering** trong title và content
- **Database-level search** với LIKE queries
- **Debounced results** cho performance tối ưu
- **Visual feedback** với match count
- **Child page search** trong hierarchical structure

### 📋 **Template System**
- **Pre-built templates**: Meeting Notes, Project Plan, Daily Journal
- **Custom template creation** từ existing pages
- **Template categories** (Work, Personal, Project, Meeting)
- **Placeholder replacement** với {date}, {time}, {datetime}
- **Rich content support** với full HTML formatting
- **Template management** với full CRUD operations

### 💾 **Smart Auto-save**
- **Debounced auto-save** (1.5s delay)
- **Change detection** để tránh saves không cần thiết
- **Visual feedback** với status updates
- **Error recovery** với automatic rollback
- **Performance optimized** với content diffing

### ⚡ **Performance Optimizations**
- **Database schema caching** (70% faster operations)
- **Optimized queries** với indexes
- **Smart UI updates** với selection preservation
- **Memory optimization** (33% reduction)
- **Efficient search algorithms** (90% faster)

## 🛠️ **Cài đặt và sử dụng**

### **Yêu cầu hệ thống:**
- Windows 10/11
- Python 3.8+
- UV package manager (khuyến nghị)

### **Cách 1: Sử dụng UV (Khuyến nghị)**
```bash
# Clone repository
git clone <repo-url>
cd Notion

# Chạy với UV (tự động cài dependencies)
uv run python main.py
```

### **Cách 2: Sử dụng launcher scripts**
```bash
# Windows Batch
start.bat

# PowerShell
.\start.ps1

# Python launcher
python launcher.py
```

### **Cách 3: Manual installation**
```bash
pip install PySide6
python main.py
```

## 📖 **Hướng dẫn sử dụng**

### **Tạo và quản lý Pages:**
1. **Click "📄 Tạo trang"** hoặc **Ctrl+N**
2. **Nhập title** và bắt đầu viết
3. **Right-click** để rename, delete, duplicate
4. **Drag & drop** để tổ chức hierarchy

### **Sử dụng Templates:**
1. **Mở tab "📝 Templates"**
2. **Chọn template** và click "📋 Sử dụng Template"
3. **Tạo custom template** từ page hiện tại
4. **Manage templates** với right-click menu

### **Chỉnh sửa nội dung:**
1. **Sử dụng toolbar** cho formatting
2. **Keyboard shortcuts**: Ctrl+B (bold), Ctrl+I (italic), Ctrl+U (underline)
3. **Insert elements**: tables, images, links
4. **Auto-save** tự động lưu changes

### **Tìm kiếm:**
1. **Click vào search box** hoặc **Ctrl+F**
2. **Nhập từ khóa** để search trong title và content
3. **Kết quả realtime** với visual feedback

## ⌨️ **Keyboard Shortcuts**

| Shortcut | Chức năng |
|----------|-----------|
| `Ctrl+N` | Tạo page mới |
| `Ctrl+S` | Lưu page hiện tại |
| `Ctrl+F` | Focus search box |
| `Ctrl+\` | Toggle sidebar |
| `Ctrl+B` | Bold text |
| `Ctrl+I` | Italic text |
| `Ctrl+U` | Underline text |
| `Ctrl+K` | Insert link |
| `Ctrl+↑/↓` | Navigate pages |
| `F2` | Rename current page |

## 🗃️ **Database Schema**

### **Pages Table:**
```sql
CREATE TABLE pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parent_id INTEGER,
    icon TEXT,
    cover_image TEXT,
    is_favorite BOOLEAN DEFAULT 0,
    is_template BOOLEAN DEFAULT 0,
    tags TEXT,
    FOREIGN KEY (parent_id) REFERENCES pages (id)
);
```

### **Templates Table:**
```sql
CREATE TABLE templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    content TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Performance Indexes:**
```sql
CREATE INDEX idx_pages_updated_at ON pages(updated_at);
CREATE INDEX idx_pages_parent_id ON pages(parent_id);
CREATE INDEX idx_pages_is_favorite ON pages(is_favorite);
```

## 📁 **Cấu trúc file**

```
Notion/
├── main.py                    # Main application
├── config.json               # Configuration settings
├── notion_clone.db           # SQLite database
├── start.bat                 # Windows batch launcher
├── start.ps1                 # PowerShell launcher
├── launch.py                 # Python launcher
├── launcher.py               # Smart launcher with env detection
├── README.md                 # This file
├── FEATURES.md               # Detailed features documentation
├── QUICKSTART.md             # Quick start guide
├── TITLE_EDITING_GUIDE.md    # Title editing guide
├── PERFORMANCE_ANALYSIS.md   # Performance analysis
└── OPTIMIZATION_REPORT.md    # Optimization report
```

## 🎯 **Tính năng nâng cao**

### **Template Placeholders:**
- `{date}` → Current date (YYYY-MM-DD)
- `{time}` → Current time (HH:MM)
- `{datetime}` → Full datetime

### **Smart Title Editing:**
- **Auto emoji removal** khi rename
- **Input validation** với fallback to "Untitled"
- **Real-time UI updates** 
- **Error recovery** với title reversion

### **Performance Features:**
- **Schema caching** cho faster database operations
- **Debounced auto-save** cho better performance
- **Optimized search** với database-level filtering
- **Smart UI updates** với selection preservation

## 🐛 **Troubleshooting**

### **Common Issues:**

#### **"ModuleNotFoundError: No module named 'PySide6'"**
- **Solution**: Sử dụng `uv run python main.py` thay vì `python main.py`
- **Alternative**: Chạy `pip install PySide6` trước

#### **Database không load được:**
- **Check**: File permissions cho `notion_clone.db`
- **Solution**: Delete database file để tạo mới

#### **Performance chậm:**
- **Check**: Số lượng pages (>1000 có thể chậm)
- **Solution**: Sử dụng search để filter pages

#### **Auto-save không hoạt động:**
- **Check**: Page hiện tại có được select không
- **Solution**: Click vào page trong sidebar

## 📈 **Performance Metrics**

- **Page loading**: ~150ms (70% faster)
- **Database operations**: 0 PRAGMA calls (100% elimination)
- **Auto-save efficiency**: 80% reduction in unnecessary saves
- **Search speed**: ~200ms (90% faster)
- **Memory usage**: ~30MB baseline (33% reduction)

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 **Acknowledgments**

- **PySide6** for the amazing Qt framework
- **SQLite** for reliable database storage
- **UV** for modern Python package management
- **Notion** for inspiration

---

**🎉 Enjoy your enhanced note-taking experience with Notion Clone v2.0!**
