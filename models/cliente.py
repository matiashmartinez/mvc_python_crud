"""
Modelo Cliente.
"""
from datetime import datetime
from typing import Dict, Any, Optional
from .base_model import BaseModel
from utils.validators import validar_dni, validar_telefono

class Cliente(BaseModel):
    """
    Modelo que representa a un cliente.
    
    Attributes:
        id (int): Identificador único del cliente
        nombre (str): Nombre del cliente
        apellido (str): Apellido del cliente
        dni (str): Documento Nacional de Identidad
        telefono (str): Número de teléfono
        baja (bool): Estado del cliente (activo/inactivo)
    """
    
    def __init__(self, id: Optional[int] = None, nombre: str = "", 
                 apellido: str = "", dni: str = "", telefono: str = "", 
                 baja: bool = False):
        """
        Inicializa una instancia de Cliente.
        
        Args:
            id: Identificador único (None para nuevo cliente)
            nombre: Nombre del cliente
            apellido: Apellido del cliente
            dni: Documento Nacional de Identidad
            telefono: Número de teléfono
            baja: Estado del cliente
        """
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.baja = baja
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Cliente a diccionario.
        
        Returns:
            Dict con todos los atributos del cliente
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'telefono': self.telefono,
            'baja': self.baja
        }
    
    def from_dict(self, data: Dict[str, Any]) -> 'Cliente':
        """
        Carga los datos desde un diccionario.
        
        Args:
            data: Diccionario con los datos del cliente
            
        Returns:
            Self: Instancia actualizada
        """
        self.id = data.get('id')
        self.nombre = data.get('nombre', '')
        self.apellido = data.get('apellido', '')
        self.dni = data.get('dni', '')
        self.telefono = data.get('telefono', '')
        self.baja = data.get('baja', False)
        return self
    
    @classmethod
    def validate_data(cls, data: Dict[str, Any]) -> bool:
        """
        Valida los datos del cliente.
        
        Args:
            data: Diccionario con datos a validar
            
        Returns:
            bool: True si los datos son válidos
        """
        # Validar campos requeridos
        if not data.get('nombre') or not data.get('apellido') or not data.get('dni'):
            return False
        
        # Validar DNI
        if not validar_dni(data.get('dni', '')):
            return False
        
        # Validar teléfono si está presente
        if data.get('telefono') and not validar_telefono(data.get('telefono', '')):
            return False
        
        return True
    
    def __str__(self) -> str:
        """Representación en string del cliente."""
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"
    
    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre completo del cliente."""
        return f"{self.nombre} {self.apellido}"