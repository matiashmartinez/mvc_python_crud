"""
Módulo con funciones de validación.
"""
import re

def validar_dni(dni: str) -> bool:
    """
    Valida que el DNI tenga un formato correcto.
    
    Args:
        dni: Número de DNI a validar
        
    Returns:
        bool: True si el DNI es válido
    """
    # Eliminar puntos y espacios
    dni_limpio = dni.replace('.', '').replace(' ', '')
    
    # Validar que sean solo números y tenga entre 7 y 8 dígitos
    if not dni_limpio.isdigit():
        return False
    
    if len(dni_limpio) < 7 or len(dni_limpio) > 8:
        return False
    
    return True

def validar_telefono(telefono: str) -> bool:
    """
    Valida que el teléfono tenga un formato correcto.
    
    Args:
        telefono: Número de teléfono a validar
        
    Returns:
        bool: True si el teléfono es válido
    """
    # Eliminar espacios, guiones y paréntesis
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    
    # Validar que sean solo números y tenga entre 8 y 15 dígitos
    if not telefono_limpio.isdigit():
        return False
    
    if len(telefono_limpio) < 8 or len(telefono_limpio) > 15:
        return False
    
    return True