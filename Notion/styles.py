"""
CSS Styles cho Notion Clone Application
"""

MAIN_STYLES = """
QMainWindow {
    background-color: #ffffff;
    color: #333333;
}

/* Sidebar Styles */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    background-color: #fafafa;
}

QTabWidget::tab-bar {
    alignment: center;
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

QTabBar::tab:hover {
    background-color: #eeeeee;
}

/* Tree Widget Styles */
QTreeWidget {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    selection-background-color: #e3f2fd;
    font-size: 13px;
}

QTreeWidget::item {
    padding: 6px;
    border-bottom: 1px solid #f0f0f0;
}

QTreeWidget::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}

QTreeWidget::item:hover {
    background-color: #f5f5f5;
}

/* List Widget Styles */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    selection-background-color: #e3f2fd;
    font-size: 13px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #f0f0f0;
}

QListWidget::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}

QListWidget::item:hover {
    background-color: #f5f5f5;
}

/* Button Styles */
QPushButton {
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1976d2;
}

QPushButton:pressed {
    background-color: #1565c0;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

/* Secondary Button */
QPushButton[class="secondary"] {
    background-color: #f5f5f5;
    color: #333333;
    border: 1px solid #d0d0d0;
}

QPushButton[class="secondary"]:hover {
    background-color: #eeeeee;
}

/* Text Edit Styles */
QTextEdit {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    padding: 16px;
}

QTextEdit:focus {
    border-color: #2196f3;
    outline: none;
}

/* Line Edit Styles */
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #2196f3;
    outline: none;
}

/* ComboBox Styles */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
    min-width: 100px;
}

QComboBox:hover {
    border-color: #b0b0b0;
}

QComboBox:focus {
    border-color: #2196f3;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    selection-background-color: #e3f2fd;
}

/* Toolbar Styles */
QToolBar {
    background-color: #f8f9fa;
    border: none;
    border-bottom: 1px solid #e0e0e0;
    spacing: 4px;
    padding: 4px;
}

QToolBar QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 6px;
    margin: 2px;
    font-size: 12px;
}

QToolBar QToolButton:hover {
    background-color: #e0e0e0;
    border-color: #b0b0b0;
}

QToolBar QToolButton:pressed {
    background-color: #d0d0d0;
}

QToolBar QToolButton:checked {
    background-color: #2196f3;
    color: white;
}

/* SpinBox Styles */
QSpinBox {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 13px;
    min-width: 60px;
}

QSpinBox:focus {
    border-color: #2196f3;
}

/* CheckBox Styles */
QCheckBox {
    font-size: 13px;
    spacing: 6px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #d0d0d0;
    border-radius: 3px;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #2196f3;
    border-color: #2196f3;
    image: url(check.png);
}

QCheckBox::indicator:hover {
    border-color: #b0b0b0;
}

/* Status Bar Styles */
QStatusBar {
    background-color: #f8f9fa;
    border-top: 1px solid #e0e0e0;
    font-size: 12px;
    color: #666666;
}

/* Splitter Styles */
QSplitter::handle {
    background-color: #e0e0e0;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #2196f3;
}

/* Menu Styles */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    font-size: 13px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 6px 12px;
}

QMenuBar::item:selected {
    background-color: #e3f2fd;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    font-size: 13px;
}

QMenu::item {
    padding: 8px 16px;
}

QMenu::item:selected {
    background-color: #e3f2fd;
}

QMenu::separator {
    height: 1px;
    background-color: #e0e0e0;
    margin: 4px 0;
}

/* Page Header Styles */
QFrame[objectName="page_header"] {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    padding: 16px;
}

/* Dark Mode Support */
QMainWindow[theme="dark"] {
    background-color: #1e1e1e;
    color: #ffffff;
}

QMainWindow[theme="dark"] QTextEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border-color: #404040;
}

QMainWindow[theme="dark"] QTreeWidget,
QMainWindow[theme="dark"] QListWidget {
    background-color: #2d2d2d;
    color: #ffffff;
    border-color: #404040;
}

QMainWindow[theme="dark"] QLineEdit,
QMainWindow[theme="dark"] QComboBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border-color: #404040;
}

/* Responsive Design */
@media (max-width: 800px) {
    QSplitter {
        orientation: vertical;
    }
    
    QTabWidget {
        max-width: none;
    }
}
"""

# Color scheme constants
COLORS = {
    'primary': '#2196f3',
    'primary_dark': '#1976d2',
    'primary_light': '#e3f2fd',
    'secondary': '#f5f5f5',
    'background': '#ffffff',
    'surface': '#fafafa',
    'border': '#e0e0e0',
    'border_light': '#f0f0f0',
    'text_primary': '#333333',
    'text_secondary': '#666666',
    'success': '#4caf50',
    'warning': '#ff9800',
    'error': '#f44336',
    'info': '#00bcd4'
}

# Font settings
FONTS = {
    'default_family': 'Segoe UI, Arial, sans-serif',
    'monospace_family': 'Consolas, Courier New, monospace',
    'default_size': 13,
    'header_size': 16,
    'small_size': 11
}

def apply_styles(app):
    """Apply styles to the application."""
    app.setStyleSheet(MAIN_STYLES)

def get_color(color_name):
    """Get color value by name."""
    return COLORS.get(color_name, '#000000')

def get_font_family(font_type='default'):
    """Get font family by type."""
    return FONTS.get(f'{font_type}_family', FONTS['default_family'])

def get_font_size(size_type='default'):
    """Get font size by type."""
    return FONTS.get(f'{size_type}_size', FONTS['default_size'])
