# 📝 Hướng dẫn chỉnh sửa Title và Template

## 🏷️ Chỉnh sửa Title của Page

### Cách 1: Click chuột phải (Right-click)
1. **Mở danh sách Pages** trong sidebar
2. **Right-click** vào page bạn muốn đổi tên
3. **Chọn "✏️ Đổi tên"** từ menu
4. **Nhập tên mới** trong dialog
5. **Click "OK"** để xác nhận

### Cách 2: Chỉnh sửa trực tiếp trong Header
1. **Mở page** bạn muốn đổi tên
2. **Click vào title** ở phần header
3. **Chỉnh sửa trực tiếp** tên page
4. **Nhấn Enter** hoặc click ra ngoài để lưu

### Tính năng nâng cao
- ✅ **Tự động loại bỏ emoji** (📄, 📁, 📋) và ký hiệu favorite (⭐)
- ✅ **Kiểm tra tên trống** - tự động sử dụng "Untitled" nếu để trống
- ✅ **Cập nhật ngay lập tức** trong danh sách và header
- ✅ **Thông báo xác nhận** sau khi đổi tên thành công
- ✅ **Khôi phục tên cũ** nếu có lỗi xảy ra

## 📋 Chỉnh sửa Template

### Quản lý Template trong Tab "📝 Templates"
1. **Mở tab Templates** trong sidebar
2. **Right-click** vào template bạn muốn chỉnh sửa
3. **Chọn hành động** từ context menu:

#### Các hành động có sẵn:
- **📋 Sử dụng Template**: Tạo page mới từ template
- **✏️ Đổi tên Template**: Thay đổi tên template
- **📝 Chỉnh sửa Template**: Chỉnh sửa nội dung và mô tả
- **🗑️ Xóa Template**: Xóa template (có xác nhận)

### Tạo Template từ Page hiện tại
1. **Mở page** bạn muốn tạo template
2. **Click "➕ Tạo Template"** trong tab Templates
3. **Nhập thông tin template**:
   - Tên template
   - Mô tả
   - Category (Custom, Work, Personal, Project, Meeting)
4. **Click "➕ Tạo Template"** để lưu

### Chỉnh sửa Template chi tiết
1. **Right-click** template → **"📝 Chỉnh sửa Template"**
2. **Dialog chỉnh sửa** sẽ hiển thị:
   - **Mô tả Template**: Thông tin mô tả
   - **Nội dung Template**: Editor HTML đầy đủ
3. **Chỉnh sửa nội dung** theo ý muốn
4. **Click "💾 Lưu"** để lưu thay đổi

## 🎯 Tips và Tricks

### Title Editing
- **Emoji được tự động loại bỏ** khi đổi tên để có tên "sạch"
- **Tên không được để trống** - hệ thống sẽ tự động đặt "Untitled"
- **Có thể hoàn tác** nếu có lỗi xảy ra trong quá trình đổi tên
- **Cập nhật real-time** trong tất cả các view

### Template Management
- **Templates có category** để dễ tổ chức
- **Preview template** trước khi sử dụng
- **Duplicate templates** bằng cách tạo mới từ page
- **Rich text formatting** được hỗ trợ đầy đủ

### Keyboard Shortcuts
- **F2**: Đổi tên page đang active (nếu có)
- **Ctrl+N**: Tạo page mới
- **Ctrl+T**: Tạo page từ template
- **Del**: Xóa page/template được chọn (có xác nhận)

## 🚀 Advanced Features

### Smart Title Processing
- Tự động detect và remove emojis: 📄 📁 📋
- Loại bỏ favorite indicator: ⭐
- Trim whitespace và validate input
- Fallback to "Untitled" cho empty strings

### Template System
- **Category-based organization**
- **Rich content support** (HTML formatting)
- **Metadata tracking** (description, category)
- **Version control** (update existing templates)
- **Usage tracking** (có thể mở rộng)

### Error Handling
- **Graceful degradation** khi có lỗi
- **User-friendly error messages**
- **Automatic rollback** cho failed operations
- **Status notifications** cho tất cả actions

## 🔧 Troubleshooting

### Nếu không đổi được tên:
1. Kiểm tra page có đang được edit không
2. Thử đóng và mở lại page
3. Restart ứng dụng nếu cần

### Nếu template không load:
1. Kiểm tra database connection
2. Restart ứng dụng
3. Check file permissions

### Performance Issues:
- **Large templates** có thể load chậm
- **Many pages** có thể affect rename speed
- Sử dụng **search function** cho large datasets

---

**💡 Tip**: Sử dụng right-click menu để truy cập nhanh tất cả các tính năng quản lý!
