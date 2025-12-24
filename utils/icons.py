"""
Gestión de iconos para la aplicación usando Unicode.
"""

ICONS = {
    "add": "➕",
    "edit": "✏️",
    "delete": "🗑️",
    "save": "💾",
    "cancel": "✖️",
    "search": "🔍",
    "refresh": "🔄",
    "user": "👤",
    "users": "👥",
    "service": "🔧",
    "services": "⚙️",
    "check": "✓",
    "close": "×",
    "menu": "☰",
    "settings": "⚙️",
    "logout": "🚪",
    "home": "🏠",
    "info": "ℹ️",
    "warning": "⚠️",
    "error": "❌",
    "success": "✅",
    "phone": "📞",
    "email": "📧",
    "calendar": "📅",
    "clock": "🕐",
    "filter": "🔽",
    "sort": "↕️",
    "download": "⬇️",
    "upload": "⬆️",
    "print": "🖨️",
}


def get_icon(icon_name: str) -> str:
    """
    Obtiene un icono por nombre.
    
    Args:
        icon_name: Nombre del icono
    
    Returns:
        str: Representación Unicode del icono
    """
    return ICONS.get(icon_name, "•")


def icon_button_text(icon_name: str, text: str = "") -> str:
    """
    Crea texto de botón con icono.
    
    Args:
        icon_name: Nombre del icono
        text: Texto del botón
    
    Returns:
        str: Texto formateado con icono
    """
    icon = get_icon(icon_name)
    if text:
        return f"{icon}  {text}"
    return icon


def get_colored_icon(icon_name: str, color: str) -> str:
    """
    Obtiene un icono (nota: el color debe aplicarse a través de estilos).
    
    Args:
        icon_name: Nombre del icono
        color: Color a aplicar (para referencia, se aplica vía QSS)
    
    Returns:
        str: Icono
    """
    return get_icon(icon_name)
