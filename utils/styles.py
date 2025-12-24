"""
Sistema de estilos y temas para la aplicación.
"""

DARK_THEME = {
    "primary": "#2563EB",       # Azul principal
    "primary_light": "#3B82F6",
    "primary_dark": "#1E40AF",
    "secondary": "#10B981",     # Verde
    "danger": "#EF4444",        # Rojo
    "warning": "#F59E0B",       # Ámbar
    "success": "#10B981",       # Verde éxito
    "background": "#0F172A",    # Negro azulado muy oscuro
    "surface": "#1E293B",       # Superficie oscura
    "surface_light": "#334155", # Superficie más clara
    "border": "#475569",        # Borde gris oscuro
    "border_light": "#64748B",  # Borde más claro
    "text_primary": "#F8FAFC",  # Texto blanco puro
    "text_secondary": "#CBD5E1",# Texto gris claro
    "text_tertiary": "#94A3B8", # Texto gris más oscuro
    "overlay": "rgba(0, 0, 0, 0.7)",  # Overlay
}

LIGHT_THEME = {
    "primary": "#2563EB",
    "primary_light": "#3B82F6",
    "primary_dark": "#1E40AF",
    "secondary": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "success": "#10B981",
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "surface_light": "#F1F5F9",
    "border": "#E2E8F0",
    "border_light": "#CBD5E1",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_tertiary": "#64748B",
    "overlay": "rgba(0, 0, 0, 0.05)",
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
        background-color: {theme['surface_light']};
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
        alternate-background-color: {theme['surface_light']};
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
    
    QScrollBar:vertical {{
        background-color: {theme['surface']};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {theme['border_light']};
        border-radius: 6px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {theme['border']};
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
