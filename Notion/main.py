import sys
import sqlite3
import json
import re
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QListWidget,
    QVBoxLayout, QHBoxLayout, QWidget, QSplitter,
    QPushButton, QToolBar, QListWidgetItem, QInputDialog, QMessageBox,
    QLineEdit, QLabel, QComboBox, QCheckBox, QTabWidget, QFrame,
    QScrollArea, QGroupBox, QGridLayout, QSpacerItem, QSizePolicy,
    QMenuBar, QMenu, QStatusBar, QTreeWidget, QTreeWidgetItem,
    QTableWidget, QTableWidgetItem, QTextBrowser, QProgressBar,
    QSlider, QSpinBox, QDateEdit, QTimeEdit, QCalendarWidget,
    QFileDialog, QColorDialog, QFontDialog, QDialog
)
from PySide6.QtGui import (
    QFont, QAction, QIcon, QPixmap, QPainter, QColor, QKeySequence,
    QTextCharFormat, QTextCursor, QTextDocument, QTextBlockFormat,
    QTextListFormat, QBrush, QPen, QShortcut
)
from PySide6.QtCore import Qt, QSize, QTimer, QDate, QTime, QDateTime
from PySide6.QtSvg import QSvgRenderer

# Import custom styles
try:
    from styles import apply_styles, MAIN_STYLES
except ImportError:
    apply_styles = None
    MAIN_STYLES = ""

# --- Cấu hình ---
DB_NAME = "notion_clone.db"
WINDOW_TITLE = "Python Notion Clone"
INITIAL_WINDOW_SIZE = (1000, 700)

