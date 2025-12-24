"""
Sistema de estilos y temas para la aplicación.
"""

DARK_THEME = {
    "primary": "#2563EB",      # Azul principal
    "primary_light": "#3B82F6",
    "primary_dark": "#1E40AF",
    "secondary": "#10B981",    # Verde
    "danger": "#EF4444",       # Rojo
    "warning": "#F59E0B",      # Ámbar
    "background": "#1F2937",   # Gris oscuro
    "surface": "#111827",      # Superficie más oscura
    "border": "#374151",       # Borde gris
    "text_primary": "#F3F4F6", # Texto blanco
    "text_secondary": "#9CA3AF", # Texto gris
}

LIGHT_THEME = {
    "primary": "#2563EB",
    "primary_light": "#3B82F6",
    "primary_dark": "#1E40AF",
    "secondary": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "background": "#F9FAFB",
    "surface": "#FFFFFF",
    "border": "#E5E7EB",
    "text_primary": "#111827",
    "text_secondary": "#6B7280",
}

CURRENT_THEME = DARK_THEME


def get_stylesheet() -> str:
    """
    Genera el stylesheet completo para la aplicación.
    
    Returns:
        str: Stylesheet QSS
    """
    theme = CURRENT_THEME
    
    return f"""
    QMainWindow {{
        background-color: {theme['background']};
    }}
    
    QWidget {{
        background-color: {theme['background']};
        color: {theme['text_primary']};
    }}
    
    QFrame {{
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
    }}
    
    QLabel {{
        color: {theme['text_primary']};
        font-size: 12px;
    }}
    
    QLabel#title {{
        font-size: 20px;
        font-weight: bold;
        color: {theme['text_primary']};
        margin: 10px 0px;
    }}
    
    QLabel#subtitle {{
        font-size: 14px;
        font-weight: 600;
        color: {theme['primary']};
    }}
    
    QLineEdit, QTextEdit, QDateEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border: 2px solid {theme['border']};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, 
    QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 2px solid {theme['primary']};
        background-color: {theme['surface']};
    }}
    
    QPushButton {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 12px;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {theme['primary_light']};
    }}
    
    QPushButton:pressed {{
        background-color: {theme['primary_dark']};
    }}
    
    QPushButton#dangerBtn {{
        background-color: {theme['danger']};
    }}
    
    QPushButton#dangerBtn:hover {{
        background-color: #DC2626;
    }}
    
    QPushButton#successBtn {{
        background-color: {theme['secondary']};
    }}
    
    QPushButton#successBtn:hover {{
        background-color: #059669;
    }}
    
    QTableWidget {{
        background-color: {theme['surface']};
        alternate-background-color: {theme['background']};
        border: 1px solid {theme['border']};
        border-radius: 6px;
        gridline-color: {theme['border']};
    }}
    
    QTableWidget::item {{
        padding: 8px;
        border: none;
    }}
    
    QTableWidget::item:selected {{
        background-color: {theme['primary']};
        color: white;
    }}
    
    QHeaderView::section {{
        background-color: {theme['primary']};
        color: white;
        padding: 8px;
        border: none;
        font-weight: bold;
    }}
    
    QCheckBox {{
        color: {theme['text_primary']};
        spacing: 8px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
    }}
    
    QCheckBox::indicator:unchecked {{
        background-color: {theme['surface']};
        border: 2px solid {theme['border']};
        border-radius: 3px;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {theme['primary']};
        border: 2px solid {theme['primary']};
        border-radius: 3px;
    }}
    
    QComboBox::drop-down {{
        border: none;
        padding-right: 8px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        width: 12px;
        height: 12px;
    }}
    
    QDialog {{
        background-color: {theme['background']};
    }}
    
    QMessageBox {{
        background-color: {theme['background']};
    }}
    
    QMessageBox QLabel {{
        color: {theme['text_primary']};
    }}
    
    QMessageBox QPushButton {{
        min-width: 60px;
    }}
    """


def get_button_style(button_type: str = "primary") -> str:
    """
    Obtiene estilos para un tipo específico de botón.
    
    Args:
        button_type: Tipo de botón ('primary', 'secondary', 'danger', 'success')
    
    Returns:
        str: Clase de estilo QSS
    """
    styles = {
        "primary": "QPushButton { background-color: " + CURRENT_THEME["primary"] + "; }",
        "secondary": "QPushButton { background-color: " + CURRENT_THEME["text_secondary"] + "; }",
        "danger": "QPushButton#dangerBtn { background-color: " + CURRENT_THEME["danger"] + "; }",
        "success": "QPushButton#successBtn { background-color: " + CURRENT_THEME["secondary"] + "; }",
    }
    return styles.get(button_type, styles["primary"])
