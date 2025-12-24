"""
Clase base para todos los modelos.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseModel(ABC):
    """
    Clase abstracta base para todos los modelos.
    Define la interfaz común que deben implementar todos los modelos.
    """
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a un diccionario.
        
        Returns:
            Dict[str, Any]: Diccionario con los atributos del objeto
        """
        pass
    
    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> 'BaseModel':
        """
        Carga los datos desde un diccionario.
        
        Args:
            data (Dict[str, Any]): Diccionario con los datos
            
        Returns:
            BaseModel: Instancia del modelo con los datos cargados
        """
        pass
    
    @classmethod
    @abstractmethod
    def validate_data(cls, data: Dict[str, Any]) -> bool:
        """
        Valida los datos antes de crear o actualizar un registro.
        
        Args:
            data (Dict[str, Any]): Datos a validar
            
        Returns:
            bool: True si los datos son válidos, False en caso contrario
        """
        pass