class NotionCloneApp(QMainWindow):
    """
    Lớp chính của ứng dụng, kế thừa từ QMainWindow.
    Chịu trách nhiệm khởi tạo giao diện, kết nối cơ sở dữ liệu và xử lý sự kiện.
    """
    def __init__(self):
        super().__init__()
        self.current_page_id = None
        self.db_connection = None
        self.db_cursor = None
        
        # Performance optimization caches
        self._table_schema_cache = {}
        self._last_saved_content = ""
        self._auto_save_timer = None
        self._is_loading = False

        self.init_db()
        self.init_ui()
        self.load_pages_from_db()

    def init_ui(self):
        """Khởi tạo giao diện người dùng nâng cao với keyboard shortcuts."""
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(QSize(*INITIAL_WINDOW_SIZE))
        self.setWindowIcon(self._create_app_icon())

        # --- Keyboard Shortcuts ---
        self.setup_keyboard_shortcuts()

        # --- Tạo Menu Bar ---
        self.create_menu_bar()

        # --- Tạo Toolbar nâng cao ---
        self.create_toolbar()

        # --- Bố cục chính với tabs ---
        self.create_main_layout()

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sẵn sàng")

    def setup_keyboard_shortcuts(self):
        """Setup các keyboard shortcuts hữu ích."""
        
        # Quick new page
        QShortcut(QKeySequence("Ctrl+N"), self, self.create_new_page)
        
        # Quick save
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_current_page)
        
        # Search focus
        def focus_search():
            self.search_box.setFocus()
            self.search_box.selectAll()
        QShortcut(QKeySequence("Ctrl+F"), self, focus_search)
        
        # Toggle sidebar
        QShortcut(QKeySequence("Ctrl+\\"), self, self.toggle_sidebar)
        
        # Quick formatting
        QShortcut(QKeySequence("Ctrl+B"), self, self.make_text_bold)
        QShortcut(QKeySequence("Ctrl+I"), self, self.make_text_italic)
        QShortcut(QKeySequence("Ctrl+U"), self, self.make_text_underline)
        
        # Navigate between pages
        def next_page():
            current = self.pages_list_widget.currentItem()
            if current:
                index = self.pages_list_widget.indexOfTopLevelItem(current)
                next_index = (index + 1) % self.pages_list_widget.topLevelItemCount()
                next_item = self.pages_list_widget.topLevelItem(next_index)
                if next_item:
                    self.pages_list_widget.setCurrentItem(next_item)
        
        def prev_page():
            current = self.pages_list_widget.currentItem()
            if current:
                index = self.pages_list_widget.indexOfTopLevelItem(current)
                prev_index = (index - 1) % self.pages_list_widget.topLevelItemCount()
                prev_item = self.pages_list_widget.topLevelItem(prev_index)
                if prev_item:
                    self.pages_list_widget.setCurrentItem(prev_item)
        
        QShortcut(QKeySequence("Ctrl+Down"), self, next_page)
        QShortcut(QKeySequence("Ctrl+Up"), self, prev_page)

    def create_menu_bar(self):
        """Tạo menu bar với đầy đủ chức năng."""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu('&File')
        
        new_page_action = QAction('&Tạo trang mới', self)
        new_page_action.setShortcut(QKeySequence.New)
        new_page_action.triggered.connect(self.create_new_page)
        file_menu.addAction(new_page_action)

        open_action = QAction('&Mở...', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('&Lưu', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_current_page)
        file_menu.addAction(save_action)

        export_action = QAction('&Xuất...', self)
        export_action.triggered.connect(self.export_page)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction('&Thoát', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu('&Edit')
        
        undo_action = QAction('&Hoàn tác', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('&Làm lại', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        copy_action = QAction('&Sao chép', self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('&Dán', self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)

        # View Menu
        view_menu = menubar.addMenu('&View')
        
        toggle_sidebar_action = QAction('&Ẩn/Hiện Sidebar', self)
        toggle_sidebar_action.setShortcut('Ctrl+\\')
        toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(toggle_sidebar_action)

        # Insert Menu
        insert_menu = menubar.addMenu('&Insert')
        
        insert_table_action = QAction('&Bảng', self)
        insert_table_action.triggered.connect(self.insert_table)
        insert_menu.addAction(insert_table_action)

        insert_image_action = QAction('&Hình ảnh', self)
        insert_image_action.triggered.connect(self.insert_image)
        insert_menu.addAction(insert_image_action)

        insert_link_action = QAction('&Liên kết', self)
        insert_link_action.setShortcut('Ctrl+K')
        insert_link_action.triggered.connect(self.insert_link)
        insert_menu.addAction(insert_link_action)

    def create_toolbar(self):
        """Tạo toolbar nâng cao với nhiều chức năng."""
        # Main Toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Font controls
        self.font_combo = QComboBox()
        self.font_combo.addItems(['Arial', 'Times New Roman', 'Helvetica', 'Courier New', 'Verdana'])
        self.font_combo.currentTextChanged.connect(self.change_font_family)
        toolbar.addWidget(QLabel("Font:"))
        toolbar.addWidget(self.font_combo)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(12)
        self.font_size_spin.valueChanged.connect(self.change_font_size)
        toolbar.addWidget(QLabel("Size:"))
        toolbar.addWidget(self.font_size_spin)

        toolbar.addSeparator()

        # Text formatting
        action_bold = QAction('B', self)
        action_bold.setCheckable(True)
        action_bold.setToolTip('Bold')
        action_bold.triggered.connect(self.make_text_bold)
        toolbar.addAction(action_bold)

        action_italic = QAction('I', self)
        action_italic.setCheckable(True)
        action_italic.setToolTip('Italic')
        action_italic.triggered.connect(self.make_text_italic)
        toolbar.addAction(action_italic)

        action_underline = QAction('U', self)
        action_underline.setCheckable(True)
        action_underline.setToolTip('Underline')
        action_underline.triggered.connect(self.make_text_underline)
        toolbar.addAction(action_underline)

        toolbar.addSeparator()

        # Color controls
        color_action = QAction('🎨', self)
        color_action.setToolTip('Text Color')
        color_action.triggered.connect(self.change_text_color)
        toolbar.addAction(color_action)

        bg_color_action = QAction('🖍️', self)
        bg_color_action.setToolTip('Background Color')
        bg_color_action.triggered.connect(self.change_background_color)
        toolbar.addAction(bg_color_action)

        toolbar.addSeparator()

        # List controls
        bullet_action = QAction('• List', self)
        bullet_action.triggered.connect(self.insert_bullet_list)
        toolbar.addAction(bullet_action)

        number_action = QAction('1. List', self)
        number_action.triggered.connect(self.insert_number_list)
        toolbar.addAction(number_action)

        toolbar.addSeparator()

        # Save button
        action_save = QAction('💾', self)
        action_save.setToolTip('Save')
        action_save.triggered.connect(self.save_current_page)
        toolbar.addAction(action_save)

    def create_main_layout(self):
        """Tạo bố cục chính với tabs và nhiều panel."""
        # Main splitter
        main_splitter = QSplitter(Qt.Horizontal)

        # Left sidebar với tabs
        self.sidebar_widget = QTabWidget()
        self.sidebar_widget.setMaximumWidth(300)
        
        # Pages tab
        self.create_pages_tab()
        
        # Templates tab
        self.create_templates_tab()
        
        # Recent tab
        self.create_recent_tab()

        # Main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Page header
        self.create_page_header()
        content_layout.addWidget(self.page_header)

        # Editor với tabs
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.tabCloseRequested.connect(self.close_editor_tab)
        
        # Default editor tab
        self.editor_widget = QTextEdit()
        self.editor_widget.setFont(QFont("Arial", 12))
        self.editor_widget.textChanged.connect(self.on_text_changed)
        self.editor_tabs.addTab(self.editor_widget, "Untitled")

        content_layout.addWidget(self.editor_tabs)

        # Add to splitter
        main_splitter.addWidget(self.sidebar_widget)
        main_splitter.addWidget(content_widget)
        main_splitter.setSizes([250, 750])

        self.setCentralWidget(main_splitter)

    def create_pages_tab(self):
        """Tạo tab quản lý pages với drag & drop support."""
        pages_widget = QWidget()
        pages_layout = QVBoxLayout(pages_widget)

        # Search box với placeholder động
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Tìm kiếm theo tên hoặc nội dung...")
        self.search_box.textChanged.connect(self.filter_pages)
        pages_layout.addWidget(self.search_box)

        # Pages list với drag & drop
        self.pages_list_widget = QTreeWidget()
        self.pages_list_widget.setHeaderLabels(["Title", "Updated"])
        self.pages_list_widget.currentItemChanged.connect(self.page_selection_changed)
        
        # Enable drag & drop
        self.pages_list_widget.setDragDropMode(QTreeWidget.InternalMove)
        self.pages_list_widget.setDefaultDropAction(Qt.MoveAction)
        
        # Context menu
        self.pages_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pages_list_widget.customContextMenuRequested.connect(self.show_page_context_menu)
        
        pages_layout.addWidget(self.pages_list_widget)

        # Control buttons với icons
        buttons_layout = QHBoxLayout()
        
        new_page_button = QPushButton("📄 Tạo trang")
        new_page_button.setToolTip("Tạo trang mới (Ctrl+N)")
        new_page_button.clicked.connect(self.create_new_page)
        buttons_layout.addWidget(new_page_button)

        new_folder_button = QPushButton("📁 Tạo folder")
        new_folder_button.setToolTip("Tạo folder để tổ chức pages")
        new_folder_button.clicked.connect(self.create_new_folder)
        buttons_layout.addWidget(new_folder_button)

        pages_layout.addLayout(buttons_layout)

        self.sidebar_widget.addTab(pages_widget, "📋 Pages")

    def show_page_context_menu(self, position):
        """Hiển thị context menu cho pages."""
        item = self.pages_list_widget.itemAt(position)
        if item is None:
            return
            
        menu = QMenu(self)
        
        # Actions
        rename_action = QAction("✏️ Đổi tên", self)
        rename_action.triggered.connect(lambda: self.rename_page(item))
        menu.addAction(rename_action)
        
        delete_action = QAction("🗑️ Xóa", self)
        delete_action.triggered.connect(lambda: self.delete_page(item))
        menu.addAction(delete_action)
        
        menu.addSeparator()
        
        duplicate_action = QAction("📄 Duplicate", self)
        duplicate_action.triggered.connect(lambda: self.duplicate_page(item))
        menu.addAction(duplicate_action)
        
        export_action = QAction("📤 Export", self)
        export_action.triggered.connect(self.export_page)
        menu.addAction(export_action)
        
        menu.exec_(self.pages_list_widget.mapToGlobal(position))

    def rename_page(self, item):
        """Đổi tên page với inline editing tối ưu và UX cải thiện."""
        page_id = item.data(0, Qt.UserRole)
        if not page_id:
            return
            
        # Extract current title (remove emoji and favorite indicator)
        current_text = item.text(0)
        old_title = self._extract_clean_title(current_text)
        
        # Show enhanced input dialog
        dialog = self._create_rename_dialog(old_title, "page")
        
        if dialog.exec_() == QDialog.Accepted:
            new_title = dialog.title_input.text().strip()
            
            if self._validate_title(new_title, "page"):
                self._update_page_title_in_db(page_id, new_title, old_title)

    def _extract_clean_title(self, text):
        """Trích xuất title sạch từ display text."""
        # Remove common emojis and indicators
        clean_title = text
        emoji_patterns = ["📄", "📁", "📋", "⭐", "🏷️"]
        
        for emoji in emoji_patterns:
            clean_title = clean_title.replace(emoji, "")
        
        # Remove extra whitespace
        return clean_title.strip()

    def _create_rename_dialog(self, current_title, item_type="page"):
        """Tạo dialog rename với UX cải thiện."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"✏️ Đổi tên {item_type}")
        dialog.setModal(True)
        dialog.resize(400, 200)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        
        # Instruction label
        instruction = QLabel(f"Nhập tên mới cho {item_type}:")
        instruction.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(instruction)
        
        # Title input với enhanced styling
        dialog.title_input = QLineEdit(current_title)
        dialog.title_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border-color: #2196f3;
                background-color: #f8f9fa;
            }
        """)
        dialog.title_input.selectAll()  # Select all text for easy editing
        layout.addWidget(dialog.title_input)
        
        # Character count label
        char_count_label = QLabel(f"Độ dài: {len(current_title)} ký tự")
        char_count_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(char_count_label)
        
        # Update character count on text change
        def update_char_count():
            count = len(dialog.title_input.text())
            char_count_label.setText(f"Độ dài: {count} ký tự")
            if count > 100:
                char_count_label.setStyleSheet("color: #ff6b6b; font-size: 12px; font-weight: bold;")
            else:
                char_count_label.setStyleSheet("color: #666; font-size: 12px;")
        
        dialog.title_input.textChanged.connect(update_char_count)
        
        # Buttons với enhanced styling
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("❌ Hủy")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        cancel_button.clicked.connect(dialog.reject)
        buttons_layout.addWidget(cancel_button)
        
        rename_button = QPushButton("✏️ Đổi tên")
        rename_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #1565c0;
            }
        """)
        rename_button.clicked.connect(dialog.accept)
        rename_button.setDefault(True)  # Make it default button
        buttons_layout.addWidget(rename_button)
        
        layout.addLayout(buttons_layout)
        
        # Enable Enter to confirm
        dialog.title_input.returnPressed.connect(dialog.accept)
        
        return dialog

    def _validate_title(self, title, item_type="page"):
        """Validate title với feedback chi tiết."""
        if not title:
            QMessageBox.warning(
                self, "⚠️ Lỗi đầu vào", 
                f"Tên {item_type} không được để trống!\n\nVui lòng nhập một tên hợp lệ.",
                QMessageBox.Ok
            )
            return False
        
        if len(title) > 100:
            QMessageBox.warning(
                self, "⚠️ Tên quá dài", 
                f"Tên {item_type} không được vượt quá 100 ký tự!\n\nHiện tại: {len(title)} ký tự.",
                QMessageBox.Ok
            )
            return False
        
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        for char in invalid_chars:
            if char in title:
                QMessageBox.warning(
                    self, "⚠️ Ký tự không hợp lệ", 
                    f"Tên {item_type} không được chứa ký tự: {char}\n\nVui lòng loại bỏ ký tự này.",
                    QMessageBox.Ok
                )
                return False
        
        return True

    def _update_page_title_in_db(self, page_id, new_title, old_title):
        """Cập nhật title trong database với error handling chi tiết."""
        try:
            # Use cached column information
            columns = self._get_table_columns('pages')
            
            if 'updated_at' in columns:
                self.db_cursor.execute("""
                    UPDATE pages SET title = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (new_title, page_id))
            else:
                self.db_cursor.execute("""
                    UPDATE pages SET title = ? WHERE id = ?
                """, (new_title, page_id))
            
            self.db_connection.commit()
            
            # Optimized reload with selection preservation
            self.load_pages_from_db(preserve_selection=True)
            
            # Update page title edit if this is the current page
            if hasattr(self, 'current_page_id') and self.current_page_id == page_id:
                self.page_title_edit.blockSignals(True)
                self.page_title_edit.setText(new_title)
                self.page_title_edit.blockSignals(False)
            
            # Enhanced success feedback
            self.status_bar.showMessage(f"✅ Đã đổi tên: '{old_title}' → '{new_title}'", 4000)
            
            # Show success notification
            self._show_rename_success(old_title, new_title, "page")
            
        except sqlite3.Error as e:
            self._handle_rename_error(e, new_title, "page")

    def _show_rename_success(self, old_title, new_title, item_type):
        """Hiển thị thông báo thành công với animation."""
        # Create a temporary widget for success notification
        if hasattr(self, '_success_timer'):
            self._success_timer.stop()
        
        self._success_timer = QTimer()
        self._success_timer.timeout.connect(lambda: self.status_bar.clearMessage())
        self._success_timer.setSingleShot(True)
        self._success_timer.start(4000)
        
        # Optional: Add to recent activity log
        self._add_to_activity_log(f"Renamed {item_type}: '{old_title}' to '{new_title}'")

    def _handle_rename_error(self, error, attempted_title, item_type):
        """Xử lý lỗi rename với feedback chi tiết."""
        error_msg = str(error)
        
        if "UNIQUE constraint failed" in error_msg:
            QMessageBox.critical(
                self, "❌ Tên đã tồn tại", 
                f"Tên '{attempted_title}' đã được sử dụng!\n\n"
                f"Vui lòng chọn tên khác cho {item_type}.",
                QMessageBox.Ok
            )
        elif "database is locked" in error_msg:
            QMessageBox.critical(
                self, "❌ Database đang bận", 
                f"Không thể đổi tên {item_type} vì database đang được sử dụng.\n\n"
                "Vui lòng thử lại sau ít phút.",
                QMessageBox.Ok
            )
        else:
            QMessageBox.critical(
                self, "❌ Lỗi không xác định", 
                f"Không thể đổi tên {item_type}: {attempted_title}\n\n"
                f"Chi tiết lỗi: {error}",
                QMessageBox.Ok
            )
        
        self.status_bar.showMessage(f"❌ Lỗi đổi tên {item_type}: {attempted_title}", 5000)

    def _add_to_activity_log(self, activity):
        """Thêm hoạt động vào log (có thể mở rộng sau)."""
        if not hasattr(self, '_activity_log'):
            self._activity_log = []
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        self._activity_log.append(f"[{timestamp}] {activity}")
        
        # Keep only last 50 activities
        if len(self._activity_log) > 50:
            self._activity_log = self._activity_log[-50:]

    def delete_page(self, item):
        """Xóa page với confirmation."""
        page_id = item.data(0, Qt.UserRole)
        if page_id:
            title = item.text(0)
            reply = QMessageBox.question(
                self, "Xác nhận xóa", 
                f"Bạn có chắc muốn xóa '{title}'?\nHành động này không thể hoàn tác.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    self.db_cursor.execute("DELETE FROM pages WHERE id = ?", (page_id,))
                    self.db_connection.commit()
                    self.load_pages_from_db()
                    self.clear_editor()
                    self.status_bar.showMessage(f"🗑️ Đã xóa: {title}", 2000)
                except sqlite3.Error as e:
                    self.show_error_message("Lỗi xóa", f"Không thể xóa trang: {e}")

    def duplicate_page(self, item):
        """Duplicate page."""
        page_id = item.data(0, Qt.UserRole)
        if page_id:
            try:
                # Get page data
                self.db_cursor.execute(
                    "SELECT title, content, icon, tags FROM pages WHERE id = ?", 
                    (page_id,)
                )
                result = self.db_cursor.fetchone()
                if result:
                    title, content, icon, tags = result
                    new_title = f"{title} (Copy)"
                    
                    # Create duplicate
                    self.db_cursor.execute("""
                        INSERT INTO pages (title, content, icon, tags, created_at, updated_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """, (new_title, content, icon, tags))
                    
                    self.db_connection.commit()
                    self.load_pages_from_db()
                    self.status_bar.showMessage(f"📄 Đã duplicate: {new_title}", 2000)
                    
            except sqlite3.Error as e:
                self.show_error_message("Lỗi duplicate", f"Không thể duplicate trang: {e}")

    def create_templates_tab(self):
        """Tạo tab templates với quản lý đầy đủ."""
        templates_widget = QWidget()
        templates_layout = QVBoxLayout(templates_widget)

        # Template categories
        template_categories = QComboBox()
        template_categories.addItems([
            "Tất cả", "Meeting Notes", "Project Plan", 
            "Daily Journal", "Task List", "Custom"
        ])
        templates_layout.addWidget(template_categories)

        # Templates list với context menu
        self.templates_list = QListWidget()
        self.templates_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.templates_list.customContextMenuRequested.connect(self.show_template_context_menu)
        self.load_templates()
        templates_layout.addWidget(self.templates_list)

        # Template control buttons
        template_buttons_layout = QHBoxLayout()
        
        use_template_button = QPushButton("📋 Sử dụng Template")
        use_template_button.setToolTip("Tạo page mới từ template được chọn")
        use_template_button.clicked.connect(self.use_template)
        template_buttons_layout.addWidget(use_template_button)
        
        create_template_button = QPushButton("➕ Tạo Template")
        create_template_button.setToolTip("Tạo template mới từ page hiện tại")
        create_template_button.clicked.connect(self.create_template_from_current_page)
        template_buttons_layout.addWidget(create_template_button)
        
        templates_layout.addLayout(template_buttons_layout)

        self.sidebar_widget.addTab(templates_widget, "� Templates")

    def show_template_context_menu(self, position):
        """Hiển thị context menu cho templates."""
        item = self.templates_list.itemAt(position)
        if item is None:
            return
            
        menu = QMenu(self)
        
        # Actions
        use_action = QAction("�📋 Sử dụng Template", self)
        use_action.triggered.connect(self.use_template)
        menu.addAction(use_action)
        
        menu.addSeparator()
        
        rename_action = QAction("✏️ Đổi tên Template", self)
        rename_action.triggered.connect(lambda: self.rename_template(item))
        menu.addAction(rename_action)
        
        edit_action = QAction("📝 Chỉnh sửa Template", self)
        edit_action.triggered.connect(lambda: self.edit_template(item))
        menu.addAction(edit_action)
        
        delete_action = QAction("🗑️ Xóa Template", self)
        delete_action.triggered.connect(lambda: self.delete_template(item))
        menu.addAction(delete_action)
        
        menu.exec_(self.templates_list.mapToGlobal(position))

    def rename_template(self, item):
        """Đổi tên template với UX cải thiện."""
        template_name = item.text().split('\n')[0]
        
        # Show enhanced rename dialog
        dialog = self._create_rename_dialog(template_name, "template")
        
        if dialog.exec_() == QDialog.Accepted:
            new_name = dialog.title_input.text().strip()
            
            if self._validate_title(new_name, "template"):
                self._update_template_name_in_db(template_name, new_name)

    def _update_template_name_in_db(self, old_name, new_name):
        """Cập nhật tên template trong database."""
        try:
            # Check if template name already exists
            self.db_cursor.execute("SELECT COUNT(*) FROM templates WHERE name = ?", (new_name,))
            if self.db_cursor.fetchone()[0] > 0:
                QMessageBox.warning(
                    self, "⚠️ Tên đã tồn tại", 
                    f"Template '{new_name}' đã tồn tại!\n\nVui lòng chọn tên khác.",
                    QMessageBox.Ok
                )
                return
            
            self.db_cursor.execute("""
                UPDATE templates SET name = ? WHERE name = ?
            """, (new_name, old_name))
            
            self.db_connection.commit()
            
            # Reload templates list
            self.templates_list.clear()
            self.load_templates()
            
            # Enhanced success feedback
            self.status_bar.showMessage(f"✅ Đã đổi tên template: '{old_name}' → '{new_name}'", 4000)
            
            # Show success notification
            self._show_rename_success(old_name, new_name, "template")
            
        except sqlite3.Error as e:
            self._handle_rename_error(e, new_name, "template")

    def edit_template(self, item):
        """Chỉnh sửa nội dung template."""
        template_name = item.text().split('\n')[0]
        
        try:
            self.db_cursor.execute("""
                SELECT description, content FROM templates WHERE name = ?
            """, (template_name,))
            result = self.db_cursor.fetchone()
            
            if result:
                description, content = result
                
                # Dialog để chỉnh sửa
                dialog = QDialog(self)
                dialog.setWindowTitle(f"📝 Chỉnh sửa Template: {template_name}")
                dialog.setModal(True)
                dialog.resize(600, 500)
                
                layout = QVBoxLayout(dialog)
                
                # Description
                layout.addWidget(QLabel("Mô tả Template:"))
                desc_edit = QLineEdit(description or "")
                layout.addWidget(desc_edit)
                
                # Content
                layout.addWidget(QLabel("Nội dung Template:"))
                content_edit = QTextEdit()
                content_edit.setHtml(content or "")
                layout.addWidget(content_edit)
                
                # Buttons
                buttons_layout = QHBoxLayout()
                
                save_button = QPushButton("💾 Lưu")
                save_button.clicked.connect(dialog.accept)
                buttons_layout.addWidget(save_button)
                
                cancel_button = QPushButton("❌ Hủy")
                cancel_button.clicked.connect(dialog.reject)
                buttons_layout.addWidget(cancel_button)
                
                layout.addLayout(buttons_layout)
                
                # Show dialog
                if dialog.exec_() == QDialog.Accepted:
                    new_desc = desc_edit.text().strip()
                    new_content = content_edit.toHtml()
                    
                    try:
                        self.db_cursor.execute("""
                            UPDATE templates SET description = ?, content = ? WHERE name = ?
                        """, (new_desc, new_content, template_name))
                        
                        self.db_connection.commit()
                        self.load_templates()
                        self.status_bar.showMessage(f"✅ Đã cập nhật template: '{template_name}'", 3000)
                        
                    except sqlite3.Error as e:
                        self.show_error_message("Lỗi cập nhật template", f"Không thể cập nhật template: {e}")
                        
        except sqlite3.Error as e:
            self.show_error_message("Lỗi load template", f"Không thể load template: {e}")

    def delete_template(self, item):
        """Xóa template với confirmation."""
        template_name = item.text().split('\n')[0]
        
        reply = QMessageBox.question(
            self, "🗑️ Xác nhận xóa Template", 
            f"Bạn có chắc muốn xóa template '{template_name}'?\nHành động này không thể hoàn tác.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db_cursor.execute("DELETE FROM templates WHERE name = ?", (template_name,))
                self.db_connection.commit()
                self.load_templates()
                self.status_bar.showMessage(f"🗑️ Đã xóa template: '{template_name}'", 3000)
                
            except sqlite3.Error as e:
                self.show_error_message("Lỗi xóa template", f"Không thể xóa template: {e}")

    def create_template_from_current_page(self):
        """Tạo template từ page hiện tại với UX cải thiện."""
        if not hasattr(self, 'current_page_id') or not self.current_page_id:
            QMessageBox.warning(
                self, "⚠️ Không có trang", 
                "Vui lòng mở một trang trước khi tạo template!\n\nBạn cần có nội dung để tạo template.",
                QMessageBox.Ok
            )
            return
        
        # Get current page info
        current_title = self.page_title_edit.text() or "Untitled"
        current_content = self.editor_widget.toHtml()
        
        # Show enhanced dialog
        dialog = self._create_template_from_page_dialog(current_title, current_content)
        
        if dialog.exec_() == QDialog.Accepted:
            template_name = dialog.name_input.text().strip()
            template_desc = dialog.desc_input.text().strip()
            template_category = dialog.category_combo.currentText()
            
            if self._validate_template_creation_data(template_name, template_desc):
                self._save_template_from_page(template_name, template_desc, template_category, current_content)

    def _create_template_from_page_dialog(self, current_title, current_content):
        """Tạo dialog cải thiện cho việc tạo template từ page."""
        dialog = QDialog(self)
        dialog.setWindowTitle("🎨 Tạo Template từ Trang hiện tại")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                border: 2px solid #3d3d3d;
                border-radius: 12px;
            }
            QLabel {
                color: #ffffff;
                font-weight: bold;
                font-size: 11pt;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2d2d2d;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 11pt;
                selection-background-color: #0078d4;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #0078d4;
                background-color: #333333;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #404040;
                border-radius: 4px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #ffffff;
                border-top: none;
                border-right: none;
                width: 6px;
                height: 6px;
                margin: 4px;
                transform: rotate(45deg);
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton#cancelButton {
                background-color: #5a5a5a;
            }
            QPushButton#cancelButton:hover {
                background-color: #6a6a6a;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header with page info
        header_label = QLabel(f"📄 Tạo template từ: '{current_title}'")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 13pt; color: #0078d4; margin-bottom: 15px;")
        layout.addWidget(header_label)
        
        # Template name
        name_label = QLabel("📋 Tên template:")
        layout.addWidget(name_label)
        
        name_input = QLineEdit(f"Template từ {current_title}")
        name_input.selectAll()  # Pre-select for easy editing
        dialog.name_input = name_input
        layout.addWidget(name_input)
        
        # Character count for name
        name_count_label = QLabel(f"{len(name_input.text())}/100 ký tự")
        name_count_label.setAlignment(Qt.AlignRight)
        name_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        layout.addWidget(name_count_label)
        
        # Template description
        desc_label = QLabel("📝 Mô tả template:")
        layout.addWidget(desc_label)
        
        desc_input = QLineEdit(f"Template được tạo từ trang '{current_title}'")
        dialog.desc_input = desc_input
        layout.addWidget(desc_input)
        
        # Character count for description
        desc_count_label = QLabel(f"{len(desc_input.text())}/200 ký tự")
        desc_count_label.setAlignment(Qt.AlignRight)
        desc_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        layout.addWidget(desc_count_label)
        
        # Template category
        category_label = QLabel("🏷️ Danh mục:")
        layout.addWidget(category_label)
        
        category_combo = QComboBox()
        category_combo.addItems([
            "📄 Chung",
            "💼 Công việc", 
            "👤 Cá nhân",
            "📊 Dự án",
            "🤝 Họp/Meeting",
            "📚 Học tập",
            "💡 Ý tưởng",
            "📋 Checklist"
        ])
        dialog.category_combo = category_combo
        layout.addWidget(category_combo)
        
        # Content preview
        preview_label = QLabel("👀 Xem trước nội dung:")
        layout.addWidget(preview_label)
        
        # Simplified content preview
        content_text = self.editor_widget.toPlainText()[:200] + "..." if len(self.editor_widget.toPlainText()) > 200 else self.editor_widget.toPlainText()
        preview_text = QTextEdit()
        preview_text.setPlainText(content_text)
        preview_text.setMaximumHeight(80)
        preview_text.setReadOnly(True)
        preview_text.setStyleSheet("background-color: #252525; border: 1px solid #555555;")
        layout.addWidget(preview_text)
        
        # Update character counts
        def update_name_count():
            count = len(name_input.text())
            name_count_label.setText(f"{count}/100 ký tự")
            if count > 100:
                name_count_label.setStyleSheet("color: #ff4444; font-weight: bold;")
            else:
                name_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        
        def update_desc_count():
            count = len(desc_input.text())
            desc_count_label.setText(f"{count}/200 ký tự")
            if count > 200:
                desc_count_label.setStyleSheet("color: #ff4444; font-weight: bold;")
            else:
                desc_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        
        name_input.textChanged.connect(update_name_count)
        desc_input.textChanged.connect(update_desc_count)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("❌ Hủy")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(dialog.reject)
        
        create_button = QPushButton("🎨 Tạo Template")
        create_button.clicked.connect(dialog.accept)
        create_button.setDefault(True)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(create_button)
        layout.addLayout(button_layout)
        
        # Focus on name input
        name_input.setFocus()
        
        return dialog

    def _validate_template_creation_data(self, name, desc):
        """Kiểm tra tính hợp lệ của dữ liệu tạo template."""
        if not name:
            QMessageBox.warning(
                self, "⚠️ Thiếu thông tin", 
                "Vui lòng nhập tên cho template!",
                QMessageBox.Ok
            )
            return False
        
        if len(name) > 100:
            QMessageBox.warning(
                self, "⚠️ Tên quá dài", 
                "Tên template không được vượt quá 100 ký tự!",
                QMessageBox.Ok
            )
            return False
        
        if len(desc) > 200:
            QMessageBox.warning(
                self, "⚠️ Mô tả quá dài", 
                "Mô tả template không được vượt quá 200 ký tự!",
                QMessageBox.Ok
            )
            return False
        
        return True

    def _save_template_from_page(self, name, description, category, content):
        """Lưu template được tạo từ page."""
        try:
            # Check if template name already exists
            self.db_cursor.execute("SELECT COUNT(*) FROM templates WHERE name = ?", (name,))
            if self.db_cursor.fetchone()[0] > 0:
                reply = QMessageBox.question(
                    self, "❓ Template đã tồn tại", 
                    f"Template '{name}' đã tồn tại!\n\nBạn có muốn ghi đè template hiện tại không?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
                
                # Update existing template
                self.db_cursor.execute("""
                    UPDATE templates SET description = ?, content = ?, category = ?, created_at = ?
                    WHERE name = ?
                """, (description, content, category, datetime.now().isoformat(), name))
                action = "cập nhật"
            else:
                # Create new template
                self.db_cursor.execute("""
                    INSERT INTO templates (name, description, content, category, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, description, content, category, datetime.now().isoformat()))
                action = "tạo"
            
            self.db_connection.commit()
            
            # Reload templates
            self.templates_list.clear()
            self.load_templates()
            
            # Success feedback
            self.status_bar.showMessage(f"✅ Đã {action} template: '{name}'", 4000)
            
            # Show success message
            QMessageBox.information(
                self, "🎉 Thành công!", 
                f"Template '{name}' đã được {action} thành công!\n\nDanh mục: {category}\nBạn có thể sử dụng template này để tạo trang mới.",
                QMessageBox.Ok
            )
            
        except sqlite3.Error as e:
            QMessageBox.critical(
                self, "❌ Lỗi cơ sở dữ liệu", 
                f"Không thể {action} template:\n\n{str(e)}\n\nVui lòng thử lại!",
                QMessageBox.Ok
            )

    def create_recent_tab(self):
        """Tạo tab recent files với khả năng tương tác."""
        recent_widget = QWidget()
        recent_layout = QVBoxLayout(recent_widget)

        self.recent_list = QListWidget()
        self.recent_list.itemDoubleClicked.connect(self.open_recent_page)
        self.load_recent_pages()
        recent_layout.addWidget(self.recent_list)

        # Button refresh recent
        refresh_recent_btn = QPushButton("🔄 Refresh Recent")
        refresh_recent_btn.clicked.connect(self.load_recent_pages)
        recent_layout.addWidget(refresh_recent_btn)

        self.sidebar_widget.addTab(recent_widget, "🕒 Recent")

    def open_recent_page(self, item):
        """Mở page từ recent list."""
        page_title = item.data(Qt.UserRole)
        if page_title:
            try:
                # Tìm page theo title
                self.db_cursor.execute("SELECT id FROM pages WHERE title = ? LIMIT 1", (page_title,))
                result = self.db_cursor.fetchone()
                
                if result:
                    page_id = result[0]
                    # Select page trong tree
                    self.find_and_select_page(page_id)
                    self.status_bar.showMessage(f"📖 Đã mở: {page_title}", 2000)
                    
            except sqlite3.Error as e:
                self.show_error_message("Lỗi mở recent page", f"Không thể mở page: {e}")

    def create_page_header(self):
        """Tạo header cho page với title và metadata."""
        self.page_header = QFrame()
        header_layout = QVBoxLayout(self.page_header)

        # Title area
        title_layout = QHBoxLayout()
        
        self.page_icon_label = QLabel("📄")
        self.page_icon_label.setStyleSheet("font-size: 24px;")
        title_layout.addWidget(self.page_icon_label)

        self.page_title_edit = QLineEdit()
        self.page_title_edit.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        self.page_title_edit.setPlaceholderText("Untitled")
        self.page_title_edit.textChanged.connect(self.update_page_title)
        title_layout.addWidget(self.page_title_edit)

        header_layout.addLayout(title_layout)

        # Metadata area
        meta_layout = QHBoxLayout()
        
        self.favorite_checkbox = QCheckBox("⭐ Favorite")
        self.favorite_checkbox.stateChanged.connect(self.toggle_favorite)
        meta_layout.addWidget(self.favorite_checkbox)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Tags (comma separated)")
        self.tags_edit.textChanged.connect(self.update_tags)
        meta_layout.addWidget(QLabel("🏷️"))
        meta_layout.addWidget(self.tags_edit)

        meta_layout.addStretch()
        header_layout.addLayout(meta_layout)

    def init_db(self):
        """
        Khởi tạo kết nối đến cơ sở dữ liệu SQLite và tạo bảng nếu chưa tồn tại.
        """
        try:
            self.db_connection = sqlite3.connect(DB_NAME)
            self.db_cursor = self.db_connection.cursor()
            
            # Tạo bảng 'pages' với nhiều trường hơn
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS pages (
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
                )
            """)
            
            # Migrate existing database if needed
            self.migrate_database()
            
            # Cache table schemas for performance
            self._cache_table_schemas()
            
            # Tạo bảng 'blocks' cho hệ thống block-based content
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    content TEXT,
                    properties TEXT,
                    position INTEGER DEFAULT 0,
                    parent_block_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (page_id) REFERENCES pages (id),
                    FOREIGN KEY (parent_block_id) REFERENCES blocks (id)
                )
            """)
            
            # Tạo bảng 'templates' cho các template có sẵn
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    content TEXT,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for better performance
            self.db_cursor.execute("CREATE INDEX IF NOT EXISTS idx_pages_updated_at ON pages(updated_at)")
            self.db_cursor.execute("CREATE INDEX IF NOT EXISTS idx_pages_parent_id ON pages(parent_id)")
            self.db_cursor.execute("CREATE INDEX IF NOT EXISTS idx_pages_is_favorite ON pages(is_favorite)")
            
            self.db_connection.commit()
        except sqlite3.Error as e:
            self.show_error_message("Lỗi cơ sở dữ liệu", f"Không thể kết nối hoặc tạo bảng: {e}")
            sys.exit(1)

    def _cache_table_schemas(self):
        """Cache table schemas để tránh PRAGMA queries lặp lại."""
        tables = ['pages', 'templates', 'blocks']
        for table in tables:
            try:
                self.db_cursor.execute(f"PRAGMA table_info({table})")
                columns = [column[1] for column in self.db_cursor.fetchall()]
                self._table_schema_cache[table] = columns
            except sqlite3.Error:
                self._table_schema_cache[table] = []

    def _get_table_columns(self, table_name):
        """Lấy danh sách columns từ cache thay vì query database."""
        if table_name not in self._table_schema_cache:
            try:
                self.db_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [column[1] for column in self.db_cursor.fetchall()]
                self._table_schema_cache[table_name] = columns
            except sqlite3.Error:
                self._table_schema_cache[table_name] = []
        return self._table_schema_cache[table_name]

    def migrate_database(self):
        """Migration database schema từ version cũ."""
        try:
            # Get current table structure
            self.db_cursor.execute("PRAGMA table_info(pages)")
            columns = [column[1] for column in self.db_cursor.fetchall()]
            
            # Add missing columns if they don't exist
            migrations = [
                ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
                ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
                ("parent_id", "INTEGER"),
                ("icon", "TEXT"),
                ("cover_image", "TEXT"),
                ("is_favorite", "BOOLEAN DEFAULT 0"),
                ("is_template", "BOOLEAN DEFAULT 0"),
                ("tags", "TEXT")
            ]
            
            for column_name, column_def in migrations:
                if column_name not in columns:
                    try:
                        self.db_cursor.execute(f"ALTER TABLE pages ADD COLUMN {column_name} {column_def}")
                        print(f"✅ Added column: {column_name}")
                    except sqlite3.Error as e:
                        print(f"⚠️ Could not add column {column_name}: {e}")
            
            # Update existing records with default timestamps if they're null
            self.db_cursor.execute("""
                UPDATE pages 
                SET created_at = CURRENT_TIMESTAMP 
                WHERE created_at IS NULL
            """)
            
            self.db_cursor.execute("""
                UPDATE pages 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE updated_at IS NULL
            """)
            
            self.db_connection.commit()
            
            # Refresh cache after migration
            self._cache_table_schemas()
            
            print("✅ Database migration completed")
            
        except sqlite3.Error as e:
            print(f"⚠️ Migration warning: {e}")
            # Don't fail completely on migration issues

    def load_pages_from_db(self, preserve_selection=True):
        """Tải danh sách các trang từ cơ sở dữ liệu và hiển thị lên sidebar."""
        if self._is_loading:
            return
            
        self._is_loading = True
        
        # Preserve current selection
        current_page_id = None
        if preserve_selection:
            current_item = self.pages_list_widget.currentItem()
            if current_item:
                current_page_id = current_item.data(0, Qt.UserRole)
        
        self.pages_list_widget.clear()
        
        try:
            # Use cached column information
            columns = self._get_table_columns('pages')
            
            # Build optimized query with only necessary columns
            base_query = "SELECT id, title"
            additional_fields = []
            
            if 'icon' in columns:
                additional_fields.append('icon')
            else:
                additional_fields.append("'📄' as icon")
                
            if 'updated_at' in columns:
                additional_fields.append('updated_at')
            elif 'created_at' in columns:
                additional_fields.append('created_at as updated_at')
            else:
                additional_fields.append("'N/A' as updated_at")
                
            if 'is_favorite' in columns:
                additional_fields.append('is_favorite')
            else:
                additional_fields.append('0 as is_favorite')
                
            if 'parent_id' in columns:
                additional_fields.append('parent_id')
            else:
                additional_fields.append('NULL as parent_id')
            
            query = f"{base_query}, {', '.join(additional_fields)} FROM pages WHERE title IS NOT NULL"
            
            # Add optimized ordering using indexes
            if 'is_favorite' in columns and 'updated_at' in columns:
                query += " ORDER BY is_favorite DESC, updated_at DESC"
            elif 'updated_at' in columns:
                query += " ORDER BY updated_at DESC"
            elif 'created_at' in columns:
                query += " ORDER BY created_at DESC"
            else:
                query += " ORDER BY id DESC"
            
            self.db_cursor.execute(query)
            pages = self.db_cursor.fetchall()
            
            # Group pages by parent_id for efficient tree building
            root_pages = []
            child_pages = {}
            
            for page_data in pages:
                page_id, title = page_data[0], page_data[1]
                icon = page_data[2] if len(page_data) > 2 else "📄"
                updated_at = page_data[3] if len(page_data) > 3 else "N/A"
                is_favorite = bool(page_data[4]) if len(page_data) > 4 else False
                parent_id = page_data[5] if len(page_data) > 5 else None
                
                page_info = {
                    'id': page_id,
                    'title': title,
                    'icon': icon or "📄",
                    'updated_at': updated_at,
                    'is_favorite': is_favorite
                }
                
                if parent_id is None:
                    root_pages.append(page_info)
                else:
                    if parent_id not in child_pages:
                        child_pages[parent_id] = []
                    child_pages[parent_id].append(page_info)
            
            # Build tree efficiently
            for page in root_pages:
                item = self._create_page_item(page)
                self.pages_list_widget.addTopLevelItem(item)
                
                # Add children if any
                if page['id'] in child_pages:
                    for child in child_pages[page['id']]:
                        child_item = self._create_page_item(child)
                        item.addChild(child_item)
            
            # Restore selection if requested
            if preserve_selection and current_page_id:
                self.find_and_select_page(current_page_id)
                
        except sqlite3.Error as e:
            self.show_error_message("Lỗi tải trang", f"Không thể tải danh sách trang: {e}")
            # Add fallback message
            item = QTreeWidgetItem()
            item.setText(0, "❌ Lỗi tải dữ liệu")
            item.setText(1, "Hãy tạo page mới")
            self.pages_list_widget.addTopLevelItem(item)
        finally:
            self._is_loading = False

    def _create_page_item(self, page_info):
        """Tạo QTreeWidgetItem từ page info với format tối ưu."""
        item = QTreeWidgetItem()
        
        # Format display text
        favorite_indicator = "⭐ " if page_info['is_favorite'] else ""
        item.setText(0, f"{page_info['icon']} {favorite_indicator}{page_info['title']}")
        
        # Format date display efficiently
        date_display = ""
        if page_info['updated_at'] and page_info['updated_at'] != 'N/A':
            if len(page_info['updated_at']) >= 10:
                date_display = page_info['updated_at'][:10]
            else:
                date_display = page_info['updated_at']
        else:
            date_display = "N/A"
            
        item.setText(1, date_display)
        item.setData(0, Qt.UserRole, page_info['id'])
        
        return item

    def page_selection_changed(self, current_item, previous_item):
        """
        Được gọi khi người dùng chọn một trang khác trong danh sách.
        Tải nội dung của trang được chọn vào editor với progress indicator.
        """
        if current_item is None:
            self.clear_editor()
            return

        new_page_id = current_item.data(0, Qt.UserRole)
        if new_page_id is None:
            return
            
        # Avoid reloading same page
        if new_page_id == self.current_page_id:
            return
            
        self.current_page_id = new_page_id
        
        # Hiển thị loading state
        self.status_bar.showMessage("📂 Đang tải trang...")
        self.editor_widget.setEnabled(False)
        
        try:
            # Use cached column information for faster query
            columns = self._get_table_columns('pages')
            
            # Build optimized query with only needed columns
            base_query = "SELECT title, content"
            additional_fields = []
            
            if 'icon' in columns:
                additional_fields.append('icon')
            else:
                additional_fields.append("'📄' as icon")
                
            if 'is_favorite' in columns:
                additional_fields.append('is_favorite')
            else:
                additional_fields.append('0 as is_favorite')
                
            if 'tags' in columns:
                additional_fields.append('tags')
            else:
                additional_fields.append("'' as tags")
                
            if 'created_at' in columns:
                additional_fields.append('created_at')
            else:
                additional_fields.append("'N/A' as created_at")
                
            if 'updated_at' in columns:
                additional_fields.append('updated_at')
            else:
                additional_fields.append("'N/A' as updated_at")
            
            query = f"{base_query}, {', '.join(additional_fields)} FROM pages WHERE id = ?"
            
            self.db_cursor.execute(query, (self.current_page_id,))
            result = self.db_cursor.fetchone()
            
            if result:
                title = result[0] or "Untitled"
                content = result[1] or ""
                icon = result[2] if len(result) > 2 else "📄"
                is_favorite = bool(result[3]) if len(result) > 3 else False
                tags = result[4] if len(result) > 4 else ""
                created_at = result[5] if len(result) > 5 else "N/A"
                updated_at = result[6] if len(result) > 6 else "N/A"
                
                # Update page header efficiently
                self.page_title_edit.blockSignals(True)
                self.page_title_edit.setText(title)
                self.page_title_edit.blockSignals(False)
                
                self.page_icon_label.setText(icon or "📄")
                self.favorite_checkbox.setChecked(is_favorite)
                self.tags_edit.setText(tags)
                
                # Update editor content efficiently
                self.editor_widget.blockSignals(True)
                self.editor_widget.setHtml(content)
                self.editor_widget.blockSignals(False)
                self.editor_widget.setEnabled(True)
                
                # Store current content for auto-save comparison
                self._last_saved_content = content
                
                # Update status bar với thông tin chi tiết
                word_count = len(content.split()) if content else 0
                char_count = len(content) if content else 0
                self.status_bar.showMessage(
                    f"📖 {title} | Tạo: {created_at[:10] if created_at != 'N/A' else 'N/A'} | "
                    f"Sửa: {updated_at[:10] if updated_at != 'N/A' else 'N/A'} | "
                    f"📝 {word_count} từ, {char_count} ký tự"
                )
                
            else:
                self.clear_editor()
                self.status_bar.showMessage("❌ Không tìm thấy nội dung trang", 3000)
                
        except sqlite3.Error as e:
            self.show_error_message("Lỗi tải nội dung", f"Không thể tải nội dung trang: {e}")
            self.clear_editor()
            self.status_bar.showMessage("❌ Lỗi tải trang", 3000)

    def clear_editor(self):
        """Xóa nội dung editor với performance tối ưu."""
        self.editor_widget.clear()
        self.editor_widget.setEnabled(False)
        self.current_page_id = None
        self._last_saved_content = ""
        self._last_saved_title = ""
        
        # Clear UI efficiently
        self.page_title_edit.clear()
        self.page_icon_label.setText("📄")
        self.favorite_checkbox.setChecked(False)
        self.tags_edit.clear()
        
        # Stop auto-save timer if running
        if self._auto_save_timer is not None:
            self._auto_save_timer.stop()

    # --- New Methods for Enhanced Functionality ---

    def filter_pages(self, text):
        """Lọc pages theo text tìm kiếm nâng cao."""
        if not text.strip():
            # Hiển thị tất cả nếu search rỗng
            for i in range(self.pages_list_widget.topLevelItemCount()):
                item = self.pages_list_widget.topLevelItem(i)
                item.setHidden(False)
                # Hiển thị cả children
                for j in range(item.childCount()):
                    item.child(j).setHidden(False)
            return
        
        search_text = text.lower()
        visible_count = 0
        
        for i in range(self.pages_list_widget.topLevelItemCount()):
            item = self.pages_list_widget.topLevelItem(i)
            item_text = item.text(0).lower()
            
            # Tìm trong title
            title_match = search_text in item_text
            
            # Tìm trong content (nếu có page_id)
            content_match = False
            page_id = item.data(0, Qt.UserRole)
            if page_id:
                try:
                    self.db_cursor.execute("SELECT content FROM pages WHERE id = ?", (page_id,))
                    result = self.db_cursor.fetchone()
                    if result and result[0]:
                        # Remove HTML tags để search trong plain text
                        import re
                        plain_content = re.sub('<[^<]+?>', '', result[0]).lower()
                        content_match = search_text in plain_content
                except:
                    pass
            
            # Kiểm tra children
            child_visible = False
            for j in range(item.childCount()):
                child = item.child(j)
                child_text = child.text(0).lower()
                child_match = search_text in child_text
                child.setHidden(not child_match)
                if child_match:
                    child_visible = True
            
            # Hiển thị item nếu match hoặc có child visible
            item_visible = title_match or content_match or child_visible
            item.setHidden(not item_visible)
            
            if item_visible:
                visible_count += 1
        
        # Hiển thị kết quả search
        if visible_count == 0:
            self.status_bar.showMessage(f"🔍 Không tìm thấy kết quả cho: '{text}'", 3000)
        else:
            self.status_bar.showMessage(f"🔍 Tìm thấy {visible_count} kết quả cho: '{text}'", 2000)

    def create_new_folder(self):
        """Tạo folder mới với performance tối ưu."""
        title, ok = QInputDialog.getText(self, "Folder mới", "Nhập tên folder:")
        if ok and title:
            try:
                # Use cached column information
                columns = self._get_table_columns('pages')
                
                # Build optimized insert query
                base_columns = ["title", "content", "icon"]
                base_values = [title, "", "📁"]
                
                if 'is_template' in columns:
                    base_columns.append("is_template")
                    base_values.append(False)
                    
                if 'created_at' in columns:
                    base_columns.append("created_at")
                    base_values.append("CURRENT_TIMESTAMP")
                    
                if 'updated_at' in columns:
                    base_columns.append("updated_at")
                    base_values.append("CURRENT_TIMESTAMP")
                
                # Create placeholders efficiently
                placeholders = []
                insert_values = []
                for value in base_values:
                    if value == "CURRENT_TIMESTAMP":
                        placeholders.append("CURRENT_TIMESTAMP")
                    else:
                        placeholders.append("?")
                        insert_values.append(value)
                
                query = f"""
                    INSERT INTO pages ({', '.join(base_columns)}) 
                    VALUES ({', '.join(placeholders)})
                """
                
                self.db_cursor.execute(query, insert_values)
                folder_id = self.db_cursor.lastrowid
                self.db_connection.commit()
                
                # Optimized reload with selection
                self.load_pages_from_db(preserve_selection=False)
                self.find_and_select_page(folder_id)
                
                self.status_bar.showMessage(f"📁 Đã tạo folder: {title}", 2000)
                
            except sqlite3.Error as e:
                self.show_error_message("Lỗi tạo folder", f"Không thể tạo folder: {e}")

    def toggle_sidebar(self):
        """Ẩn/hiện sidebar."""
        self.sidebar_widget.setVisible(not self.sidebar_widget.isVisible())

    def change_font_family(self, font_family):
        """Thay đổi font family."""
        if hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            char_format = QTextCharFormat()
            char_format.setFontFamily(font_family)
            cursor.mergeCharFormat(char_format)

    def change_font_size(self, size):
        """Thay đổi font size."""
        if hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            char_format = QTextCharFormat()
            char_format.setFontPointSize(size)
            cursor.mergeCharFormat(char_format)

    def change_text_color(self):
        """Thay đổi màu chữ."""
        color = QColorDialog.getColor()
        if color.isValid() and hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            char_format = QTextCharFormat()
            char_format.setForeground(QBrush(color))
            cursor.mergeCharFormat(char_format)

    def change_background_color(self):
        """Thay đổi màu nền."""
        color = QColorDialog.getColor()
        if color.isValid() and hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            char_format = QTextCharFormat()
            char_format.setBackground(QBrush(color))
            cursor.mergeCharFormat(char_format)

    def insert_bullet_list(self):
        """Chèn bullet list."""
        if hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            list_format = QTextListFormat()
            list_format.setStyle(QTextListFormat.ListDisc)
            cursor.insertList(list_format)

    def insert_number_list(self):
        """Chèn numbered list."""
        if hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            list_format = QTextListFormat()
            list_format.setStyle(QTextListFormat.ListDecimal)
            cursor.insertList(list_format)

    def insert_table(self):
        """Chèn bảng."""
        rows, ok1 = QInputDialog.getInt(self, "Chèn bảng", "Số hàng:", 3, 1, 20)
        if ok1:
            cols, ok2 = QInputDialog.getInt(self, "Chèn bảng", "Số cột:", 3, 1, 10)
            if ok2 and hasattr(self, 'editor_widget'):
                cursor = self.editor_widget.textCursor()
                table_format = cursor.insertTable(rows, cols)

    def insert_image(self):
        """Chèn hình ảnh."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn hình ảnh", "", 
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path and hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            image = QPixmap(file_path)
            if not image.isNull():
                # Scale image if too large
                if image.width() > 600:
                    image = image.scaledToWidth(600, Qt.SmoothTransformation)
                cursor.insertImage(image.toImage())

    def insert_link(self):
        """Chèn liên kết."""
        url, ok = QInputDialog.getText(self, "Chèn liên kết", "URL:")
        if ok and url and hasattr(self, 'editor_widget'):
            cursor = self.editor_widget.textCursor()
            if cursor.hasSelection():
                text = cursor.selectedText()
            else:
                text = url
            
            char_format = QTextCharFormat()
            char_format.setAnchor(True)
            char_format.setAnchorHref(url)
            char_format.setForeground(QColor("blue"))
            char_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
            
            cursor.insertText(text, char_format)

    def on_text_changed(self):
        """Xử lý khi text thay đổi với auto-save thông minh và debounced."""
        if hasattr(self, 'current_page_id') and self.current_page_id:
            # Get current content efficiently
            current_content = self.editor_widget.toHtml()
            
            # Quick check if content actually changed
            if current_content == self._last_saved_content:
                return
            
            # Cancel existing timer to debounce
            if self._auto_save_timer is not None:
                self._auto_save_timer.stop()
            else:
                self._auto_save_timer = QTimer()
                self._auto_save_timer.timeout.connect(self.auto_save)
                self._auto_save_timer.setSingleShot(True)
            
            # Debounced auto-save - only trigger after 1.5 seconds of no typing
            self._auto_save_timer.start(1500)
            
            # Update status immediately for better UX
            if hasattr(self, 'current_page_id'):
                title = self.page_title_edit.text() or "Untitled"
                self.status_bar.showMessage(f"📝 Đang chỉnh sửa: {title}...", 1000)

    def auto_save(self):
        """Tự động lưu với feedback tối ưu."""
        if hasattr(self, 'current_page_id') and self.current_page_id:
            try:
                current_content = self.editor_widget.toHtml()
                
                # Double-check if content changed before saving
                if current_content == self._last_saved_content:
                    return
                
                self.save_current_page(show_message=False)
                self._last_saved_content = current_content
                
                # Show brief save confirmation
                title = self.page_title_edit.text() or "Untitled"
                self.status_bar.showMessage(f"💾 Đã lưu: {title}", 1500)
                
            except Exception as e:
                self.status_bar.showMessage(f"❌ Lỗi auto-save: {str(e)}", 3000)

    def update_page_title(self):
        """Cập nhật title của page với validation tối ưu."""
        if hasattr(self, 'current_page_id') and self.current_page_id:
            new_title = self.page_title_edit.text().strip()
            
            # Validation
            if not new_title:
                self.page_title_edit.setText("Untitled")
                new_title = "Untitled"
            
            try:
                # Use cached column information
                columns = self._get_table_columns('pages')
                
                if 'updated_at' in columns:
                    self.db_cursor.execute("""
                        UPDATE pages SET title = ?, updated_at = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (new_title, self.current_page_id))
                else:
                    self.db_cursor.execute("""
                        UPDATE pages SET title = ? WHERE id = ?
                    """, (new_title, self.current_page_id))
                
                self.db_connection.commit()
                
                # Optimized reload - preserve selection
                self.load_pages_from_db(preserve_selection=True)
                
                # Show feedback
                self.status_bar.showMessage(f"✅ Đã cập nhật title: '{new_title}'", 2000)
                
            except sqlite3.Error as e:
                self.show_error_message("Lỗi cập nhật", f"Không thể cập nhật title: {e}")
                # Revert to original title
                try:
                    self.db_cursor.execute("SELECT title FROM pages WHERE id = ?", (self.current_page_id,))
                    result = self.db_cursor.fetchone()
                    if result:
                        self.page_title_edit.blockSignals(True)
                        self.page_title_edit.setText(result[0])
                        self.page_title_edit.blockSignals(False)
                except:
                    pass

    def toggle_favorite(self, state):
        """Toggle favorite status với performance tối ưu."""
        if hasattr(self, 'current_page_id') and self.current_page_id:
            try:
                # Use cached column information
                columns = self._get_table_columns('pages')
                
                if 'is_favorite' in columns and 'updated_at' in columns:
                    self.db_cursor.execute("""
                        UPDATE pages SET is_favorite = ?, updated_at = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (state == 2, self.current_page_id))
                elif 'is_favorite' in columns:
                    self.db_cursor.execute("""
                        UPDATE pages SET is_favorite = ? WHERE id = ?
                    """, (state == 2, self.current_page_id))
                else:
                    # Column doesn't exist, just return
                    return
                    
                self.db_connection.commit()
                
                # Optimized reload with selection preservation
                self.load_pages_from_db(preserve_selection=True)
                
            except sqlite3.Error as e:
                self.show_error_message("Lỗi cập nhật", f"Không thể cập nhật favorite: {e}")

    def update_tags(self):
        """Cập nhật tags với performance tối ưu."""
        if hasattr(self, 'current_page_id') and self.current_page_id:
            tags = self.tags_edit.text()
            try:
                # Use cached column information
                columns = self._get_table_columns('pages')
                
                if 'tags' in columns and 'updated_at' in columns:
                    self.db_cursor.execute("""
                        UPDATE pages SET tags = ?, updated_at = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (tags, self.current_page_id))
                elif 'tags' in columns:
                    self.db_cursor.execute("""
                        UPDATE pages SET tags = ? WHERE id = ?
                    """, (tags, self.current_page_id))
                else:
                    # Tags column doesn't exist, just return
                    return
                    
                self.db_connection.commit()
            except sqlite3.Error as e:
                self.show_error_message("Lỗi cập nhật", f"Không thể cập nhật tags: {e}")

    def load_templates(self):
        """Load templates."""
        try:
            self.db_cursor.execute("SELECT name, description FROM templates ORDER BY name")
            templates = self.db_cursor.fetchall()
            for name, description in templates:
                item = QListWidgetItem(f"{name}\n{description}")
                self.templates_list.addItem(item)
                
            # Add default templates if none exist
            if not templates:
                self.create_default_templates()
                self.load_templates()
                
        except sqlite3.Error as e:
            self.show_error_message("Lỗi load templates", f"Không thể load templates: {e}")

    def create_default_templates(self):
        """Tạo các template mặc định."""
        default_templates = [
            ("Meeting Notes", "Template for meeting notes", """
                <h1>Meeting Notes</h1>
                <p><strong>Date:</strong> {date}</p>
                <p><strong>Attendees:</strong> </p>
                <p><strong>Agenda:</strong></p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
                <p><strong>Action Items:</strong></p>
                <ul>
                    <li>[ ] Task 1</li>
                    <li>[ ] Task 2</li>
                </ul>
            """, "Work"),
            ("Daily Journal", "Personal daily journal template", """
                <h1>Daily Journal - {date}</h1>
                <h2>Today's Goals</h2>
                <ul>
                    <li>Goal 1</li>
                    <li>Goal 2</li>
                </ul>
                <h2>What happened today?</h2>
                <p>Write about your day...</p>
                <h2>Reflection</h2>
                <p>What did you learn?</p>
            """, "Personal"),
            ("Project Plan", "Project planning template", """
                <h1>Project Plan</h1>
                <p><strong>Project Name:</strong> </p>
                <p><strong>Timeline:</strong> </p>
                <p><strong>Team Members:</strong> </p>
                <h2>Objectives</h2>
                <ul>
                    <li>Objective 1</li>
                    <li>Objective 2</li>
                </ul>
                <h2>Milestones</h2>
                <ul>
                    <li>Milestone 1 - Date</li>
                    <li>Milestone 2 - Date</li>
                </ul>
            """, "Work")
        ]
        
        try:
            for name, description, content, category in default_templates:
                self.db_cursor.execute("""
                    INSERT INTO templates (name, description, content, category)
                    VALUES (?, ?, ?, ?)
                """, (name, description, content, category))
            self.db_connection.commit()
        except sqlite3.Error as e:
            self.show_error_message("Lỗi tạo templates", f"Không thể tạo templates: {e}")

    def use_template(self):
        """Sử dụng template được chọn và tạo page mới."""
        current_item = self.templates_list.currentItem()
        if current_item:
            template_name = current_item.text().split('\n')[0]
            try:
                self.db_cursor.execute("""
                    SELECT content FROM templates WHERE name = ?
                """, (template_name,))
                result = self.db_cursor.fetchone()
                
                if result:
                    content = result[0]
                    # Replace placeholders với thông tin thực tế
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    current_time = datetime.now().strftime('%H:%M')
                    content = content.replace('{date}', current_date)
                    content = content.replace('{time}', current_time)
                    content = content.replace('{datetime}', f"{current_date} {current_time}")
                    
                    # Tạo page mới từ template
                    page_title = f"New {template_name} - {current_date}"
                    
                    # Check which columns exist before inserting
                    self.db_cursor.execute("PRAGMA table_info(pages)")
                    columns = [column[1] for column in self.db_cursor.fetchall()]
                    
                    # Build dynamic insert query
                    base_columns = ["title", "content", "icon"]
                    base_values = [page_title, content, "📋"]
                    
                    if 'is_template' in columns:
                        base_columns.append("is_template")
                        base_values.append(False)
                        
                    if 'created_at' in columns:
                        base_columns.append("created_at")
                        base_values.append("CURRENT_TIMESTAMP")
                        
                    if 'updated_at' in columns:
                        base_columns.append("updated_at")
                        base_values.append("CURRENT_TIMESTAMP")
                    
                    # Create placeholders for values
                    placeholders = []
                    insert_values = []
                    for value in base_values:
                        if value == "CURRENT_TIMESTAMP":
                            placeholders.append("CURRENT_TIMESTAMP")
                        else:
                            placeholders.append("?")
                            insert_values.append(value)
                    
                    query = f"""
                        INSERT INTO pages ({', '.join(base_columns)}) 
                        VALUES ({', '.join(placeholders)})
                    """
                    
                    self.db_cursor.execute(query, insert_values)
                    page_id = self.db_cursor.lastrowid
                    self.db_connection.commit()
                    
                    # Reload và select page mới
                    self.load_pages_from_db()
                    self.find_and_select_page(page_id)
                    
                    self.status_bar.showMessage(f"✅ Đã tạo page từ template: {template_name}", 3000)
                    
            except sqlite3.Error as e:
                self.show_error_message("Lỗi sử dụng template", f"Không thể sử dụng template: {e}")

    def load_recent_pages(self):
        """Load recent pages."""
        try:
            # Check if updated_at column exists
            self.db_cursor.execute("PRAGMA table_info(pages)")
            columns = [column[1] for column in self.db_cursor.fetchall()]
            
            if 'updated_at' in columns:
                # Use updated_at if available
                self.db_cursor.execute("""
                    SELECT title, updated_at FROM pages 
                    WHERE title IS NOT NULL
                    ORDER BY updated_at DESC LIMIT 10
                """)
            else:
                # Fallback to created_at or id if updated_at doesn't exist
                if 'created_at' in columns:
                    self.db_cursor.execute("""
                        SELECT title, created_at as updated_at FROM pages 
                        WHERE title IS NOT NULL
                        ORDER BY created_at DESC LIMIT 10
                    """)
                else:
                    # Fallback to id ordering
                    self.db_cursor.execute("""
                        SELECT title, 'N/A' as updated_at FROM pages 
                        WHERE title IS NOT NULL
                        ORDER BY id DESC LIMIT 10
                    """)
            
            recent = self.db_cursor.fetchall()
            
            for title, updated_at in recent:
                display_time = updated_at[:10] if updated_at and updated_at != 'N/A' else 'N/A'
                item = QListWidgetItem(f"{title}\n{display_time}")
                item.setData(Qt.UserRole, title)  # Store title for potential selection
                self.recent_list.addItem(item)
                
        except sqlite3.Error as e:
            self.show_error_message("Lỗi load recent", f"Không thể load recent pages: {e}")
            # Add a default message if loading fails
            item = QListWidgetItem("Không có dữ liệu recent\nHãy tạo page đầu tiên!")
            self.recent_list.addItem(item)

    def close_editor_tab(self, index):
        """Đóng tab editor."""
        if self.editor_tabs.count() > 1:
            self.editor_tabs.removeTab(index)

    # Menu actions
    def open_file(self):
        """Mở file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "HTML Files (*.html);;Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor_widget.setHtml(content)
            except Exception as e:
                self.show_error_message("Lỗi mở file", f"Không thể mở file: {e}")

    def export_page(self):
        """Xuất page."""
        if hasattr(self, 'current_page_id') and self.current_page_id:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Page", "", "HTML Files (*.html);;PDF Files (*.pdf);;Text Files (*.txt)"
            )
            if file_path:
                try:
                    content = self.editor_widget.toHtml()
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    self.status_bar.showMessage(f"Exported to {file_path}")
                except Exception as e:
                    self.show_error_message("Lỗi xuất file", f"Không thể xuất file: {e}")

    def undo(self):
        """Hoàn tác."""
        if hasattr(self, 'editor_widget'):
            self.editor_widget.undo()

    def redo(self):
        """Làm lại."""
        if hasattr(self, 'editor_widget'):
            self.editor_widget.redo()

    def copy(self):
        """Sao chép."""
        if hasattr(self, 'editor_widget'):
            self.editor_widget.copy()

    def paste(self):
        """Dán."""
        if hasattr(self, 'editor_widget'):
            self.editor_widget.paste()

    def create_new_page(self):
        """Hỏi người dùng tên trang mới và tạo nó trong cơ sở dữ liệu với performance tối ưu."""
        title, ok = QInputDialog.getText(self, "Trang mới", "Nhập tiêu đề cho trang mới:")
        if ok and title:
            try:
                # Get parent_id if a folder is selected
                parent_id = None
                current_item = self.pages_list_widget.currentItem()
                if current_item:
                    # Check if current item is a folder
                    potential_parent_id = current_item.data(0, Qt.UserRole)
                    if potential_parent_id:
                        self.db_cursor.execute("SELECT icon FROM pages WHERE id = ?", (potential_parent_id,))
                        result = self.db_cursor.fetchone()
                        if result and result[0] == "📁":
                            parent_id = potential_parent_id

                # Use cached column information
                columns = self._get_table_columns('pages')
                
                # Build optimized insert query
                base_columns = ["title", "content", "icon"]
                base_values = [title, "", "📄"]
                
                if 'parent_id' in columns:
                    base_columns.append("parent_id")
                    base_values.append(parent_id)
                    
                if 'created_at' in columns:
                    base_columns.append("created_at")
                    base_values.append("CURRENT_TIMESTAMP")
                    
                if 'updated_at' in columns:
                    base_columns.append("updated_at")
                    base_values.append("CURRENT_TIMESTAMP")
                
                # Create placeholders efficiently
                placeholders = []
                insert_values = []
                for value in base_values:
                    if value == "CURRENT_TIMESTAMP":
                        placeholders.append("CURRENT_TIMESTAMP")
                    else:
                        placeholders.append("?")
                        insert_values.append(value)
                
                query = f"""
                    INSERT INTO pages ({', '.join(base_columns)}) 
                    VALUES ({', '.join(placeholders)})
                """
                
                self.db_cursor.execute(query, insert_values)
                page_id = self.db_cursor.lastrowid
                self.db_connection.commit()
                
                # Optimized reload and select
                self.load_pages_from_db(preserve_selection=False)
                self.find_and_select_page(page_id)
                
                self.status_bar.showMessage(f"📄 Đã tạo page: {title}", 2000)
                
            except sqlite3.Error as e:
                self.show_error_message("Lỗi tạo trang", f"Không thể tạo trang mới: {e}")

    def find_and_select_page(self, page_id):
        """Tìm và chọn page theo ID."""
        def search_item(item):
            if item.data(0, Qt.UserRole) == page_id:
                self.pages_list_widget.setCurrentItem(item)
                return True
            for i in range(item.childCount()):
                if search_item(item.child(i)):
                    return True
            return False

        for i in range(self.pages_list_widget.topLevelItemCount()):
            if search_item(self.pages_list_widget.topLevelItem(i)):
                break

    def save_current_page(self, show_message=True):
        """Lưu nội dung hiện tại của editor vào cơ sở dữ liệu với performance tối ưu."""
        if not hasattr(self, 'current_page_id') or self.current_page_id is None:
            return
            
        content_html = self.editor_widget.toHtml()
        title = self.page_title_edit.text() or "Untitled"
        tags = self.tags_edit.text()
        is_favorite = self.favorite_checkbox.isChecked()
        
        try:
            # Use cached column information
            columns = self._get_table_columns('pages')
            
            # Build optimized update query
            update_fields = ["content = ?", "title = ?"]
            update_values = [content_html, title]
            
            if 'tags' in columns:
                update_fields.append("tags = ?")
                update_values.append(tags)
                
            if 'is_favorite' in columns:
                update_fields.append("is_favorite = ?")
                update_values.append(is_favorite)
                
            if 'updated_at' in columns:
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
            
            update_values.append(self.current_page_id)
            
            query = f"""
                UPDATE pages 
                SET {', '.join(update_fields)}
                WHERE id = ?
            """
            
            self.db_cursor.execute(query, update_values)
            self.db_connection.commit()
            
            if show_message:
                self.status_bar.showMessage(f"💾 Đã lưu: {title}", 1500)
                
            # Only reload pages if title changed for better performance
            if hasattr(self, '_last_saved_title') and self._last_saved_title != title:
                self.load_pages_from_db(preserve_selection=True)
            
            self._last_saved_title = title
            
        except sqlite3.Error as e:
            self.show_error_message("Lỗi lưu trang", f"Không thể lưu nội dung: {e}")

    # --- Các hàm định dạng văn bản ---
    def make_text_bold(self):
        weight = self.editor_widget.fontWeight()
        self.editor_widget.setFontWeight(QFont.Bold if weight != QFont.Bold else QFont.Normal)

    def make_text_italic(self):
        self.editor_widget.setFontItalic(not self.editor_widget.fontItalic())

    def make_text_underline(self):
        self.editor_widget.setFontUnderline(not self.editor_widget.fontUnderline())

    # --- Hàm tiện ích ---
    def show_error_message(self, title, message):
        """Hiển thị một hộp thoại thông báo lỗi."""
        QMessageBox.critical(self, title, message)

    def _create_app_icon(self):
        """Tạo icon cho ứng dụng bằng cách vẽ SVG (không cần file ngoài)."""
        svg_data = """
        <svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <rect width="64" height="64" rx="12" fill="#333740"/>
          <path d="M20 16H44V24H36V48H28V24H20V16Z" fill="white"/>
        </svg>
        """
        renderer = QSvgRenderer(bytearray(svg_data, 'utf-8'))
        pixmap = QPixmap(QSize(64, 64))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def closeEvent(self, event):
        """Đảm bảo kết nối cơ sở dữ liệu được đóng khi thoát ứng dụng."""
        if self.db_connection:
            self.db_connection.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply basic styling
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QPushButton {
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1976d2;
        }
        QTextEdit {
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 16px;
            font-size: 14px;
        }
        QTreeWidget {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            selection-background-color: #e3f2fd;
        }
        QTabWidget::pane {
            border: 1px solid #e0e0e0;
            background-color: #fafafa;
        }
        QTabBar::tab {
            background-color: #f5f5f5;
            border: 1px solid #d0d0d0;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 80px;
            padding: 8px 12px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #ffffff;
            border-color: #e0e0e0;
        }
    """)
    
    # Set application metadata
    app.setApplicationName("Notion Clone")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Your Company")
    
    # Create and show main window
    window = NotionCloneApp()
    window.show()
    
    # Show welcome message
    window.status_bar.showMessage("Chào mừng đến với Notion Clone! Hãy tạo trang đầu tiên của bạn.", 5000)
    
    sys.exit(app.exec())
